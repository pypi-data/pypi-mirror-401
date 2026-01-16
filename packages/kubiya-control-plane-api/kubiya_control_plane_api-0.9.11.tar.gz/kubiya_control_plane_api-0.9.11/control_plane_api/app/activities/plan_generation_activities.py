"""Activities for plan generation workflow"""

from dataclasses import dataclass
from typing import Optional, List, Dict, Any
from temporalio import activity
import structlog
import httpx
import os
import json
from datetime import datetime
from sqlalchemy.orm import Session

from control_plane_api.app.database import get_db
from control_plane_api.app.models.execution import Execution, ExecutionStatus
from control_plane_api.app.models.task_planning import TaskPlanRequest
from control_plane_api.app.services.plan_generator import generate_plan

logger = structlog.get_logger()


async def publish_event_to_api(execution_id: str, event_type: str, data: Dict[str, Any], api_token: Optional[str] = None) -> bool:
    """
    Publish event via Control Plane API (which handles Redis internally).
    Same pattern as plan execution activities.
    """
    try:
        control_plane_url = os.getenv("CONTROL_PLANE_URL", "http://localhost:8000")

        # Get API token from environment if not provided
        if not api_token:
            api_token = os.getenv("KUBIYA_API_KEY")

        message = {
            "event_type": event_type,
            "data": data,
            "timestamp": datetime.utcnow().isoformat(),
        }

        headers = {}
        if api_token:
            headers["Authorization"] = f"Bearer {api_token}"

        logger.info(
            "🔍 DEBUG: publishing_event_to_api",
            execution_id=execution_id[:12],
            event_type=event_type,
            url=f"{control_plane_url}/api/v1/executions/{execution_id}/events",
            has_auth=bool(api_token),
            token_preview=api_token[:20] if api_token else None
        )

        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.post(
                f"{control_plane_url}/api/v1/executions/{execution_id}/events",
                json=message,
                headers=headers,
            )

            if response.status_code in (200, 201, 202):
                logger.info(
                    "✅ DEBUG: event_published_successfully",
                    execution_id=execution_id[:12],
                    event_type=event_type,
                    status_code=response.status_code
                )
                return True
            else:
                logger.error(
                    "❌ DEBUG: event_publish_failed",
                    execution_id=execution_id[:12],
                    event_type=event_type,
                    status=response.status_code,
                    response_text=response.text[:200]
                )
                return False

    except Exception as e:
        logger.error(
            "❌ DEBUG: event_publish_exception",
            execution_id=execution_id[:12],
            event_type=event_type,
            error=str(e),
            error_type=type(e).__name__
        )
        return False


@dataclass
class ActivityGeneratePlanInput:
    """Input for generate_plan_activity"""
    execution_id: str
    organization_id: str
    task_request: Dict[str, Any]  # TaskPlanRequest as dict
    api_token: Optional[str] = None


@dataclass
class ActivityStorePlanInput:
    """Input for store_plan_activity"""
    execution_id: str
    plan_json: Dict[str, Any]
    metadata: Dict[str, Any]


@dataclass
class ActivityUpdatePlanGenerationInput:
    """Input for update_plan_generation_status activity"""
    execution_id: str
    status: str
    current_step: Optional[str] = None
    error_message: Optional[str] = None
    plan_json: Optional[Dict[str, Any]] = None


async def _publish_event_async(execution_id: str, event_type: str, data: Dict[str, Any], api_token: Optional[str] = None):
    """Publish event via Control Plane API (which handles Redis)."""
    await publish_event_to_api(execution_id, event_type, data, api_token)


@activity.defn
async def generate_plan_activity(input: ActivityGeneratePlanInput) -> Dict[str, Any]:
    """
    Generate a plan using the existing planning workflow infrastructure.

    This activity wraps the existing Agno-based planning workflow to run
    asynchronously in a Temporal activity.
    """
    # Reconstruct TaskPlanRequest from dict
    task_request = TaskPlanRequest(**input.task_request)

    activity.logger.info(
        f"Starting plan generation",
        extra={
            "execution_id": input.execution_id,
            "organization_id": input.organization_id,
            "description": task_request.description[:100],
            "quick_mode": task_request.quick_mode,
        }
    )

    try:
        # Create database session
        db = next(get_db())

        # Publish metadata event first (helps streaming endpoint identify execution type)
        await publish_event_to_api(
            input.execution_id,
            "metadata",
            {
                "execution_type": "PLAN_GENERATION",
                "organization_id": input.organization_id,
                "started_at": datetime.utcnow().isoformat(),
            },
            api_token=input.api_token
        )

        # Publish progress event (with auth token)
        await publish_event_to_api(
            input.execution_id,
            "progress",
            {
                "status": "analyzing",
                "message": "Analyzing task requirements",
                "progress_percentage": 30,
            },
            api_token=input.api_token
        )

        # Send heartbeat
        activity.heartbeat("Generating plan")

        # Event publisher for streaming
        def publish_event(event_data: Dict[str, Any]):
            """Callback to publish intermediate events during plan generation"""
            try:
                event_type = event_data.get("event", "progress")
                data = event_data.get("data", {})

                # For thinking events with large content, split into chunks for better UX
                if event_type == "thinking" and isinstance(data.get("content"), str):
                    content = data["content"]
                    chunk_size = 500  # Characters per chunk

                    if len(content) > chunk_size:
                        activity.logger.debug(
                            "chunking_thinking_event",
                            execution_id=input.execution_id[:12],
                            content_length=len(content),
                            num_chunks=(len(content) // chunk_size) + 1
                        )

                        # Send thinking in chunks
                        for i in range(0, len(content), chunk_size):
                            chunk = content[i:i + chunk_size]
                            chunk_data = {
                                **data,
                                "content": chunk,
                                "is_chunk": True,
                                "chunk_index": i // chunk_size,
                                "is_final_chunk": i + chunk_size >= len(content)
                            }

                            chunk_message = {
                                "event_type": "thinking",
                                "data": chunk_data,
                                "timestamp": datetime.utcnow().isoformat(),
                            }

                            headers = {}
                            if input.api_token:
                                headers["Authorization"] = f"Bearer {input.api_token}"

                            control_plane_url = os.getenv("CONTROL_PLANE_URL", "http://localhost:8000")
                            with httpx.Client(timeout=5.0) as client:
                                client.post(
                                    f"{control_plane_url}/api/v1/executions/{input.execution_id}/events",
                                    json=chunk_message,
                                    headers=headers,
                                )

                        activity.heartbeat(f"Planning: thinking (chunked)")
                        return  # Don't send the full event

                # Publish normally for non-thinking or small thinking events
                control_plane_url = os.getenv("CONTROL_PLANE_URL", "http://localhost:8000")

                message = {
                    "event_type": event_type,
                    "data": data,
                    "timestamp": datetime.utcnow().isoformat(),
                }

                headers = {}
                if input.api_token:
                    headers["Authorization"] = f"Bearer {input.api_token}"

                # Use sync httpx client since this is called from sync context
                with httpx.Client(timeout=5.0) as client:
                    response = client.post(
                        f"{control_plane_url}/api/v1/executions/{input.execution_id}/events",
                        json=message,
                        headers=headers,
                    )

                    if response.status_code in (200, 201, 202):
                        activity.logger.debug(
                            f"event_published_from_callback: {event_type}",
                            extra={
                                "execution_id": input.execution_id[:12],
                                "event_type": event_type,
                            },
                        )
                    else:
                        activity.logger.warning(
                            f"event_publish_failed_from_callback: {event_type}",
                            extra={
                                "execution_id": input.execution_id[:12],
                                "event_type": event_type,
                                "status": response.status_code,
                            },
                        )

                activity.heartbeat(f"Planning: {event_type}")
            except Exception as e:
                activity.logger.error(
                    f"failed_to_publish_event_from_callback: {str(e)}",
                    extra={
                        "error_type": type(e).__name__,
                        "execution_id": input.execution_id[:12]
                    },
                )

        # Use shared plan generation service (same code as /plan/stream)
        plan = await generate_plan(
            request=task_request,
            organization_id=input.organization_id,
            api_token=input.api_token,
            db=db,
            event_callback=publish_event,
        )

        # Calculate total tasks from team_breakdown
        total_tasks = sum(len(team.tasks) for team in plan.team_breakdown) if plan.team_breakdown else 0

        activity.logger.info(
            f"Plan generation completed",
            extra={
                "execution_id": input.execution_id,
                "plan_title": plan.title,
                "total_tasks": total_tasks,
            }
        )

        # Convert plan to dict
        plan_dict = plan.model_dump()

        # Publish final progress event
        await publish_event_to_api(
            input.execution_id,
            "progress",
            {
                "status": "completed",
                "message": "Plan generation complete",
                "progress_percentage": 100,
            },
            api_token=input.api_token
        )

        # Publish complete event with plan (matching /plan/stream behavior)
        await publish_event_to_api(
            input.execution_id,
            "complete",
            {
                "plan": plan_dict,
                "progress": 100,
                "message": "✅ Plan generated successfully!",
            },
            api_token=input.api_token
        )

        # Publish done event to signal stream completion
        await publish_event_to_api(
            input.execution_id,
            "done",
            {
                "message": "Plan generation workflow completed",
                "execution_id": input.execution_id,
            },
            api_token=input.api_token
        )

        return {
            "plan_json": plan_dict,
            "metadata": {
                "total_tasks": total_tasks,
                "quick_mode": task_request.quick_mode,
                "generated_at": datetime.utcnow().isoformat(),
            },
        }

    except Exception as e:
        activity.logger.error(
            f"Plan generation failed: {str(e)}",
            extra={"execution_id": input.execution_id},
            exc_info=True,
        )

        # Publish error event
        await publish_event_to_api(
            input.execution_id,
            "error",
            {
                "error": str(e),
                "message": "Plan generation failed",
            },
            api_token=input.api_token
        )

        raise


@activity.defn
async def store_plan_activity(input: ActivityStorePlanInput) -> None:
    """
    Store the generated plan in the execution record.
    """
    activity.logger.info(
        f"Storing plan",
        extra={
            "execution_id": input.execution_id,
        }
    )

    try:
        # Create database session
        db = next(get_db())

        # Update execution with plan JSON
        execution = db.query(Execution).filter(
            Execution.id == input.execution_id
        ).first()

        if not execution:
            raise ValueError(f"Execution {input.execution_id} not found")

        execution.plan_json = input.plan_json
        execution.execution_metadata = {
            **(execution.execution_metadata or {}),
            **input.metadata,
        }
        execution.response = input.plan_json.get("title", "Plan generated")
        execution.status = ExecutionStatus.COMPLETED.value
        execution.completed_at = datetime.utcnow()

        db.commit()

        activity.logger.info(f"Plan stored successfully", extra={"execution_id": input.execution_id})

        # Publish plan stored event
        await publish_event_to_api(
            input.execution_id,
            "plan_stored",
            {
                "message": "Plan stored successfully",
                "plan_title": input.plan_json.get("title", "Untitled Plan"),
            },
            api_token=os.getenv("KUBIYA_API_KEY")
        )

    except Exception as e:
        activity.logger.error(
            f"Failed to store plan: {str(e)}",
            extra={"execution_id": input.execution_id},
            exc_info=True,
        )
        raise


@activity.defn
async def update_plan_generation_status(input: ActivityUpdatePlanGenerationInput) -> None:
    """
    Update the execution status for plan generation.
    """
    activity.logger.info(
        f"Updating plan generation status",
        extra={
            "execution_id": input.execution_id,
            "status": input.status,
        }
    )

    try:
        # Create database session
        db = next(get_db())

        # Update execution status
        execution = db.query(Execution).filter(
            Execution.id == input.execution_id
        ).first()

        if not execution:
            raise ValueError(f"Execution {input.execution_id} not found")

        # Map plan generation status to execution status
        status_mapping = {
            "pending": ExecutionStatus.PENDING,
            "running": ExecutionStatus.RUNNING,
            "analyzing": ExecutionStatus.RUNNING,
            "generating": ExecutionStatus.RUNNING,
            "completed": ExecutionStatus.COMPLETED,
            "failed": ExecutionStatus.FAILED,
        }

        execution.status = status_mapping.get(input.status, ExecutionStatus.RUNNING).value

        if input.error_message:
            execution.error_message = input.error_message

        if input.current_step:
            execution.execution_metadata = {
                **(execution.execution_metadata or {}),
                "current_step": input.current_step,
            }

        if input.plan_json:
            execution.plan_json = input.plan_json

        if input.status == "running" and not execution.started_at:
            execution.started_at = datetime.utcnow()

        if input.status in ["completed", "failed"]:
            execution.completed_at = datetime.utcnow()

        db.commit()

        activity.logger.info(
            f"Plan generation status updated",
            extra={"execution_id": input.execution_id, "status": input.status}
        )

        # Publish status update event
        await publish_event_to_api(
            input.execution_id,
            "status",
            {
                "status": input.status,
                "current_step": input.current_step,
                "error_message": input.error_message,
            },
            api_token=os.getenv("KUBIYA_API_KEY")
        )

    except Exception as e:
        activity.logger.error(
            f"Failed to update plan generation status: {str(e)}",
            extra={"execution_id": input.execution_id},
            exc_info=True,
        )
        raise
