"""Async Plan Generation Router - AI-powered task planning with Temporal"""

from fastapi import APIRouter, HTTPException, status, Depends, Request
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
import structlog
import uuid
import os
from datetime import datetime
from temporalio.client import Client as TemporalClient
import httpx

from control_plane_api.app.database import get_db
from control_plane_api.app.middleware.auth import get_current_organization
from control_plane_api.app.models.execution import Execution, ExecutionType, ExecutionStatus, ExecutionTriggerSource
from control_plane_api.app.models.associations import ExecutionParticipant, ParticipantRole
from control_plane_api.app.models.task_planning import TaskPlanRequest
from control_plane_api.app.workflows.plan_generation import PlanGenerationWorkflow, PlanGenerationInput
from control_plane_api.app.lib.task_planning.helpers import _extract_organization_id_from_token

router = APIRouter()
logger = structlog.get_logger()


class PlanGenerationResponse(BaseModel):
    """Response model for async plan generation"""
    execution_id: str = Field(..., description="Unique execution identifier")
    workflow_id: str = Field(..., description="Temporal workflow identifier")
    status: str = Field(..., description="Current execution status")
    message: str = Field(..., description="Human-readable status message")


@router.post("/plans/generate", response_model=PlanGenerationResponse)
async def generate_plan_async(
    plan_request: TaskPlanRequest,  # Same as /plan/stream
    request: Request,
    organization: dict = Depends(get_current_organization),
    db: Session = Depends(get_db),
):
    """
    Generate a task plan asynchronously using Temporal workflow.

    This endpoint:
    1. Creates an execution record in the database
    2. Submits a Temporal workflow for plan generation
    3. Returns execution_id for tracking progress
    4. Client can stream results via /api/v1/executions/{execution_id}/stream

    Flow:
    1. POST /api/v1/plans/generate → get execution_id
    2. GET /api/v1/executions/{execution_id}/stream → stream progress and final plan
    3. Use plan from execution.plan_json with existing /api/v1/tasks/plan/execute

    Benefits:
    - Non-blocking: API responds immediately
    - Progress tracking: Stream real-time updates
    - Persistence: Plan stored in DB for later execution
    - Resilient: Temporal handles retries and failures
    """
    try:
        logger.info(
            "async_plan_generation_requested",
            description=plan_request.description[:100],
            organization_id=organization["id"],
            quick_mode=plan_request.quick_mode,
        )

        # Extract API token from Authorization header
        auth_header = request.headers.get("authorization", "")
        api_token = auth_header.replace("UserKey ", "").replace("Bearer ", "") if auth_header else None

        if not api_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication required: No API token provided"
            )

        # Validate organization ID from token
        try:
            token_org_id = _extract_organization_id_from_token(api_token)
            if token_org_id != organization["id"]:
                raise ValueError("Token organization mismatch")
        except Exception as e:
            logger.error("token_validation_failed", error=str(e))
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Authentication failed: {str(e)}"
            )

        # Create execution record
        execution_id = uuid.uuid4()
        now = datetime.utcnow()

        # Extract user metadata from organization (JWT)
        user_metadata = {}
        user_metadata["user_id"] = organization.get("user_id")
        user_metadata["user_email"] = organization.get("user_email")
        user_metadata["user_name"] = organization.get("user_name")
        user_metadata["user_avatar"] = None

        execution = Execution(
            id=execution_id,
            organization_id=organization["id"],
            execution_type=ExecutionType.PLAN_GENERATION.value,
            entity_id=execution_id,  # For plan generation, entity_id = execution_id
            entity_name="Plan Generation",
            runner_name="plan-generator",  # Static runner name for plan generation
            prompt=plan_request.description,
            system_prompt=None,
            status=ExecutionStatus.PENDING.value,
            trigger_source=ExecutionTriggerSource.USER,
            user_id=user_metadata.get("user_id"),
            user_name=user_metadata.get("user_name"),
            user_email=user_metadata.get("user_email"),
            user_avatar=user_metadata.get("user_avatar"),
            usage={},
            execution_metadata={
                "quick_mode": plan_request.quick_mode,
                "priority": plan_request.priority,
                "planning_strategy": plan_request.planning_strategy,
                "kubiya_org_id": organization["id"],
                "kubiya_org_name": organization.get("name"),
            },
            created_at=now,
            updated_at=now,
        )

        db.add(execution)
        db.commit()
        db.refresh(execution)

        logger.info(
            "plan_generation_execution_created",
            execution_id=str(execution_id),
            organization_id=organization["id"],
        )

        # Add creator as owner participant
        user_id = user_metadata.get("user_id")
        if user_id:
            try:
                participant = ExecutionParticipant(
                    id=uuid.uuid4(),
                    execution_id=execution_id,
                    organization_id=organization["id"],
                    user_id=user_id,
                    user_name=user_metadata.get("user_name"),
                    user_email=user_metadata.get("user_email"),
                    user_avatar=user_metadata.get("user_avatar"),
                    role=ParticipantRole.OWNER,
                )
                db.add(participant)
                db.commit()
                logger.info("owner_participant_added", execution_id=str(execution_id))
            except Exception as participant_error:
                db.rollback()
                logger.warning(
                    "failed_to_add_owner_participant",
                    error=str(participant_error),
                    execution_id=str(execution_id),
                )

        # Submit to Temporal
        try:
            # Use shared Temporal client for all organizations
            from control_plane_api.app.lib.temporal_client import get_temporal_client

            logger.info("getting_shared_temporal_client")
            temporal_client = await get_temporal_client()

            # Create workflow input
            workflow_input = PlanGenerationInput(
                execution_id=str(execution_id),
                organization_id=organization["id"],
                task_request=plan_request.model_dump(),  # Convert TaskPlanRequest to dict
                user_metadata=user_metadata,
                api_token=api_token,
            )

            # Workflow ID format: plan-generation-{execution_id}
            workflow_id = f"plan-generation-{execution_id}"

            # Use shared task queue for all organizations
            task_queue = os.getenv("TASK_QUEUE", "agent-control-plane.internal")

            logger.info(
                "submitting_plan_generation_to_temporal",
                workflow_id=workflow_id,
                task_queue=task_queue,
                execution_id=str(execution_id),
                organization_id=organization['id'],
            )

            # Start workflow
            workflow_handle = await temporal_client.start_workflow(
                PlanGenerationWorkflow.run,
                workflow_input,
                id=workflow_id,
                task_queue=task_queue,
            )

            # Update execution with Temporal workflow info
            execution.temporal_workflow_id = workflow_handle.id
            execution.temporal_run_id = workflow_handle.run_id
            execution.task_queue_name = task_queue
            db.commit()

            logger.info(
                "plan_generation_workflow_started",
                workflow_id=workflow_handle.id,
                run_id=workflow_handle.run_id,
                execution_id=str(execution_id),
            )

            return PlanGenerationResponse(
                execution_id=str(execution_id),
                workflow_id=workflow_handle.id,
                status="pending",
                message=f"Plan generation submitted. Use /api/v1/executions/{execution_id}/stream to track progress.",
            )

        except Exception as temporal_error:
            logger.error(
                "temporal_submission_failed",
                error=str(temporal_error),
                execution_id=str(execution_id),
                exc_info=True,
            )

            # Update execution status to failed
            execution.status = ExecutionStatus.FAILED.value
            execution.error_message = f"Failed to submit to Temporal: {str(temporal_error)}"
            db.commit()

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to submit plan generation: {str(temporal_error)}"
            )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "plan_generation_request_failed",
            error=str(e),
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Plan generation request failed: {str(e)}"
        )


@router.get("/plans/generation/{execution_id}")
async def get_plan_generation_status(
    execution_id: str,
    organization: dict = Depends(get_current_organization),
    db: Session = Depends(get_db),
):
    """
    Get the status of a plan generation execution.

    Returns execution details including the generated plan if completed.
    """
    try:
        execution = db.query(Execution).filter(
            Execution.id == execution_id,
            Execution.organization_id == organization["id"],
            Execution.execution_type == ExecutionType.PLAN_GENERATION.value,
        ).first()

        if not execution:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Plan generation execution not found"
            )

        return {
            "execution_id": str(execution.id),
            "status": execution.status,
            "description": execution.prompt[:100] if execution.prompt else None,
            "current_step": execution.execution_metadata.get("current_step"),
            "error_message": execution.error_message,
            "plan_json": execution.plan_json,
            "created_at": execution.created_at.isoformat() if execution.created_at else None,
            "started_at": execution.started_at.isoformat() if execution.started_at else None,
            "completed_at": execution.completed_at.isoformat() if execution.completed_at else None,
            "temporal_workflow_id": execution.temporal_workflow_id,
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "failed_to_get_plan_generation_status",
            error=str(e),
            execution_id=execution_id,
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get plan generation status: {str(e)}"
        )
