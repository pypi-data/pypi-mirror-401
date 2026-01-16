"""
Shared plan generation service - used by both sync and async endpoints.
Clean code with zero duplication.
"""
from typing import Dict, Any, Callable
from sqlalchemy.orm import Session
import structlog

from control_plane_api.app.models.task_planning import TaskPlanRequest, TaskPlanResponse
from control_plane_api.app.lib.task_planning.planning_workflow import (
    create_planning_workflow as create_multistep_workflow,
    run_planning_workflow_stream,
)
from control_plane_api.app.lib.task_planning.entity_resolver import resolve_plan_entities

logger = structlog.get_logger()


async def generate_plan(
    request: TaskPlanRequest,
    organization_id: str,
    api_token: str,
    db: Session,
    event_callback: Callable[[Dict[str, Any]], None] = None,
) -> TaskPlanResponse:
    """
    Generate a plan using the Agno workflow.

    This is the SINGLE source of truth for plan generation,
    used by both /tasks/plan/stream and async plan generation.

    Args:
        request: Task plan request
        organization_id: Organization ID
        api_token: API token for authentication
        db: Database session
        event_callback: Optional callback for streaming events

    Returns:
        Generated TaskPlanResponse with resolved entities
    """
    logger.info(
        "generating_plan",
        description=request.description[:100],
        organization_id=organization_id,
        quick_mode=request.quick_mode,
    )

    # Create the 2-step planning workflow
    workflow = create_multistep_workflow(
        db=db,
        organization_id=organization_id,
        api_token=api_token,
        quick_mode=request.quick_mode,
        outer_context=None,
    )

    logger.info("planning_workflow_created")

    # Run the workflow with event streaming
    plan = run_planning_workflow_stream(
        workflow,
        request,
        event_callback or (lambda x: None),  # No-op callback if not provided
        request.quick_mode,
    )

    logger.info("plan_generated", plan_title=plan.title)

    # Resolve entity names to UUIDs
    await resolve_plan_entities(
        plan_response=plan,
        organization_id=organization_id,
        db=db,
    )

    logger.info("plan_entities_resolved", plan_title=plan.title)

    return plan
