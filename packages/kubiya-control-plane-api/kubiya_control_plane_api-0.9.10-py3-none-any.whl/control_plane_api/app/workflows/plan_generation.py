"""Plan generation workflow for Temporal"""

from dataclasses import dataclass, field
from datetime import timedelta
from typing import Optional, Dict, Any, List
from temporalio import workflow
from temporalio.common import RetryPolicy
import asyncio

with workflow.unsafe.imports_passed_through():
    from control_plane_api.app.activities.plan_generation_activities import (
        generate_plan_activity,
        store_plan_activity,
        update_plan_generation_status,
        ActivityGeneratePlanInput,
        ActivityStorePlanInput,
        ActivityUpdatePlanGenerationInput,
    )


@dataclass
class PlanGenerationInput:
    """Input for plan generation workflow"""
    execution_id: str
    organization_id: str
    task_request: Dict[str, Any]  # TaskPlanRequest as dict (for serialization)
    user_metadata: Optional[Dict[str, Any]] = None
    api_token: Optional[str] = None  # API token for accessing resources

    def __post_init__(self):
        if self.user_metadata is None:
            self.user_metadata = {}


@dataclass
class PlanGenerationState:
    """Current state of plan generation for queries"""
    status: str  # "pending", "analyzing", "generating", "completed", "failed"
    current_step: str = ""
    error_message: Optional[str] = None
    plan_json: Optional[Dict[str, Any]] = None
    progress_percentage: int = 0

    def to_dict(self) -> Dict[str, Any]:
        """Convert state to dict for serialization"""
        return {
            "status": self.status,
            "current_step": self.current_step,
            "error_message": self.error_message,
            "plan_json": self.plan_json,
            "progress_percentage": self.progress_percentage,
        }


@workflow.defn
class PlanGenerationWorkflow:
    """
    Workflow for generating a task plan asynchronously.

    This workflow:
    1. Updates execution status to running
    2. Generates the plan using the planning strategy
    3. Stores the generated plan in the execution record
    4. Updates execution with results
    5. Supports queries for real-time state access
    """

    def __init__(self) -> None:
        """Initialize workflow state"""
        self._state = PlanGenerationState(status="pending")
        self._lock = asyncio.Lock()

    @workflow.query
    def get_state(self) -> PlanGenerationState:
        """Query handler: Get current plan generation state"""
        return self._state

    @workflow.run
    async def run(self, input: PlanGenerationInput) -> Dict[str, Any]:
        """
        Run the plan generation workflow.

        Args:
            input: Workflow input with plan generation details

        Returns:
            Result dict with generated plan and metadata
        """
        workflow.logger.info(
            f"Starting plan generation workflow",
            extra={
                "execution_id": input.execution_id,
                "organization_id": input.organization_id,
                "quick_mode": input.task_request.get("quick_mode", False),
            }
        )

        try:
            # Step 1: Update execution status to running
            async with self._lock:
                self._state.status = "running"
                self._state.current_step = "Initializing plan generation"
                self._state.progress_percentage = 10

            await workflow.execute_activity(
                update_plan_generation_status,
                ActivityUpdatePlanGenerationInput(
                    execution_id=input.execution_id,
                    status="running",
                    current_step="Initializing plan generation",
                ),
                start_to_close_timeout=timedelta(seconds=30),
                retry_policy=RetryPolicy(
                    maximum_attempts=3,
                    initial_interval=timedelta(seconds=1),
                    maximum_interval=timedelta(seconds=10),
                ),
            )

            # Step 2: Analyze and generate plan
            async with self._lock:
                self._state.status = "analyzing"
                self._state.current_step = "Analyzing task requirements"
                self._state.progress_percentage = 30

            await workflow.execute_activity(
                update_plan_generation_status,
                ActivityUpdatePlanGenerationInput(
                    execution_id=input.execution_id,
                    status="analyzing",
                    current_step="Analyzing task requirements",
                ),
                start_to_close_timeout=timedelta(seconds=30),
            )

            # Generate the plan (this is the long-running step: 1-3 minutes)
            async with self._lock:
                self._state.status = "generating"
                self._state.current_step = "Generating execution plan"
                self._state.progress_percentage = 50

            await workflow.execute_activity(
                update_plan_generation_status,
                ActivityUpdatePlanGenerationInput(
                    execution_id=input.execution_id,
                    status="generating",
                    current_step="Generating execution plan",
                ),
                start_to_close_timeout=timedelta(seconds=30),
            )

            workflow.logger.info("Executing plan generation activity")
            plan_result = await workflow.execute_activity(
                generate_plan_activity,
                ActivityGeneratePlanInput(
                    execution_id=input.execution_id,
                    organization_id=input.organization_id,
                    task_request=input.task_request,
                    api_token=input.api_token,
                ),
                start_to_close_timeout=timedelta(minutes=10),  # Plan generation can take 1-3 minutes, allow extra buffer
                # No heartbeat timeout - plan generation is a long-running operation
                retry_policy=RetryPolicy(
                    maximum_attempts=2,
                    initial_interval=timedelta(seconds=5),
                    maximum_interval=timedelta(seconds=30),
                ),
            )

            async with self._lock:
                self._state.plan_json = plan_result.get("plan_json")
                self._state.progress_percentage = 80

            workflow.logger.info("Plan generated successfully")

            # Step 3: Store the plan
            async with self._lock:
                self._state.current_step = "Storing generated plan"
                self._state.progress_percentage = 90

            await workflow.execute_activity(
                store_plan_activity,
                ActivityStorePlanInput(
                    execution_id=input.execution_id,
                    plan_json=plan_result["plan_json"],
                    metadata=plan_result.get("metadata", {}),
                ),
                start_to_close_timeout=timedelta(seconds=30),
                retry_policy=RetryPolicy(
                    maximum_attempts=3,
                    initial_interval=timedelta(seconds=1),
                    maximum_interval=timedelta(seconds=10),
                ),
            )

            workflow.logger.info("Plan stored successfully")

            # Step 4: Mark as completed
            async with self._lock:
                self._state.status = "completed"
                self._state.current_step = "Plan generation complete"
                self._state.progress_percentage = 100

            await workflow.execute_activity(
                update_plan_generation_status,
                ActivityUpdatePlanGenerationInput(
                    execution_id=input.execution_id,
                    status="completed",
                    current_step="Plan generation complete",
                    plan_json=plan_result["plan_json"],
                ),
                start_to_close_timeout=timedelta(seconds=30),
            )

            workflow.logger.info(
                "Plan generation workflow completed successfully",
                extra={"execution_id": input.execution_id}
            )

            return {
                "status": "completed",
                "plan_json": plan_result["plan_json"],
                "metadata": plan_result.get("metadata", {}),
            }

        except Exception as e:
            workflow.logger.error(
                f"Plan generation workflow failed: {str(e)}",
                extra={"execution_id": input.execution_id},
                exc_info=True,
            )

            async with self._lock:
                self._state.status = "failed"
                self._state.error_message = str(e)

            # Update execution status to failed
            try:
                await workflow.execute_activity(
                    update_plan_generation_status,
                    ActivityUpdatePlanGenerationInput(
                        execution_id=input.execution_id,
                        status="failed",
                        error_message=str(e),
                    ),
                    start_to_close_timeout=timedelta(seconds=30),
                )
            except Exception as update_error:
                workflow.logger.error(f"Failed to update error status: {str(update_error)}")

            return {
                "status": "failed",
                "error": str(e),
            }
