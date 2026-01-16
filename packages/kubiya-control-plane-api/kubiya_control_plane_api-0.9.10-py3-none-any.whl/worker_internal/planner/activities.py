"""Temporal activities for plan orchestration."""

import os
import json
import httpx
from typing import Dict, Any, Optional, List
from datetime import datetime, timezone
from temporalio import activity
import structlog

from worker_internal.planner.models import (
    CreatePlanExecutionInput,
    UpdatePlanStateInput,
    TaskExecutionResult,
    TaskValidationResult,
    TaskStatus,
    PlanTask,
    TaskRetryContext,
)
from worker_internal.planner.event_publisher import publish_plan_event
from worker_internal.planner.event_models import (
    PlanStartedEvent,
    TaskStartedEvent,
    TaskRunningEvent,
    TaskWaitingForInputEvent,
    TaskCompletedEvent,
    TaskValidationStartedEvent,
    TaskValidationCompleteEvent,
    PlanStatusUpdateEvent,
    TodoListInitializedEvent,
    TodoItemUpdatedEvent,
    TodoItem,
)

logger = structlog.get_logger()


def extract_user_from_jwt(jwt_token: Optional[str]) -> Optional[str]:
    """
    Extract user email from JWT token.

    Args:
        jwt_token: JWT token string

    Returns:
        User email if found, None otherwise
    """
    if not jwt_token:
        return None

    try:
        import jwt as pyjwt
        # Decode without verification to extract email
        decoded = pyjwt.decode(jwt_token, options={"verify_signature": False})
        return decoded.get("email")
    except Exception as e:
        logger.warning(f"failed_to_extract_user_from_jwt: {str(e)}")
        return None


def build_langfuse_metadata(
    plan_execution_id: str,
    generation_name: str,
    user_id: Optional[str] = None,
    organization_id: Optional[str] = None,
    agent_id: Optional[str] = None,
    task_id: Optional[int] = None,
) -> Dict[str, Any]:
    """
    Build Langfuse metadata for LLM calls in plan execution.

    This follows the same pattern as the agent worker to ensure proper
    observability in Langfuse. All LLM calls within a plan execution
    will be grouped under the same trace.

    Args:
        plan_execution_id: Plan execution ID (used as trace_id and session_id)
        generation_name: Name for this specific LLM call (e.g., "task-1-completion-analysis")
        user_id: User email (proxy will format as email-org)
        organization_id: Organization ID
        agent_id: Agent ID making the call
        task_id: Task ID if this call is for a specific task

    Returns:
        Context dict for proxy to inject Langfuse metadata
    """
    context = {}

    # CRITICAL: Pass raw user_id and organization_id for proxy to format
    # Proxy will create trace_user_id = "email-org" to avoid 401 errors
    if user_id:
        context["user_id"] = user_id
    if organization_id:
        context["organization_id"] = organization_id

    # CRITICAL: Use plan_execution_id as session_id to group all LLM calls
    # Proxy will set this as trace_id
    context["session_id"] = plan_execution_id

    # Set custom names (proxy will preserve these instead of defaulting to "agent-chat")
    context["trace_name"] = "plan-execution"
    context["generation_name"] = generation_name
    context["name"] = generation_name

    # Additional context metadata
    if agent_id:
        context["agent_id"] = agent_id
    if task_id is not None:
        context["task_id"] = task_id

    return context


@activity.defn
async def publish_event_activity(
    execution_id: str,
    event_type: str,
    event_data: Dict[str, Any],
) -> bool:
    """Activity to publish events from workflow context."""
    try:
        redis_client = get_redis_client()
        if not redis_client:
            activity.logger.warning("redis_not_available", execution_id=execution_id[:8])
            return False

        message = {
            "event_type": event_type,
            "data": event_data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        # Serialize to JSON string
        message_json = json.dumps(message)

        list_key = f"plan-execution:{execution_id}:events"
        channel = f"plan-execution:{execution_id}:stream"

        await redis_client.lpush(list_key, message_json)
        await redis_client.ltrim(list_key, 0, 999)
        await redis_client.expire(list_key, 3600)
        await redis_client.publish(channel, message_json)

        activity.logger.debug(
            "plan_event_published_from_workflow",
            execution_id=execution_id[:8],
            event_type=event_type,
        )
        return True
    except Exception as e:
        activity.logger.error("publish_event_failed", error=str(e), execution_id=execution_id[:8])
        return False


def get_redis_client():
    """Get Redis client for event publishing."""
    from control_plane_api.app.lib.redis_client import get_redis_client as _get_redis_client
    return _get_redis_client()


def get_control_plane_url() -> str:
    """Get Control Plane API URL from environment."""
    return os.getenv("CONTROL_PLANE_URL", "http://localhost:8000")


def get_auth_headers(jwt_token: Optional[str] = None) -> Dict[str, str]:
    """Get authentication headers for Control Plane API."""
    headers = {"Content-Type": "application/json"}
    if jwt_token:
        headers["Authorization"] = f"Bearer {jwt_token}"
    return headers


@activity.defn
async def create_plan_execution(input: CreatePlanExecutionInput) -> Dict[str, Any]:
    """
    Create plan execution record in database.

    NOTE: The API already creates this record before starting the workflow,
    so this activity just validates it exists and returns success.
    """
    activity.logger.info(
        "plan_execution_already_created_by_api",
        extra={
            "execution_id": input.execution_id[:8],
            "title": input.title,
            "total_tasks": input.total_tasks,
        }
    )

    # Publish plan_started event
    await publish_plan_event(
        execution_id=input.execution_id,
        event_type="plan_started",
        event_data=PlanStartedEvent(
            execution_id=input.execution_id,
            title=input.title,
            total_tasks=input.total_tasks,
            agent_id=input.agent_id,
        )
    )

    # Record already created by API, just return success
    return {"success": True, "plan_execution_id": input.execution_id}


@activity.defn
async def update_plan_state(input: UpdatePlanStateInput) -> Dict[str, Any]:
    """
    Update plan execution state in database via HTTP API.
    """
    activity.logger.info(
        f"updating_plan_state: plan_id={input.plan_execution_id[:8]}, status={input.status}, completed={input.completed_tasks}"
    )

    try:
        control_plane_url = get_control_plane_url()

        # Build update payload
        updates = {}
        if input.status is not None:
            updates["status"] = input.status.value if hasattr(input.status, 'value') else input.status
        if input.completed_tasks is not None:
            updates["completed_tasks"] = input.completed_tasks
        if input.failed_tasks is not None:
            updates["failed_tasks"] = input.failed_tasks
        if input.waiting_tasks is not None:
            updates["waiting_tasks"] = input.waiting_tasks
        if input.dag_state is not None:
            updates["dag_state"] = input.dag_state
        if input.total_tokens is not None:
            updates["total_tokens"] = input.total_tokens
        if input.actual_cost_usd is not None:
            updates["actual_cost_usd"] = input.actual_cost_usd

        if not updates:
            return {"success": True, "message": "No updates to apply"}

        # Update via API
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.patch(
                f"{control_plane_url}/api/v1/tasks/plan/{input.plan_execution_id}",
                json=updates,
            )

            if response.status_code not in (200, 201):
                activity.logger.error(
                    f"failed_to_update_plan_state: status={response.status_code}, response={response.text[:200]}"
                )
                return {"success": False, "error": response.text}

            activity.logger.info(f"plan_state_updated: updates={list(updates.keys())}")
            return {"success": True}

    except Exception as e:
        activity.logger.error(f"update_plan_state_failed: {str(e)}")
        return {"success": False, "error": str(e)}


@activity.defn
async def execute_task_activity(
    task: PlanTask,
    plan_execution_id: str,
    organization_id: str,
    dependency_outputs: Optional[Dict[int, str]] = None,
    jwt_token: Optional[str] = None,
    model_id: Optional[str] = None,
    retry_context: Optional[TaskRetryContext] = None,
    default_worker_queue_id: Optional[str] = None,  # Fallback from workflow input
) -> TaskExecutionResult:
    """
    Execute a task by triggering an agent execution.

    This spawns a child agent execution and waits for it to complete.
    Returns the execution result for the orchestrator agent to analyze.

    Uses agent_id and worker_queue_id from the task object.
    Falls back to default_worker_queue_id if task doesn't have one.
    Includes outputs from dependent tasks if provided.
    If retry_context is provided, enriches the task with failure history.
    """
    from worker_internal.planner.retry_logic import enrich_task_with_retry_context

    if retry_context:
        task = enrich_task_with_retry_context(task, retry_context)

    # Use agent_id and worker_queue_id from task, with fallback to workflow-level default
    agent_id = task.agent_id
    worker_queue_id = task.worker_queue_id or default_worker_queue_id

    if not agent_id:
        raise ValueError(f"Task {task.id} missing agent_id")
    if not worker_queue_id:
        raise ValueError(f"Task {task.id} missing worker_queue_id (and no default_worker_queue_id provided)")

    activity.logger.info(
        "executing_task",
        extra={
            "task_id": task.id,
            "task_title": task.title,
            "plan_execution_id": plan_execution_id[:8],
            "has_jwt_token": bool(jwt_token),
            "jwt_token_length": len(jwt_token) if jwt_token else 0,
            "worker_queue_id": worker_queue_id,
            "agent_id": agent_id,
            "dependencies": task.dependencies,
            "has_dependency_outputs": bool(dependency_outputs),
            "is_retry": bool(retry_context),
            "retry_attempt": retry_context.current_attempt if retry_context else 0,
        }
    )

    started_at = datetime.now(timezone.utc)

    try:
        # Build dependency context if this task depends on others
        dependency_context = ""
        if task.dependencies and dependency_outputs:
            dependency_context = "\n## Outputs from Previous Tasks\n"
            for dep_task_id in task.dependencies:
                if dep_task_id in dependency_outputs:
                    output = dependency_outputs[dep_task_id]
                    dependency_context += f"\n### Task {dep_task_id} Output:\n```\n{output}\n```\n"
                else:
                    dependency_context += f"\n### Task {dep_task_id}: Output not available\n"
            dependency_context += "\n"

        # Build enriched prompt for the task
        enriched_prompt = f"""# Task: {task.title}

## Description
{task.description}

## Detailed Instructions
{task.details}
{dependency_context}
## Test Strategy
{task.test_strategy or 'Complete the task as described and verify the output.'}

## Priority
{task.priority}

## Available Skills
{', '.join(task.skills_to_use) if task.skills_to_use else 'Use any available skills as needed'}

Please complete this task following the instructions above. Be thorough and verify your work.
"""

        # Trigger agent execution via Control Plane API
        control_plane_url = get_control_plane_url()

        async with httpx.AsyncClient(timeout=600.0) as client:  # 10 min timeout for task execution
            response = await client.post(
                f"{control_plane_url}/api/v1/agents/{agent_id}/execute",
                json={
                    "prompt": enriched_prompt,
                    "worker_queue_id": worker_queue_id,  # Use worker_queue_id from plan request
                    # Don't pass execution_id - let API generate it
                    "user_metadata": {
                        "plan_execution_id": plan_execution_id,
                        "task_id": task.id,
                        "task_title": task.title,
                        "skills_filter": task.skills_to_use,
                        "env_vars_filter": task.env_vars_to_use,
                        "secrets_filter": task.secrets_to_use,
                        "session_id": plan_execution_id,  # For agent worker to use
                    },
                    "runtime_config": {
                        "session_id": plan_execution_id,  # CRITICAL: Use plan_execution_id to group agent LLM calls under plan trace
                    }
                },
                headers=get_auth_headers(jwt_token),
            )

            if response.status_code not in (200, 201, 202):
                activity.logger.error(
                    f"agent_execution_api_failed: status={response.status_code}, response={response.text[:500]}"
                )
                raise Exception(f"Failed to execute task: {response.text}")

            result = response.json()
            # Use execution_id from API response
            execution_id = result.get("execution_id")
            activity.logger.info(
                f"agent_execution_started: execution_id={execution_id}, workflow_id={result.get('workflow_id')}"
            )

            # Publish task_started event (now we have task_execution_id)
            await publish_plan_event(
                execution_id=plan_execution_id,
                event_type="task_started",
                event_data=TaskStartedEvent(
                    execution_id=plan_execution_id,
                    task_id=task.id,
                    title=task.title,
                    description=task.description,
                    agent_id=agent_id,
                    task_execution_id=execution_id,  # Agent execution ID
                    dependencies=task.dependencies or [],
                )
            )

            # Publish TODO update: pending -> running
            await publish_plan_event(
                execution_id=plan_execution_id,
                event_type="todo_item_updated",
                event_data=TodoItemUpdatedEvent(
                    execution_id=plan_execution_id,
                    task_id=task.id,
                    title=task.title,
                    old_status="pending",
                    new_status="running",
                    message=f"Started executing: {task.title}",
                )
            )

            # Stream execution events instead of polling
            import asyncio
            activity.logger.info(f"streaming_task_execution: execution_id={execution_id}, task_id={task.id}")

            final_status = None
            final_output = ""
            final_tokens = 0
            final_cost = 0.0
            final_error = None
            all_events = []  # Store all stream events

            # Stream events from execution
            async with client.stream(
                "GET",
                f"{control_plane_url}/api/v1/executions/{execution_id}/stream",
                headers=get_auth_headers(jwt_token),
                timeout=600.0,  # 10 min timeout
            ) as stream_response:
                if stream_response.status_code not in (200, 201):
                    raise Exception(f"Failed to stream execution: {stream_response.status_code}")

                current_event = None
                async for line in stream_response.aiter_lines():
                    if not line:
                        continue

                    # Parse SSE format: "event: type\ndata: json"
                    if line.startswith("event: "):
                        current_event = line[7:]  # Get event type
                        continue

                    if line.startswith("data: "):
                        try:
                            # Parse SSE data
                            data = json.loads(line[6:])  # Remove "data: " prefix
                            status = data.get("status")

                            # Store event
                            all_events.append({
                                "event": current_event,
                                "data": data,
                                "timestamp": data.get("timestamp", datetime.now(timezone.utc).isoformat())
                            })

                            # Log event
                            activity.logger.info(
                                f"stream_event: event={current_event}, "
                                f"status={status}, task_id={task.id}"
                            )

                            # Track status events for completion
                            if current_event == "status" and status:
                                if status in ("waiting_for_input", "completed", "success", "failed", "error"):
                                    final_status = status
                                    activity.logger.info(f"✅ Task complete! status={final_status}, task_id={task.id}")
                                    break  # Done!

                            # Track message content for summary output (only assistant messages)
                            if current_event in ("message", "message_chunk"):
                                # Only capture assistant messages, not user prompts
                                msg_data = data.get("data", {})
                                role = msg_data.get("role", data.get("role"))
                                content = msg_data.get("content", data.get("content", ""))

                                if role == "assistant" and content and content != "(no content)":
                                    final_output += content

                        except json.JSONDecodeError:
                            continue  # Skip malformed events

            # Return result based on stream
            completed_at = datetime.now(timezone.utc)

            # Determine task status based on final_status
            if final_status in ("completed", "success"):
                # Task completed successfully
                task_status = TaskStatus.SUCCESS
                needs_continuation = False
                user_question = None

            elif final_status == "waiting_for_input":
                # Agent is waiting for user response - use LLM to analyze if task is complete
                activity.logger.info(
                    f"analyzing_waiting_for_input_status: task_id={task.id}, analyzing if task is complete or needs user input"
                )

                analysis = await analyze_task_completion_status(
                    task,
                    final_output,
                    all_events,
                    plan_execution_id=plan_execution_id,
                    organization_id=organization_id,
                    user_id=None,
                    jwt_token=jwt_token,
                )

                if analysis.get("task_complete", False):
                    # Task is actually complete despite waiting_for_input status
                    activity.logger.info(
                        f"task_complete_despite_waiting: task_id={task.id}, "
                        f"reasoning={analysis.get('reasoning')}"
                    )
                    task_status = TaskStatus.SUCCESS
                    needs_continuation = False
                    user_question = None
                else:
                    # Task genuinely needs user input to continue
                    activity.logger.info(
                        f"task_needs_user_input: task_id={task.id}, "
                        f"user_question={analysis.get('user_question')}"
                    )
                    task_status = TaskStatus.WAITING_FOR_INPUT
                    needs_continuation = True
                    user_question = analysis.get("user_question")

            else:
                # Task failed or errored
                task_status = TaskStatus.FAILED
                needs_continuation = False
                user_question = None

            # Publish appropriate event based on status
            if task_status == TaskStatus.WAITING_FOR_INPUT:
                await publish_plan_event(
                    execution_id=plan_execution_id,
                    event_type="task_waiting_for_input",
                    event_data=TaskWaitingForInputEvent(
                        execution_id=plan_execution_id,
                        task_id=task.id,
                        question=user_question or "Waiting for user input",
                        task_execution_id=execution_id,
                    )
                )
                # Publish TODO update: running -> waiting_for_input
                await publish_plan_event(
                    execution_id=plan_execution_id,
                    event_type="todo_item_updated",
                    event_data=TodoItemUpdatedEvent(
                        execution_id=plan_execution_id,
                        task_id=task.id,
                        title=task.title,
                        old_status="running",
                        new_status="waiting_for_input",
                        message=user_question or "Waiting for user input",
                    )
                )
            else:
                # Task completed (success or failed)
                await publish_plan_event(
                    execution_id=plan_execution_id,
                    event_type="task_completed",
                    event_data=TaskCompletedEvent(
                        execution_id=plan_execution_id,
                        task_id=task.id,
                        title=task.title,
                        status="success" if task_status == TaskStatus.SUCCESS else "failed",
                        output=final_output[:500] if final_output else "",  # Truncate for event
                        error=final_error,
                        tokens=final_tokens,
                        cost=final_cost,
                    )
                )
                # Publish TODO update: running -> completed/failed
                await publish_plan_event(
                    execution_id=plan_execution_id,
                    event_type="todo_item_updated",
                    event_data=TodoItemUpdatedEvent(
                        execution_id=plan_execution_id,
                        task_id=task.id,
                        title=task.title,
                        old_status="running",
                        new_status="completed" if task_status == TaskStatus.SUCCESS else "failed",
                        message=f"Task {'completed successfully' if task_status == TaskStatus.SUCCESS else 'failed'}",
                    )
                )

            return TaskExecutionResult(
                task_id=task.id,
                status=task_status,
                execution_id=execution_id,
                output=final_output,
                events=all_events,  # Include all stream events
                tokens=final_tokens,
                cost=final_cost,
                started_at=started_at,
                completed_at=completed_at,
                error=final_error,
                needs_continuation=needs_continuation,
                user_question=user_question,
            )

    except Exception as e:
        activity.logger.error(
            "execute_task_failed",
            extra={
                "task_id": task.id,
                "error": str(e),
            }
        )

        return TaskExecutionResult(
            task_id=task.id,
            status=TaskStatus.FAILED,
            execution_id=f"{plan_execution_id}-task-{task.id}",
            output="",
            events=[],  # No events on error
            tokens=0,
            cost=0.0,
            started_at=started_at,
            completed_at=datetime.now(timezone.utc),
            error=str(e),
        )


@activity.defn
async def analyze_task_completion_status(
    task: PlanTask,
    agent_output: str,
    events: List[Dict[str, Any]] = None,
    plan_execution_id: Optional[str] = None,
    organization_id: Optional[str] = None,
    user_id: Optional[str] = None,
    jwt_token: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Analyze if a task is complete or needs user input.

    When an agent execution reaches 'waiting_for_input' status, we need to determine:
    - Is the task actually complete? (agent finished the work)
    - Or does the task need user input to continue? (agent is asking a question)

    This uses LLM analysis to make an intelligent decision.
    """
    # Extract user_id from JWT if not provided
    if not user_id and jwt_token:
        user_id = extract_user_from_jwt(jwt_token)
    # Extract full conversation from events (all user/assistant messages + tool executions)
    conversation_summary = ""
    if events:
        # Build conversation from message and tool events
        messages_by_id = {}  # message_id -> accumulated content
        conversation_order = []  # (message_id, role, timestamp)
        tool_executions = []  # Track tool executions

        for event in events:
            event_type = event.get("event")

            # Track tool executions
            if event_type == "tool_completed":
                tool_data = event.get("data", {}).get("data", {})
                tool_name = tool_data.get("tool_name", "")
                tool_output = tool_data.get("tool_output", "")
                if tool_name and tool_output:
                    # Extract stdout if it's in dict format
                    if isinstance(tool_output, str) and "stdout" in tool_output:
                        try:
                            import ast
                            tool_dict = ast.literal_eval(tool_output)
                            if isinstance(tool_dict, dict):
                                tool_output = tool_dict.get("tool_response", {}).get("stdout", tool_output)
                        except:
                            pass
                    tool_executions.append(f"TOOL({tool_name}): {tool_output}")

            # Track messages
            if event_type in ("message", "message_chunk"):
                data = event.get("data", {})
                if isinstance(data, dict):
                    if event_type == "message_chunk" and "data" in data:
                        msg_data = data.get("data", {})
                    else:
                        msg_data = data

                    role = msg_data.get("role")
                    content = msg_data.get("content", "")
                    message_id = msg_data.get("message_id", "")
                    timestamp = event.get("timestamp", "")

                    # Skip tool messages and empty/no-content
                    if role in ("user", "assistant") and content and content != "(no content)":
                        if message_id not in messages_by_id:
                            messages_by_id[message_id] = ""
                            conversation_order.append((message_id, role, timestamp))

                        # Accumulate chunks for this message
                        messages_by_id[message_id] += content

        # Build conversation in order, including tool executions
        conversation_turns = []
        for message_id, role, timestamp in conversation_order:
            content = messages_by_id[message_id].strip()
            if content:
                truncated_content = content if len(content) <= 500 else content[:500] + "..."
                conversation_turns.append(f"{role.upper()}: {truncated_content}")

        # Add tool executions to conversation
        if tool_executions:
            conversation_turns.extend(tool_executions)

        if conversation_turns:
            conversation_summary = "\n\n".join(conversation_turns)
            activity.logger.info(
                f"extracted_full_conversation_from_events",
                extra={
                    "task_id": task.id,
                    "total_events": len(events),
                    "conversation_turns": len(conversation_turns),
                    "conversation_preview": conversation_summary[:400],
                }
            )
        else:
            # No conversation in events, use accumulated output
            conversation_summary = agent_output
            activity.logger.info(
                f"no_conversation_in_events_using_accumulated_output",
                extra={
                    "task_id": task.id,
                    "output_length": len(agent_output),
                }
            )

    # Use conversation summary for analysis
    analysis_text = conversation_summary

    activity.logger.info(
        "analyzing_task_completion_status",
        extra={
            "task_id": task.id,
            "task_title": task.title,
            "analysis_text_length": len(analysis_text),
            "analysis_text_preview": analysis_text[:300],
            "using_conversation_summary": bool(conversation_summary),
        }
    )

    try:
        # Build analysis prompt
        analysis_prompt = f"""Analyze this task execution to determine if the task is complete or if it needs user input to continue.

Task Requirement:
Title: {task.title}
Description: {task.description}
Details: {task.details}
Test Strategy: {task.test_strategy or 'Complete the task as described'}

Full Conversation for this Task:
{analysis_text[:10000] if analysis_text else 'No output available'}

Question: Looking at the FULL conversation above, did the agent complete the task requirement, or does it still need more user input?

Analyze the complete conversation flow:
1. What did the task require? (from Description and Details)
2. What has happened in the conversation so far?
3. Has the agent fulfilled the task requirement?
4. Is the LATEST agent message asking for NEW information, or just confirming completion?

Decision Rules:
- **CRITICAL: If the agent explicitly says "completed", "done", "finished" → task_complete=true**
- If the task said "ask user for X, then do Y" AND the conversation shows user provided X AND agent did Y → task_complete=true
- If the task said "ask user" AND agent asked AND user hasn't responded yet → needs_user_input=true
- If agent provided a result/answer that satisfies the task → task_complete=true
- If agent's latest message is asking for the FIRST TIME for input → needs_user_input=true
- If agent already got input and produced a result, even if asking again → task_complete=true (use the result before the repeat)
- **If agent's LAST message confirms completion (not asking a question) → task_complete=true**

Examples:
- Task: "Ask for number, calculate" | Conv: "ASSISTANT: What number? USER: 5 ASSISTANT: Result is 10" → task_complete=true (result: 10)
- Task: "Ask for input" | Conv: "ASSISTANT: What input?" → needs_user_input=true
- Task: "Generate random number" | Conv: "ASSISTANT: Generated 7" → task_complete=true

Respond with ONLY a JSON object (no markdown, no explanation):
{{
    "task_complete": true | false,
    "reasoning": "brief explanation of your determination",
    "confidence": 0.95,
    "needs_user_input": true | false,
    "user_question": "what the agent is asking for (if needs_user_input=true, otherwise null)"
}}

Guidelines:
- task_complete=true: The task requirement was satisfied, agent produced a result
- task_complete=false: The task is not complete yet
- needs_user_input=true: The agent is explicitly asking for user input/clarification
- needs_user_input=false: The task is complete or failed, no user input needed
"""

        # Use LiteLLM directly with metadata in request body
        litellm_api_base = os.getenv("LITELLM_API_BASE", "https://llm-proxy.kubiya.ai")
        litellm_api_key = os.getenv("LITELLM_API_KEY")
        model = "kubiya/claude-sonnet-4"

        # Build Langfuse metadata
        metadata_context = build_langfuse_metadata(
            plan_execution_id=plan_execution_id or "unknown",
            generation_name=f"task-{task.id}-completion-analysis",
            user_id=user_id,
            organization_id=organization_id,
            agent_id=task.agent_id,
            task_id=task.id,
        )

        # Format user for LiteLLM (format: email-org)
        user_field = None
        if user_id and organization_id:
            user_field = f"{user_id}-{organization_id}"

        activity.logger.info(
            "calling_llm_for_task_completion_analysis",
            extra={
                "task_id": task.id,
                "plan_execution_id": plan_execution_id[:8] if plan_execution_id else "unknown",
                "generation_name": metadata_context.get("generation_name"),
                "session_id": metadata_context.get("session_id"),
            }
        )

        async with httpx.AsyncClient(timeout=60.0) as client:
            request_body = {
                "model": model,
                "messages": [
                    {"role": "user", "content": analysis_prompt}
                ],
                "temperature": 0.0,
                "max_tokens": 500,
            }

            # DON'T add user field - Anthropic rejects emails!
            # LiteLLM will extract trace_user_id from metadata for Langfuse

            # Add metadata (LiteLLM extracts Langfuse fields from here)
            # CRITICAL: Don't include user_id in metadata - Anthropic rejects emails!
            # Only use trace_user_id which LiteLLM extracts for Langfuse
            request_body["metadata"] = {
                "trace_name": metadata_context.get("trace_name"),
                "generation_name": metadata_context.get("generation_name"),
                "trace_id": metadata_context.get("session_id"),
                "session_id": metadata_context.get("session_id"),
                "trace_user_id": user_field,  # For Langfuse only
                "organization_id": organization_id,
                "agent_id": metadata_context.get("agent_id"),
                "task_id": metadata_context.get("task_id"),
            }

            response = await client.post(
                f"{litellm_api_base}/v1/chat/completions",
                json=request_body,
                headers={
                    "Authorization": f"Bearer {litellm_api_key}",
                    "Content-Type": "application/json",
                }
            )

            if response.status_code != 200:
                raise Exception(f"LLM analysis failed: {response.status_code} - {response.text}")

            result = response.json()
            content = result['choices'][0]['message']['content']

            # Parse JSON response
            content = content.strip()
            if content.startswith('```'):
                content = content.split('```')[1]
                if content.startswith('json'):
                    content = content[4:]
            content = content.strip()

            analysis_data = json.loads(content)

            activity.logger.info(
                "task_completion_analysis_complete",
                extra={
                    "task_id": task.id,
                    "task_complete": analysis_data.get("task_complete"),
                    "needs_user_input": analysis_data.get("needs_user_input"),
                    "confidence": analysis_data.get("confidence"),
                    "reasoning": analysis_data.get("reasoning"),
                    "analyzed_text_preview": analysis_text[:200],
                }
            )

            return analysis_data

    except Exception as e:
        activity.logger.error(
            "task_completion_analysis_failed",
            extra={
                "task_id": task.id,
                "error": str(e),
                "litellm_api_base": os.getenv("LITELLM_API_BASE", "https://llm-proxy.kubiya.ai"),
                "has_api_key": bool(os.getenv("LITELLM_API_KEY")),
            }
        )
        # Re-raise the exception so we can see what's wrong
        raise Exception(f"Failed to analyze task completion for task {task.id}: {str(e)}") from e


@activity.defn
async def validate_task_completion(
    task: PlanTask,
    execution_result: TaskExecutionResult,
    plan_execution_id: Optional[str] = None,
    organization_id: Optional[str] = None,
    user_id: Optional[str] = None,
    jwt_token: Optional[str] = None,
) -> TaskValidationResult:
    """
    Validate task completion using LLM analysis.

    Analyzes the task output to determine if it actually completed successfully.
    """
    # Extract user_id from JWT if not provided
    if not user_id and jwt_token:
        user_id = extract_user_from_jwt(jwt_token)
    activity.logger.info(
        "validating_task",
        extra={
            "task_id": task.id,
            "task_title": task.title,
        }
    )

    try:
        # Build validation prompt
        validation_prompt = f"""Analyze this task execution and determine if it completed successfully.

Task: {task.title}

Description: {task.description}

Test Strategy: {task.test_strategy or 'Task should be completed as described'}

Task Output:
{execution_result.output[:2000] if execution_result.output else 'No output available'}

Execution Status: {execution_result.status}
{f"Error: {execution_result.error}" if execution_result.error else ""}

Respond with ONLY a JSON object (no markdown, no explanation):
{{
    "status": "success" | "failed" | "pending",
    "reason": "brief explanation of why you determined this status",
    "confidence": 0.95,
    "suggestions": "optional suggestions for improvement or next steps"
}}

Guidelines:
- "success": Task completed and output matches test strategy
- "failed": Task failed, errored, or output doesn't match requirements
- "pending": Task seems incomplete or needs clarification
"""

        # Use LiteLLM directly with metadata in request body
        litellm_api_base = os.getenv("LITELLM_API_BASE", "https://llm-proxy.kubiya.ai")
        litellm_api_key = os.getenv("LITELLM_API_KEY")
        model = "kubiya/claude-sonnet-4"

        # Build Langfuse metadata
        metadata_context = build_langfuse_metadata(
            plan_execution_id=plan_execution_id or "unknown",
            generation_name=f"task-{task.id}-validation",
            user_id=user_id,
            organization_id=organization_id,
            agent_id=task.agent_id,
            task_id=task.id,
        )

        # Format user for LiteLLM (format: email-org)
        user_field = None
        if user_id and organization_id:
            user_field = f"{user_id}-{organization_id}"

        activity.logger.info(
            "calling_llm_for_task_validation",
            extra={
                "task_id": task.id,
                "plan_execution_id": plan_execution_id[:8] if plan_execution_id else "unknown",
                "generation_name": metadata_context.get("generation_name"),
                "session_id": metadata_context.get("session_id"),
            }
        )

        async with httpx.AsyncClient(timeout=60.0) as client:
            request_body = {
                "model": model,
                "messages": [
                    {"role": "user", "content": validation_prompt}
                ],
                "temperature": 0.0,
                "max_tokens": 500,
            }

            # DON'T add user field - Anthropic rejects emails!
            # LiteLLM will extract trace_user_id from metadata for Langfuse

            # Add metadata (LiteLLM extracts Langfuse fields from here)
            # CRITICAL: Don't include user_id in metadata - Anthropic rejects emails!
            # Only use trace_user_id which LiteLLM extracts for Langfuse
            request_body["metadata"] = {
                "trace_name": metadata_context.get("trace_name"),
                "generation_name": metadata_context.get("generation_name"),
                "trace_id": metadata_context.get("session_id"),
                "session_id": metadata_context.get("session_id"),
                "trace_user_id": user_field,  # For Langfuse only
                "organization_id": organization_id,
                "agent_id": metadata_context.get("agent_id"),
                "task_id": metadata_context.get("task_id"),
            }

            response = await client.post(
                f"{litellm_api_base}/v1/chat/completions",
                json=request_body,
                headers={
                    "Authorization": f"Bearer {litellm_api_key}",
                    "Content-Type": "application/json",
                }
            )

            if response.status_code != 200:
                raise Exception(f"LLM validation failed: {response.status_code} - {response.text}")

            result = response.json()
            content = result['choices'][0]['message']['content']

            # Parse JSON response
            content = content.strip()
            if content.startswith('```'):
                content = content.split('```')[1]
                if content.startswith('json'):
                    content = content[4:]
            content = content.strip()

            validation_data = json.loads(content)

            # Map status string to TaskStatus enum
            status_map = {
                "success": TaskStatus.SUCCESS,
                "failed": TaskStatus.FAILED,
                "pending": TaskStatus.PENDING,
            }

            return TaskValidationResult(
                task_id=task.id,
                status=status_map.get(validation_data.get("status", "failed"), TaskStatus.FAILED),
                reason=validation_data.get("reason", "Validation completed"),
                confidence=validation_data.get("confidence", 0.5),
                suggestions=validation_data.get("suggestions"),
            )

    except Exception as e:
        activity.logger.error(
            "task_validation_failed",
            extra={
                "task_id": task.id,
                "error": str(e),
            }
        )

        # Default to success if validation fails
        return TaskValidationResult(
            task_id=task.id,
            status=TaskStatus.SUCCESS,
            reason=f"Validation failed, assuming success: {str(e)}",
            confidence=0.5,
        )


@activity.defn
async def continue_task_activity(
    task: PlanTask,
    execution_id: str,
    user_message: str,
    plan_execution_id: str,
    jwt_token: Optional[str] = None,
    model_id: Optional[str] = None,
    organization_id: Optional[str] = None,
) -> TaskExecutionResult:
    """
    Continue a task execution after user provides input.

    This sends the user's message to the existing agent execution,
    then continues streaming events until the task completes or needs more input.
    """
    activity.logger.info(
        "continuing_task_execution",
        extra={
            "task_id": task.id,
            "execution_id": execution_id,
            "plan_execution_id": plan_execution_id[:8],
            "message_preview": user_message[:100],
        }
    )

    started_at = datetime.now(timezone.utc)

    try:
        control_plane_url = get_control_plane_url()

        async with httpx.AsyncClient(timeout=600.0) as client:
            # Step 1: Send user message to continue conversation (only if message provided)
            if user_message:
                message_response = await client.post(
                    f"{control_plane_url}/api/v1/executions/{execution_id}/message",
                    json={"message": user_message},
                    headers=get_auth_headers(jwt_token),
                )

                if message_response.status_code not in (200, 201, 202):
                    raise Exception(f"Failed to send message: {message_response.text}")

                activity.logger.info(
                    f"user_message_sent_to_execution: execution_id={execution_id}"
                )
            else:
                activity.logger.info(
                    f"skipping_message_send_already_sent_by_api: execution_id={execution_id}"
                )

            # Step 2: Continue streaming from the execution
            final_status = None
            final_output = ""
            final_tokens = 0
            final_cost = 0.0
            final_error = None
            all_events = []
            seen_events_after_message = False  # Track if we've seen NEW events after sending message

            async with client.stream(
                "GET",
                f"{control_plane_url}/api/v1/executions/{execution_id}/stream",
                headers=get_auth_headers(jwt_token),
                timeout=600.0,
            ) as stream_response:
                if stream_response.status_code not in (200, 201):
                    raise Exception(f"Failed to stream execution: {stream_response.status_code}")

                current_event = None
                async for line in stream_response.aiter_lines():
                    if not line:
                        continue

                    # Parse SSE format
                    if line.startswith("event: "):
                        current_event = line[7:]
                        continue

                    if line.startswith("data: "):
                        try:
                            data = json.loads(line[6:])
                            status = data.get("status")

                            # Check if this is a NEW event (after our message was sent)
                            event_timestamp = data.get("timestamp", "")
                            if event_timestamp and event_timestamp > started_at.isoformat():
                                seen_events_after_message = True

                            all_events.append({
                                "event": current_event,
                                "data": data,
                                "timestamp": data.get("timestamp", datetime.now(timezone.utc).isoformat())
                            })

                            activity.logger.info(
                                f"stream_event: event={current_event}, status={status}, task_id={task.id}, new={seen_events_after_message}"
                            )

                            # Check for completion (but ignore old waiting_for_input status)
                            if current_event == "status" and status:
                                # During continuation, ignore waiting_for_input unless we've seen new events
                                # This prevents breaking on old cached status
                                if status in ("completed", "success", "failed", "error"):
                                    final_status = status
                                    activity.logger.info(
                                        f"task_continuation_complete: status={final_status}, task_id={task.id}"
                                    )
                                    break
                                elif status == "waiting_for_input" and seen_events_after_message:
                                    # Agent needs MORE input after our message
                                    final_status = status
                                    activity.logger.info(
                                        f"task_needs_more_input: status={final_status}, task_id={task.id}"
                                    )
                                    break

                            # Track assistant messages
                            if current_event in ("message", "message_chunk"):
                                msg_data = data.get("data", {})
                                role = msg_data.get("role", data.get("role"))
                                content = msg_data.get("content", data.get("content", ""))

                                if role == "assistant" and content and content != "(no content)":
                                    final_output += content

                        except json.JSONDecodeError:
                            continue

            # Analyze completion status
            completed_at = datetime.now(timezone.utc)

            if final_status in ("completed", "success"):
                task_status = TaskStatus.SUCCESS
                needs_continuation = False
                user_question = None

            elif final_status == "waiting_for_input":
                # Use LLM analysis again
                activity.logger.info(
                    f"re_analyzing_after_user_input: task_id={task.id}, analyzing continuation result"
                )
                analysis = await analyze_task_completion_status(
                    task,
                    final_output,
                    all_events,
                    plan_execution_id=plan_execution_id,
                    organization_id=organization_id,
                    user_id=None,
                    jwt_token=jwt_token,
                )

                if analysis.get("task_complete", False):
                    task_status = TaskStatus.SUCCESS
                    needs_continuation = False
                    user_question = None
                    activity.logger.info(
                        f"task_complete_after_user_input: task_id={task.id}"
                    )
                else:
                    # Task still needs more input
                    task_status = TaskStatus.WAITING_FOR_INPUT
                    needs_continuation = True
                    user_question = analysis.get("user_question")
                    activity.logger.info(
                        f"task_still_needs_input: task_id={task.id}, question={user_question}"
                    )

            else:
                task_status = TaskStatus.FAILED
                needs_continuation = False
                user_question = None

            # Publish completion events (same as execute_task_activity)
            if task_status == TaskStatus.WAITING_FOR_INPUT:
                await publish_plan_event(
                    execution_id=plan_execution_id,
                    event_type="task_waiting_for_input",
                    event_data=TaskWaitingForInputEvent(
                        execution_id=plan_execution_id,
                        task_id=task.id,
                        question=user_question or "Waiting for user input",
                        task_execution_id=execution_id,
                    )
                )
                await publish_plan_event(
                    execution_id=plan_execution_id,
                    event_type="todo_item_updated",
                    event_data=TodoItemUpdatedEvent(
                        execution_id=plan_execution_id,
                        task_id=task.id,
                        title=task.title,
                        old_status="running",
                        new_status="waiting_for_input",
                        message=user_question or "Waiting for user input",
                    )
                )
            else:
                # Task completed (success or failed)
                await publish_plan_event(
                    execution_id=plan_execution_id,
                    event_type="task_completed",
                    event_data=TaskCompletedEvent(
                        execution_id=plan_execution_id,
                        task_id=task.id,
                        title=task.title,
                        status="success" if task_status == TaskStatus.SUCCESS else "failed",
                        output=final_output[:500] if final_output else "",
                        error=final_error,
                        tokens=final_tokens,
                        cost=final_cost,
                    )
                )
                await publish_plan_event(
                    execution_id=plan_execution_id,
                    event_type="todo_item_updated",
                    event_data=TodoItemUpdatedEvent(
                        execution_id=plan_execution_id,
                        task_id=task.id,
                        title=task.title,
                        old_status="waiting_for_input",  # Was waiting, now completing
                        new_status="completed" if task_status == TaskStatus.SUCCESS else "failed",
                        message=f"Task {'completed successfully' if task_status == TaskStatus.SUCCESS else 'failed'}",
                    )
                )

            return TaskExecutionResult(
                task_id=task.id,
                status=task_status,
                execution_id=execution_id,
                output=final_output,
                events=all_events,
                tokens=final_tokens,
                cost=final_cost,
                started_at=started_at,
                completed_at=completed_at,
                error=final_error,
                needs_continuation=needs_continuation,
                user_question=user_question,
            )

    except Exception as e:
        activity.logger.error(
            "continue_task_failed",
            extra={
                "task_id": task.id,
                "execution_id": execution_id,
                "error": str(e),
            }
        )

        return TaskExecutionResult(
            task_id=task.id,
            status=TaskStatus.FAILED,
            execution_id=execution_id,
            output="",
            events=[],
            tokens=0,
            cost=0.0,
            started_at=started_at,
            completed_at=datetime.now(timezone.utc),
            error=str(e),
            needs_continuation=False,
            user_question=None,
        )


@activity.defn
async def get_task_status_activity(
    task_id: int,
    task_results: Dict[int, TaskExecutionResult],
) -> Dict[str, Any]:
    """Get the current status of a task."""
    if task_id in task_results:
        result = task_results[task_id]
        return {
            "found": True,
            "status": result.status.value,
            "output": result.output,
            "tokens": result.tokens,
            "cost": result.cost,
            "error": result.error,
        }
    else:
        return {
            "found": False,
            "status": "pending",
        }


@activity.defn
async def call_llm_activity(
    messages: List[Dict[str, Any]],
    system_prompt: str,
    tools: List[Dict[str, Any]],
    model_id: str,
    plan_execution_id: Optional[str] = None,
    organization_id: Optional[str] = None,
    user_id: Optional[str] = None,
    task_id: Optional[int] = None,
    generation_name: Optional[str] = None,
    jwt_token: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Activity to call Anthropic API directly (like Claude Code runtime does).

    This activity now includes Langfuse metadata for proper observability.
    """
    # Extract user_id from JWT if not provided
    if not user_id and jwt_token:
        user_id = extract_user_from_jwt(jwt_token)

    activity.logger.info(
        "calling_anthropic_api",
        model=model_id,
        message_count=len(messages),
        tool_count=len(tools),
        plan_execution_id=plan_execution_id[:8] if plan_execution_id else "unknown",
    )

    try:
        # Use httpx directly to have full control over request with metadata
        litellm_api_base = os.getenv("LITELLM_API_BASE", "https://llm-proxy.kubiya.ai")
        litellm_api_key = os.getenv("LITELLM_API_KEY")

        # Build Langfuse metadata
        metadata_context = build_langfuse_metadata(
            plan_execution_id=plan_execution_id or "unknown",
            generation_name=generation_name or "plan-orchestrator-llm-call",
            user_id=user_id,
            organization_id=organization_id,
            task_id=task_id,
        )

        # Format user for LiteLLM (format: email-org)
        user_field = None
        if user_id and organization_id:
            user_field = f"{user_id}-{organization_id}"

        activity.logger.info(
            "calling_anthropic_with_metadata",
            extra={
                "plan_execution_id": plan_execution_id[:8] if plan_execution_id else "unknown",
                "generation_name": metadata_context.get("generation_name"),
                "session_id": metadata_context.get("session_id"),
            }
        )

        # Build request body in Anthropic format with metadata
        request_body = {
            "model": model_id,
            "max_tokens": 4096,
            "system": system_prompt,
            "messages": messages,
            "tools": tools,
            "temperature": 0.0,
        }

        # DON'T add user field - Anthropic rejects emails!
        # LiteLLM will extract trace_user_id from metadata for Langfuse

        # Add metadata (LiteLLM extracts Langfuse fields from here)
        # CRITICAL: Don't include user_id - Anthropic rejects emails!
        request_body["metadata"] = {
            "trace_name": metadata_context.get("trace_name"),
            "generation_name": metadata_context.get("generation_name"),
            "trace_id": metadata_context.get("session_id"),
            "session_id": metadata_context.get("session_id"),
            "trace_user_id": user_field,  # For Langfuse only
            "organization_id": organization_id,
            "agent_id": metadata_context.get("agent_id"),
            "task_id": metadata_context.get("task_id"),
        }

        async with httpx.AsyncClient(timeout=300.0) as http_client:
            response = await http_client.post(
                f"{litellm_api_base}/v1/messages",
                json=request_body,
                headers={
                    "Authorization": f"Bearer {litellm_api_key}",
                    "Content-Type": "application/json",
                    "anthropic-version": "2023-06-01",
                },
            )

            if response.status_code != 200:
                raise Exception(f"Anthropic API call failed: {response.status_code} - {response.text}")

            result = response.json()

            # Extract tool calls from response
            tool_calls = []
            content_text = ""

            for block in result.get("content", []):
                if block.get("type") == "text":
                    content_text = block.get("text", "")
                elif block.get("type") == "tool_use":
                    tool_calls.append({
                        "id": block.get("id"),
                        "name": block.get("name"),
                        "input": block.get("input", {}),
                    })

            activity.logger.info(
                "anthropic_call_complete",
                tool_calls_count=len(tool_calls),
            )

            return {
                "content": content_text,
                "tool_calls": tool_calls,
            }

    except Exception as e:
        activity.logger.error(f"anthropic_call_failed: {str(e)}")
        raise
