"""Temporal workflow for plan orchestration using Claude Code Agent SDK.

This workflow uses a Claude Code agent to intelligently orchestrate plan execution.
The agent has access to tools that allow it to:
- Execute tasks (spawn child agent workflows)
- Check task status
- Validate task completion
- Update plan state

The agent manages the entire plan flow, making intelligent decisions about:
- Task execution order (respecting dependencies)
- Error handling and retries
- Task validation
- Progress reporting
"""

import os
import json
from typing import Dict, Any, List
from datetime import timedelta, datetime, timezone
from temporalio import workflow

# Import activities and models in unsafe block
with workflow.unsafe.imports_passed_through():
    from worker_internal.planner.activities import (
        create_plan_execution,
        update_plan_state,
        execute_task_activity,
        validate_task_completion,
        get_task_status_activity,
        continue_task_activity,
        publish_event_activity,
    )
    from worker_internal.planner.models import (
        PlanOrchestratorInput,
        PlanExecutionSummary,
        CreatePlanExecutionInput,
        UpdatePlanStateInput,
        TaskExecutionResult,
        TaskValidationResult,
        TaskStatus,
        PlanStatus,
        PlanTask,
    )
    from worker_internal.planner.agent_tools import get_agent_tools_formatted


@workflow.defn
class PlanOrchestratorWorkflow:
    """
    Orchestrates plan execution using a Claude Code agent.

    The agent is given the full plan context and tools to execute tasks,
    check status, validate completion, and update state. It makes intelligent
    decisions about execution flow while the workflow provides durability.
    """

    @workflow.signal
    async def continue_task_signal(self, data: dict):
        """
        Signal handler for continuing a task that's waiting for user input.

        Args:
            data: Dict containing task_id and user_message
        """
        task_id = data["task_id"]
        user_message = data["user_message"]

        workflow.logger.info(
            f"continue_task_signal_received: task_id={task_id}, message={user_message[:100]}"
        )
        self._pending_user_messages[task_id] = user_message

    def __init__(self):
        self._plan_execution_id: str = ""
        self._task_results: Dict[int, TaskExecutionResult] = {}
        self._completed_tasks: int = 0
        self._failed_tasks: int = 0
        self._total_tasks: int = 0
        self._tasks: List[PlanTask] = []
        self._agent_id: str = ""
        self._organization_id: str = ""
        self._worker_queue_id: str = ""
        self._jwt_token: str = ""
        self._model_id: str = ""
        self._pending_user_messages: Dict[int, str] = {}  # task_id -> user_message
        self._waiting_tasks: List[Dict] = []  # List of tasks currently waiting for user input

    @workflow.run
    async def run(self, input: PlanOrchestratorInput) -> PlanExecutionSummary:
        """
        Execute a plan using Claude Code agent orchestration.

        The agent manages the entire plan flow using provided tools.
        """
        # Import TaskStatus at function scope
        from worker_internal.planner.models import TaskExecutionResult, TaskStatus

        workflow.logger.info(
            "plan_orchestrator_started",
            extra={
                "plan_title": input.plan.title,
                "organization_id": input.organization_id,
            }
        )

        # Initialize workflow state
        execution_id = input.execution_id or str(workflow.uuid4())
        self._plan_execution_id = execution_id
        self._organization_id = input.organization_id
        self._agent_id = input.agent_id
        self._worker_queue_id = input.worker_queue_id
        self._jwt_token = input.jwt_token or ""

        # Extract tasks from plan
        if input.plan.team_breakdown:
            self._tasks = input.plan.team_breakdown[0].tasks
            self._total_tasks = len(self._tasks)
            # Always use claude-sonnet-4 for the orchestrator agent (plan model is for tasks)
            self._model_id = "kubiya/claude-sonnet-4"

        # Load previous task results if this is a continuation
        if input.is_continuation and input.previous_task_results:
            try:
                workflow.logger.info(
                    "loading_previous_task_results",
                    extra={"task_count": len(input.previous_task_results)}
                )
                # Convert dict results to TaskExecutionResult objects
                for task_id_str, result_data in input.previous_task_results.items():
                    task_id = int(task_id_str)
                    # Reconstruct TaskExecutionResult from dict
                    self._task_results[task_id] = TaskExecutionResult(**result_data)

                    # Update counts based on previous status
                    if self._task_results[task_id].status == TaskStatus.SUCCESS:
                        self._completed_tasks += 1
                    elif self._task_results[task_id].status == TaskStatus.FAILED:
                        self._failed_tasks += 1

                workflow.logger.info(
                    "previous_results_loaded",
                    extra={
                        "loaded_tasks": len(self._task_results),
                        "completed": self._completed_tasks,
                        "failed": self._failed_tasks,
                    }
                )
            except Exception as e:
                workflow.logger.error(
                    "failed_to_load_previous_results",
                    extra={"error": str(e)}
                )
                # Continue without previous results

        started_at = datetime.now(timezone.utc)

        # Step 1: Create plan execution record
        await workflow.execute_activity(
            create_plan_execution,
            CreatePlanExecutionInput(
                execution_id=execution_id,
                organization_id=input.organization_id,
                agent_id=input.agent_id,
                title=input.plan.title,
                summary=input.plan.summary,
                total_tasks=self._total_tasks,
                plan_json=input.plan.dict(),
                estimated_cost_usd=input.plan.cost_estimate.get("estimated_cost_usd"),
            ),
            start_to_close_timeout=timedelta(seconds=30),
        )

        # Publish initial TODO list (all tasks as pending)
        todo_items = [
            {
                "task_id": task.id,
                "title": task.title,
                "description": task.description,
                "status": "pending",
                "dependencies": task.dependencies or [],
                "agent_id": task.agent_id,
            }
            for task in self._tasks
        ]

        await workflow.execute_activity(
            publish_event_activity,
            args=[
                execution_id,
                "todo_list_initialized",
                {
                    "execution_id": execution_id,
                    "title": input.plan.title,
                    "total_tasks": self._total_tasks,
                    "items": todo_items,
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                }
            ],
            start_to_close_timeout=timedelta(seconds=5),
        )

        # Step 2: Execute plan using Claude Code agent
        try:
            await self._execute_plan_with_agent(input)

            # All tasks completed (workflow waits internally for user input)
            await workflow.execute_activity(
                update_plan_state,
                UpdatePlanStateInput(
                    plan_execution_id=self._plan_execution_id,
                    status=PlanStatus.COMPLETED,
                    completed_tasks=self._completed_tasks,
                    failed_tasks=self._failed_tasks,
                ),
                start_to_close_timeout=timedelta(seconds=30),
            )

            status = PlanStatus.COMPLETED

        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            workflow.logger.error(
                f"plan_execution_failed: {str(e)}\n{error_details}",
                extra={"error": str(e), "traceback": error_details}
            )

            # Mark plan as failed
            await workflow.execute_activity(
                update_plan_state,
                UpdatePlanStateInput(
                    plan_execution_id=self._plan_execution_id,
                    status=PlanStatus.FAILED,
                    completed_tasks=self._completed_tasks,
                    failed_tasks=self._failed_tasks,
                ),
                start_to_close_timeout=timedelta(seconds=30),
            )

            status = PlanStatus.FAILED

        # Step 3: Generate summary
        completed_at = datetime.now(timezone.utc)
        total_tokens = sum(r.tokens for r in self._task_results.values())
        total_cost = sum(r.cost for r in self._task_results.values())
        duration = (completed_at - started_at).total_seconds()

        # Publish plan_completed event
        await workflow.execute_activity(
            publish_event_activity,
            args=[
                self._plan_execution_id,
                "plan_completed",
                {
                    "execution_id": self._plan_execution_id,
                    "status": "completed" if status == PlanStatus.COMPLETED else "failed",
                    "completed_tasks": self._completed_tasks,
                    "failed_tasks": self._failed_tasks,
                    "total_tasks": self._total_tasks,
                    "total_tokens": total_tokens,
                    "total_cost": total_cost,
                    "duration_seconds": duration,
                    "timestamp": completed_at.isoformat(),
                }
            ],
            start_to_close_timeout=timedelta(seconds=5),
        )

        return PlanExecutionSummary(
            plan_execution_id=self._plan_execution_id,
            status=status,
            total_tasks=self._total_tasks,
            completed_tasks=self._completed_tasks,
            failed_tasks=self._failed_tasks,
            total_tokens=total_tokens,
            total_cost=total_cost,
            started_at=started_at,
            completed_at=completed_at,
            execution_time_seconds=(completed_at - started_at).total_seconds(),
            task_results=self._task_results,
        )

    async def _execute_plan_with_agent(self, input: PlanOrchestratorInput):
        """
        Execute the plan using a Claude Code agent.

        The agent is given the full plan context and tools to manage execution.
        It will intelligently orchestrate tasks, handle dependencies, and
        provide status updates.
        """
        workflow.logger.info("starting_agent_orchestration")

        # Build system prompt for orchestrator agent
        system_prompt = self._build_orchestrator_system_prompt(input.plan)

        # Build initial user prompt
        user_prompt = self._build_orchestrator_user_prompt(input.plan)

        # Get available tools
        tools = get_agent_tools_formatted()

        # Run agent conversation loop
        messages = [{"role": "user", "content": user_prompt}]
        max_turns = 100  # Safety limit

        for turn in range(max_turns):
            workflow.logger.info(
                "agent_turn",
                extra={"turn": turn, "completed_tasks": self._completed_tasks}
            )

            # Call Claude API with tools
            response = await self._call_claude_with_tools(
                messages=messages,
                system_prompt=system_prompt,
                tools=tools,
            )

            # Check if agent is done (no more tool calls)
            if not response.get("tool_calls"):
                # Agent has finished or provided final summary
                workflow.logger.info(
                    "agent_orchestration_complete",
                    extra={"final_message": response.get("content", "")[:200]}
                )
                break

            # Process tool calls - build in Anthropic format (content blocks)
            content_blocks = []

            # Add text content if present
            if response.get("content"):
                content_blocks.append({
                    "type": "text",
                    "text": response["content"]
                })

            # Add tool_use blocks
            for tool_call in response.get("tool_calls", []):
                content_blocks.append({
                    "type": "tool_use",
                    "id": tool_call["id"],
                    "name": tool_call["name"],
                    "input": tool_call["input"],
                })

            assistant_message = {
                "role": "assistant",
                "content": content_blocks,  # Array of blocks (Anthropic format)
            }

            messages.append(assistant_message)

            # Execute each tool call
            tool_results = []
            for tool_call in response.get("tool_calls", []):
                tool_name = tool_call.get("name")
                tool_input = tool_call.get("input", {})
                tool_call_id = tool_call.get("id")

                workflow.logger.info(
                    "executing_tool",
                    extra={"tool": tool_name, "input": tool_input}
                )

                result = await self._execute_tool(tool_name, tool_input)

                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": tool_call_id,
                    "content": json.dumps(result),
                })

            # Add tool results to conversation
            messages.append({
                "role": "user",
                "content": tool_results,
            })

            # Check if all tasks are complete
            if self._completed_tasks >= self._total_tasks:
                workflow.logger.info("all_tasks_completed")
                # Give agent one more turn to provide summary
                continue

        workflow.logger.info(
            "agent_orchestration_finished",
            extra={
                "total_turns": turn + 1,
                "completed_tasks": self._completed_tasks,
            }
        )

    async def _call_claude_with_tools(
        self,
        messages: List[Dict[str, Any]],
        system_prompt: str,
        tools: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """Call Claude API with tool support via activity."""
        from worker_internal.planner.activities import call_llm_activity

        response_data = await workflow.execute_activity(
            call_llm_activity,
            args=[
                messages,
                system_prompt,
                tools,
                self._model_id,
                self._plan_execution_id,
                self._organization_id,
                None,  # user_id - will be extracted from JWT
                None,  # task_id
                "plan-orchestrator",  # generation_name
                self._jwt_token,  # jwt_token for user extraction
            ],
            start_to_close_timeout=timedelta(minutes=5),
        )

        return response_data

    async def _execute_tool(self, tool_name: str, tool_input: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a tool call from the agent."""
        try:
            if tool_name == "execute_task":
                return await self._tool_execute_task(tool_input)

            elif tool_name == "get_task_status":
                return await self._tool_get_task_status(tool_input)

            elif tool_name == "validate_task":
                return await self._tool_validate_task(tool_input)

            elif tool_name == "update_plan_status":
                return await self._tool_update_plan_status(tool_input)

            elif tool_name == "list_tasks":
                return await self._tool_list_tasks(tool_input)

            else:
                return {"error": f"Unknown tool: {tool_name}"}

        except Exception as e:
            workflow.logger.error(
                "tool_execution_failed",
                extra={"tool": tool_name, "error": str(e)}
            )
            return {"error": str(e)}

    async def _tool_execute_task(self, tool_input: Dict[str, Any]) -> Dict[str, Any]:
        """Tool: Execute a task (or multiple tasks in parallel if they're independent)."""
        task_id = tool_input.get("task_id")

        # Support executing multiple tasks: execute_task(task_id=1) or execute_task(task_ids=[1,2,3])
        task_ids = tool_input.get("task_ids", [task_id] if task_id else [])

        if not task_ids:
            return {"error": "No task_id or task_ids provided"}

        # Execute tasks in parallel
        tasks_to_execute = []
        for tid in task_ids:
            task = next((t for t in self._tasks if t.id == tid), None)
            if not task:
                return {"error": f"Task {tid} not found"}

            # Check if task already has a result
            if tid in self._task_results:
                existing_result = self._task_results[tid]
                # If task is waiting for input, we'll continue it (not start new)
                if existing_result.status == TaskStatus.WAITING_FOR_INPUT:
                    workflow.logger.info(
                        "task_already_waiting_will_continue",
                        extra={"task_id": tid, "execution_id": existing_result.execution_id}
                    )
                    tasks_to_execute.append(task)
                # If task is complete or failed, skip it
                elif existing_result.status in (TaskStatus.SUCCESS, TaskStatus.FAILED):
                    workflow.logger.info(
                        "task_already_complete_skipping",
                        extra={"task_id": tid, "status": existing_result.status.value}
                    )
                    continue
                else:
                    tasks_to_execute.append(task)
            else:
                tasks_to_execute.append(task)

        # Execute all tasks in parallel
        import asyncio
        workflow.logger.info(f"executing_{len(tasks_to_execute)}_tasks_in_parallel", task_ids=task_ids)

        # Publish tasks_parallel event if multiple tasks
        if len(tasks_to_execute) > 1:
            await workflow.execute_activity(
                publish_event_activity,
                args=[
                    self._plan_execution_id,
                    "tasks_parallel",
                    {
                        "execution_id": self._plan_execution_id,
                        "task_ids": [t.id for t in tasks_to_execute],
                        "message": f"Executing {len(tasks_to_execute)} tasks in parallel",
                        "timestamp": datetime.now(timezone.utc).isoformat(),
                    }
                ],
                start_to_close_timeout=timedelta(seconds=5),
            )

        async def execute_single_task(task):
            # Check if task already has a result (from previous workflow run)
            existing_result = self._task_results.get(task.id)

            # If task was waiting for input and user already sent message, continue it
            if existing_result and existing_result.status == TaskStatus.WAITING_FOR_INPUT:
                workflow.logger.info(
                    "continuing_task_from_previous_execution",
                    extra={
                        "task_id": task.id,
                        "execution_id": existing_result.execution_id,
                    }
                )

                # Continue streaming from existing execution (message already sent via API)
                result = await workflow.execute_activity(
                    continue_task_activity,
                    args=[
                        task,
                        existing_result.execution_id,
                        "",
                        self._plan_execution_id,
                        self._jwt_token,
                        self._model_id,
                        self._organization_id,
                    ],
                    start_to_close_timeout=timedelta(minutes=15),
                )
            else:
                from worker_internal.planner.retry_logic import (
                    should_retry_task,
                    build_retry_context,
                    create_retry_attempt_record,
                )
                from worker_internal.planner.models import TaskRetryAttempt

                await workflow.execute_activity(
                    update_plan_state,
                    UpdatePlanStateInput(
                        plan_execution_id=self._plan_execution_id,
                        current_task_id=task.id,
                        current_task_status=TaskStatus.RUNNING,
                    ),
                    start_to_close_timeout=timedelta(seconds=30),
                )

                dependency_outputs = {}
                if task.dependencies:
                    for dep_task_id in task.dependencies:
                        if dep_task_id in self._task_results:
                            dependency_outputs[dep_task_id] = self._task_results[dep_task_id].output

                retry_history: List[TaskRetryAttempt] = []
                result = None
                current_attempt = 1

                while current_attempt <= 5:
                    retry_context = build_retry_context(retry_history, current_attempt) if retry_history else None

                    if retry_context:
                        workflow.logger.info(
                            f"retrying_task_attempt_{current_attempt}",
                            extra={
                                "task_id": task.id,
                                "attempt": current_attempt,
                                "previous_failures": len(retry_history),
                            }
                        )

                    result = await workflow.execute_activity(
                        execute_task_activity,
                        args=[
                            task,
                            self._plan_execution_id,
                            self._organization_id,
                            dependency_outputs,
                            self._jwt_token,
                            self._model_id,
                            retry_context,
                            self._worker_queue_id,  # Pass workflow-level worker_queue_id as fallback
                        ],
                        start_to_close_timeout=timedelta(minutes=15),
                    )

                    if result.status == TaskStatus.SUCCESS:
                        result.retry_count = current_attempt - 1
                        result.retry_history = retry_history
                        break

                    if result.status == TaskStatus.WAITING_FOR_INPUT:
                        break

                    if should_retry_task(result, current_attempt):
                        retry_attempt = create_retry_attempt_record(result, current_attempt)
                        retry_history.append(retry_attempt)

                        from worker_internal.planner.event_models import TaskRetryEvent
                        from worker_internal.planner.activities import publish_event_activity

                        await workflow.execute_activity(
                            publish_event_activity,
                            args=[
                                self._plan_execution_id,
                                "task_retry",
                                {
                                    "execution_id": self._plan_execution_id,
                                    "task_id": task.id,
                                    "title": task.title,
                                    "attempt_number": current_attempt + 1,
                                    "max_attempts": 5,
                                    "previous_error": (result.error or "Unknown error")[:200],
                                    "timestamp": datetime.now(timezone.utc).isoformat(),
                                }
                            ],
                            start_to_close_timeout=timedelta(seconds=5),
                        )

                        current_attempt += 1
                    else:
                        result.retry_count = current_attempt - 1
                        result.retry_history = retry_history
                        workflow.logger.error(
                            f"task_failed_after_{current_attempt}_attempts",
                            extra={
                                "task_id": task.id,
                                "final_error": result.error[:200] if result.error else "unknown",
                            }
                        )
                        break

            # Check if task needs user input
            if result.status == TaskStatus.WAITING_FOR_INPUT:
                workflow.logger.info(
                    f"task_waiting_for_user_input: task_id={task.id}, execution_id={result.execution_id}"
                )

                # Add to waiting tasks list for tracking
                waiting_task_info = {
                    "task_id": task.id,
                    "execution_id": result.execution_id,
                    "question": result.user_question or "Please provide input",
                    "waiting_since": datetime.now(timezone.utc).isoformat(),
                }
                self._waiting_tasks.append(waiting_task_info)

                # Update plan status to pending_user_input
                await workflow.execute_activity(
                    update_plan_state,
                    UpdatePlanStateInput(
                        plan_execution_id=self._plan_execution_id,
                        status=PlanStatus.PENDING_USER_INPUT,
                        current_task_id=task.id,
                        current_task_status=TaskStatus.WAITING_FOR_INPUT,
                        waiting_tasks=self._waiting_tasks,
                    ),
                    start_to_close_timeout=timedelta(seconds=30),
                )

                workflow.logger.info(f"⏸️  PAUSING WORKFLOW: task_id={task.id} - waiting for signal")

                # PAUSE: Wait indefinitely for user to send signal (no timeout)
                await workflow.wait_condition(
                    lambda: task.id in self._pending_user_messages
                )

                # Resume: User sent message via signal (message was already sent by /continue endpoint)
                self._pending_user_messages.pop(task.id, None)  # Clear the signal data

                workflow.logger.info(
                    f"▶️  WORKFLOW RESUMED: task_id={task.id} - message already sent by API, streaming result"
                )

                # Remove from waiting tasks list
                self._waiting_tasks = [wt for wt in self._waiting_tasks if wt["task_id"] != task.id]

                # Update status back to running
                new_status = PlanStatus.PENDING_USER_INPUT if self._waiting_tasks else PlanStatus.RUNNING
                await workflow.execute_activity(
                    update_plan_state,
                    UpdatePlanStateInput(
                        plan_execution_id=self._plan_execution_id,
                        status=new_status,
                        current_task_id=task.id,
                        current_task_status=TaskStatus.RUNNING,
                        waiting_tasks=self._waiting_tasks,
                    ),
                    start_to_close_timeout=timedelta(seconds=30),
                )

                # Continue the task (message already sent by /continue endpoint, so pass empty string)
                result = await workflow.execute_activity(
                    continue_task_activity,
                    args=[
                        task,
                        result.execution_id,
                        "",
                        self._plan_execution_id,
                        self._jwt_token,
                        self._model_id,
                        self._organization_id,
                    ],
                    start_to_close_timeout=timedelta(minutes=15),
                )

                workflow.logger.info(
                    f"✅ TASK CONTINUED: task_id={task.id}, status={result.status.value}, output_length={len(result.output)}"
                )

            # Store
            self._task_results[task.id] = result
            if result.status == TaskStatus.SUCCESS:
                self._completed_tasks += 1
                workflow.logger.info(f"✅ TASK COMPLETED: task_id={task.id}, completed_count={self._completed_tasks}/{self._total_tasks}")
            elif result.status == TaskStatus.FAILED:
                self._failed_tasks += 1
                workflow.logger.info(f"❌ TASK FAILED: task_id={task.id}, error={result.error[:100] if result.error else 'none'}")
            # WAITING_FOR_INPUT tasks are not counted as failed or completed yet

            # Update: task completed
            await workflow.execute_activity(
                update_plan_state,
                UpdatePlanStateInput(
                    plan_execution_id=self._plan_execution_id,
                    current_task_id=task.id,
                    current_task_status=result.status,
                    completed_tasks=self._completed_tasks,
                    failed_tasks=self._failed_tasks,
                ),
                start_to_close_timeout=timedelta(seconds=30),
            )

            return result

        # Execute all tasks concurrently
        results = await asyncio.gather(*[execute_single_task(t) for t in tasks_to_execute])

        # Log summary before returning to orchestrator
        workflow.logger.info(
            f"🎯 EXECUTE_TASK TOOL COMPLETE: {len(results)} tasks, "
            f"completed={len([r for r in results if r.status == TaskStatus.SUCCESS])}, "
            f"failed={len([r for r in results if r.status == TaskStatus.FAILED])}, "
            f"waiting={len([r for r in results if r.status == TaskStatus.WAITING_FOR_INPUT])}"
        )

        # Return summary
        return {
            "success": True,
            "task_ids": task_ids,
            "completed": len([r for r in results if r.status == TaskStatus.SUCCESS]),
            "failed": len([r for r in results if r.status == TaskStatus.FAILED]),
            "results": [
                {
                    "task_id": r.task_id,
                    "status": r.status.value,
                    "output": r.output,  # Full output, no truncation
                    "execution_id": r.execution_id,
                }
                for r in results
            ]
        }

    async def _tool_get_task_status(self, tool_input: Dict[str, Any]) -> Dict[str, Any]:
        """Tool: Get task status."""
        task_id = tool_input.get("task_id")

        result = await workflow.execute_activity(
            get_task_status_activity,
            args=[task_id, self._task_results],
            start_to_close_timeout=timedelta(seconds=10),
        )

        return result

    async def _tool_validate_task(self, tool_input: Dict[str, Any]) -> Dict[str, Any]:
        """Tool: Validate task completion."""
        task_id = tool_input.get("task_id")

        # Find task and result
        task = next((t for t in self._tasks if t.id == task_id), None)
        if not task:
            return {"error": f"Task {task_id} not found"}

        if task_id not in self._task_results:
            return {"error": f"Task {task_id} not executed yet"}

        result = self._task_results[task_id]

        # Validate
        validation = await workflow.execute_activity(
            validate_task_completion,
            args=[
                task,
                result,
                self._plan_execution_id,
                self._organization_id,
                None,  # user_id - will be extracted from JWT
                self._jwt_token,  # jwt_token for user extraction
            ],
            start_to_close_timeout=timedelta(minutes=2),
        )

        return {
            "task_id": task_id,
            "validation_status": validation.status.value,
            "reason": validation.reason,
            "confidence": validation.confidence,
            "suggestions": validation.suggestions,
        }

    async def _tool_update_plan_status(self, tool_input: Dict[str, Any]) -> Dict[str, Any]:
        """Tool: Update plan status."""
        status_message = tool_input.get("status_message", "")
        completed_tasks = tool_input.get("completed_tasks")

        workflow.logger.info(
            "plan_status_update",
            extra={"message": status_message, "completed": completed_tasks}
        )

        # Update state
        await workflow.execute_activity(
            update_plan_state,
            UpdatePlanStateInput(
                plan_execution_id=self._plan_execution_id,
                completed_tasks=completed_tasks if completed_tasks is not None else self._completed_tasks,
                failed_tasks=self._failed_tasks,
            ),
            start_to_close_timeout=timedelta(seconds=30),
        )

        return {"success": True, "message": "Status updated"}

    async def _continue_task_execution(
        self,
        task: PlanTask,
        execution_id: str,
        user_message: str,
    ) -> TaskExecutionResult:
        """
        Continue a task execution after receiving user input.

        This sends the user's message to the existing agent execution,
        then continues streaming events until the task completes or
        needs more input.
        """
        workflow.logger.info(
            "continuing_task_after_user_input",
            extra={"task_id": task.id, "execution_id": execution_id}
        )

        # Create an activity to continue the task
        from worker_internal.planner.activities import continue_task_activity

        result = await workflow.execute_activity(
            continue_task_activity,
            args=[task, execution_id, user_message, self._jwt_token, self._model_id],
            start_to_close_timeout=timedelta(minutes=15),
        )

        return result

    async def _tool_list_tasks(self, tool_input: Dict[str, Any]) -> Dict[str, Any]:
        """Tool: List all tasks."""
        tasks_info = []
        for task in self._tasks:
            task_status = "pending"
            if task.id in self._task_results:
                task_status = self._task_results[task.id].status.value

            tasks_info.append({
                "id": task.id,
                "title": task.title,
                "description": task.description[:100],
                "dependencies": task.dependencies,
                "status": task_status,
                "priority": task.priority,
            })

        return {
            "total_tasks": self._total_tasks,
            "completed_tasks": self._completed_tasks,
            "failed_tasks": self._failed_tasks,
            "tasks": tasks_info,
        }

    def _build_orchestrator_system_prompt(self, plan: Any) -> str:
        """Build system prompt for orchestrator agent."""
        agent_info = plan.team_breakdown[0] if plan.team_breakdown else None

        return f"""You are a Plan Orchestrator Agent for the Kubiya platform. Your job is to intelligently manage the execution of multi-task plans.

## Your Role
{agent_info.agent_name if agent_info else 'Plan Orchestrator'}

## Responsibilities
{chr(10).join(f"- {r}" for r in (agent_info.responsibilities if agent_info else ['Execute tasks in correct order', 'Monitor progress', 'Validate completion']))}

## Available Tools
You have access to these tools to manage plan execution:

1. **execute_task(task_id)** - Execute a specific task by spawning an agent execution
2. **get_task_status(task_id)** - Check the status of a task execution
3. **validate_task(task_id)** - Validate that a task completed successfully using LLM analysis
4. **update_plan_status(status_message, completed_tasks)** - Update the overall plan status for UI
5. **list_tasks()** - Get a list of all tasks with their dependencies and status

## Your Process
1. First, call list_tasks() to understand the plan structure and identify dependencies
2. **IMPORTANT: Execute independent tasks in PARALLEL for speed!**
   - Group tasks by dependency level
   - Tasks with no dependencies can run together: execute_task(task_ids=[1, 2, 3])
   - Tasks that depend on others run after their dependencies complete
3. For each task or group:
   - Call execute_task(task_ids=[...]) to run independent tasks in parallel
   - OR execute_task(task_id=N) for single tasks
   - Wait for completion
   - Call validate_task(task_id) to verify success if needed
   - Provide status updates using update_plan_status()
4. Handle errors gracefully - if a task fails, decide whether to retry or continue with other tasks
5. Provide clear, concise updates about progress
6. When all tasks are complete, provide a final summary

## Important Guidelines
- ALWAYS respect task dependencies - don't execute a task until its dependencies are complete
- Use validate_task() to ensure tasks actually completed successfully
- Provide regular status updates so users can track progress
- Be intelligent about error handling - don't fail the entire plan for one task failure
- Think step by step and explain your reasoning

Begin by analyzing the plan and executing tasks systematically.
"""

    def _build_orchestrator_user_prompt(self, plan: Any) -> str:
        """Build initial user prompt for orchestrator agent."""
        tasks_summary = []
        if plan.team_breakdown and plan.team_breakdown[0].tasks:
            for task in plan.team_breakdown[0].tasks:
                tasks_summary.append(
                    f"- Task {task.id}: {task.title} (depends on: {task.dependencies or 'none'})"
                )

        return f"""# Plan Execution Request

## Plan: {plan.title}

{plan.summary}

## Tasks to Execute
{chr(10).join(tasks_summary)}

## Success Criteria
{chr(10).join(f"- {c}" for c in plan.success_criteria)}

## Risks to Consider
{chr(10).join(f"- {r}" for r in plan.risks)}

Please execute this plan systematically. Start by calling list_tasks() to see the full task structure, then proceed with execution while respecting dependencies.

Provide status updates as you progress, and validate each task after completion.
"""
