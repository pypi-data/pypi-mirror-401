"""
Plan Execution Router - Execute and manage multi-task plans using Temporal orchestration

Supports both SSE and WebSocket streaming for plan execution updates.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import Optional, Dict, Any
from datetime import datetime, timezone
import structlog
import uuid
import json
import os
import jwt as jwt_lib
import asyncio

from control_plane_api.app.database import get_db
from control_plane_api.app.models.plan_execution import PlanExecution, PlanExecutionStatus
from control_plane_api.app.lib.redis_client import get_redis_client
from control_plane_api.app.middleware.auth import get_current_organization, decode_jwt_token
from pydantic import BaseModel, Field

# Temporal client
from temporalio.client import Client as TemporalClient

# Import our workflow - conditionally to allow API to start without worker_internal
try:
    from worker_internal.planner.workflows import PlanOrchestratorWorkflow
    from worker_internal.planner.models import PlanOrchestratorInput, Plan
    PLANNER_AVAILABLE = True
except ImportError as e:
    PLANNER_AVAILABLE = False
    PlanOrchestratorWorkflow = None
    PlanOrchestratorInput = None
    Plan = None
    # Will log when first used

router = APIRouter()
logger = structlog.get_logger()


def extract_organization_id_from_token(api_token: Optional[str]) -> Optional[str]:
    """
    Extract organization ID from JWT token.

    Args:
        api_token: JWT token string

    Returns:
        Organization ID if found, None otherwise
    """
    if not api_token:
        return None

    try:
        # Decode without verification to get organization
        decoded = jwt_lib.decode(api_token, options={"verify_signature": False})
        org_id = decoded.get("organization") or decoded.get("org") or decoded.get("org_id")

        if org_id:
            logger.debug("extracted_org_from_token", organization_id=org_id)

        return org_id
    except Exception as e:
        logger.warning("failed_to_decode_token", error=str(e))
        return None


def extract_user_id_from_token(api_token: Optional[str]) -> Optional[str]:
    """
    Extract user ID from JWT token.

    Args:
        api_token: JWT token string

    Returns:
        User ID if found, None otherwise
    """
    if not api_token:
        return None

    try:
        decoded = jwt_lib.decode(api_token, options={"verify_signature": False})
        user_id = decoded.get("user_id") or decoded.get("sub") or decoded.get("email")

        if user_id:
            logger.debug("extracted_user_from_token", user_id=user_id)

        return user_id
    except Exception as e:
        logger.warning("failed_to_extract_user_id", error=str(e))
        return None


class PlanExecutionRequest(BaseModel):
    """Request to execute a plan"""
    plan: dict = Field(..., description="The plan JSON to execute")
    agent_id: Optional[str] = Field(None, description="Agent ID to use for task execution (optional, extracted from plan if not provided)")
    worker_queue_id: str = Field(..., description="Worker queue ID to route task executions to")
    plan_generation_id: Optional[str] = Field(None, description="ID of the plan generation execution that created this plan (for linking)")


class PlanExecutionResponse(BaseModel):
    """Response for plan execution"""
    execution_id: str
    status: str
    plan_title: str
    total_tasks: int


class PlanStatusResponse(BaseModel):
    """Response for plan status"""
    execution_id: str
    plan_generation_id: Optional[str] = None  # Link to plan generation
    status: str
    plan_title: str
    total_tasks: int
    completed_tasks: int
    failed_tasks: int
    progress_percentage: float
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    waiting_tasks: Optional[list] = None  # Tasks waiting for user input
    plan_json: Optional[dict] = None  # The full plan for UI rendering


async def get_temporal_client() -> TemporalClient:
    """
    Get Temporal client using env-based credentials.

    Uses shared namespace for all organizations.
    """
    from control_plane_api.app.lib.temporal_client import get_temporal_client as get_shared_client

    return await get_shared_client()


@router.post("/execute", response_model=PlanExecutionResponse, status_code=status.HTTP_201_CREATED)
async def execute_plan(
    request: PlanExecutionRequest,
    http_request: Request,
    db: Session = Depends(get_db),
):
    """
    Execute a multi-task plan using Temporal orchestration.

    This endpoint:
    1. Validates the plan structure
    2. Creates a plan execution record
    3. Starts a Temporal workflow to orchestrate task execution
    4. Returns execution ID for status tracking

    The workflow uses a Claude Code agent to intelligently manage plan execution.
    """
    # Check if planner module is available
    if not PLANNER_AVAILABLE:
        logger.error("planner_module_not_available", message="worker_internal.planner not installed")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Plan execution is not available. The planner module is not installed."
        )

    try:
        # Extract auth token
        auth_header = http_request.headers.get("authorization", "")
        jwt_token = auth_header.replace("Bearer ", "").replace("UserKey ", "") if auth_header else None

        # Extract organization ID and user ID from JWT token
        organization_id = extract_organization_id_from_token(jwt_token)
        user_id = extract_user_id_from_token(jwt_token)

        if not organization_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not extract organization_id from JWT token"
            )

        if not jwt_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authorization token required"
            )

        # Parse and validate plan
        plan_data = request.plan.get("plan", request.plan)  # Handle both formats
        plan_title = plan_data.get("title", "Untitled Plan")
        total_tasks = 0

        # Extract agent_id or team_id from plan if not provided in request
        agent_id = request.agent_id
        team_id = None

        if plan_data.get("team_breakdown"):
            team = plan_data["team_breakdown"][0]

            # Check if this is a team-based plan
            team_id = team.get("team_id")

            # Extract agent_id (could be null for team plans)
            if not agent_id:
                agent_id = team.get("agent_id")

            # If still no agent_id, try to get from first task (fallback for team plans)
            if not agent_id and team.get("tasks") and len(team.get("tasks", [])) > 0:
                agent_id = team["tasks"][0].get("agent_id")
                logger.info("agent_id_extracted_from_first_task", agent_id=agent_id)
            elif agent_id:
                logger.info("agent_id_extracted_from_plan", agent_id=agent_id)

        # For team-based plans, agent_id can be null (tasks have individual agent_ids)
        # Only raise error if it's not a team plan
        if not agent_id and not team_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Either agent_id or team_id must be provided in plan"
            )

        if plan_data.get("team_breakdown"):
            team = plan_data["team_breakdown"][0]
            total_tasks = len(team.get("tasks", []))

        logger.info(
            "plan_execution_requested",
            plan_title=plan_title,
            total_tasks=total_tasks,
            agent_id=agent_id,
        )

        # Generate execution ID
        execution_id = str(uuid.uuid4())

        # Create plan execution record
        plan_execution = PlanExecution(
            id=uuid.uuid4(),
            execution_id=execution_id,
            organization_id=organization_id,
            agent_id=agent_id,
            plan_generation_id=request.plan_generation_id,  # Link to plan generation
            title=plan_title,
            summary=plan_data.get("summary"),
            total_tasks=total_tasks,
            completed_tasks=0,
            failed_tasks=0,
            status=PlanExecutionStatus.RUNNING,
            plan_json=request.plan,
            estimated_cost_usd=plan_data.get("cost_estimate", {}).get("estimated_cost_usd"),
            started_at=datetime.utcnow(),
        )
        db.add(plan_execution)
        db.commit()

        # CRITICAL: Normalize plan data before validation
        # Convert None to empty dicts/lists/strings to prevent Pydantic validation errors
        def normalize_plan_data(data):
            """Recursively normalize plan data for Pydantic validation"""
            if isinstance(data, dict):
                normalized = {}
                for key, value in data.items():
                    if value is None:
                        # Convert None to appropriate empty value
                        if key in ['model_info', 'execution_environment', 'recommended_execution', 'cost_estimate', 'realized_savings']:
                            normalized[key] = {}
                        elif key.endswith('_to_use') or key in ['knowledge_references', 'subtasks', 'risks', 'prerequisites', 'success_criteria']:
                            normalized[key] = []
                        elif key in ['agent_id', 'agent_name', 'team_id', 'team_name']:
                            # For team-based plans, these can be empty strings
                            normalized[key] = ''
                        else:
                            normalized[key] = value
                    elif isinstance(value, (dict, list)):
                        normalized[key] = normalize_plan_data(value)
                    else:
                        normalized[key] = value
                return normalized
            elif isinstance(data, list):
                return [normalize_plan_data(item) for item in data]
            return data

        plan_data = normalize_plan_data(plan_data)
        logger.info("plan_data_normalized", plan_title=plan_data.get('title'))

        # Parse plan into Pydantic model
        plan_obj = Plan(**plan_data)

        # CRITICAL: Ensure all tasks have worker_queue_id set
        # The workflow requires each task to have worker_queue_id
        for team in plan_obj.team_breakdown:
            for task in team.tasks:
                if not task.worker_queue_id:
                    task.worker_queue_id = request.worker_queue_id
                    logger.debug(
                        "set_worker_queue_id_on_task",
                        task_id=task.id,
                        worker_queue_id=request.worker_queue_id
                    )

        # Start Temporal workflow
        try:
            temporal_client = await get_temporal_client()

            workflow_input = PlanOrchestratorInput(
                plan=plan_obj,
                organization_id=organization_id,
                agent_id=agent_id,  # Use extracted agent_id (from request or plan)
                worker_queue_id=request.worker_queue_id,
                user_id=user_id,
                execution_id=execution_id,
                jwt_token=jwt_token,
            )

            # Use shared task queue for all organizations
            task_queue = os.getenv("TASK_QUEUE", "agent-control-plane.internal")

            # Start workflow
            await temporal_client.start_workflow(
                PlanOrchestratorWorkflow.run,
                workflow_input,
                id=f"plan-{execution_id}",
                task_queue=task_queue,
            )

            logger.info(
                "plan_workflow_started",
                execution_id=execution_id,
                workflow_id=f"plan-{execution_id}",
                task_queue=task_queue,
                organization_id=organization_id,
            )

        except Exception as e:
            logger.error(
                "failed_to_start_workflow",
                error=str(e),
                execution_id=execution_id,
            )
            # Update status to failed
            plan_execution.status = PlanExecutionStatus.FAILED
            db.commit()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to start plan execution workflow: {str(e)}"
            )

        return PlanExecutionResponse(
            execution_id=execution_id,
            status="running",
            plan_title=plan_title,
            total_tasks=total_tasks,
        )

    except Exception as e:
        logger.error("plan_execution_error", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Plan execution failed: {str(e)}"
        )


@router.get("/plan-executions")
def list_plan_executions(
    status: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
    organization: dict = Depends(get_current_organization),
    db: Session = Depends(get_db),
):
    """
    List plan executions with optional filtering.
    Automatically filters by the authenticated user's organization.
    """
    query = db.query(PlanExecution)

    # Always filter by organization from auth
    query = query.filter(PlanExecution.organization_id == organization["id"])

    if status:
        query = query.filter(PlanExecution.status == status)

    # Order by created_at so newest executions appear first, regardless of whether they've started
    query = query.order_by(PlanExecution.created_at.desc())
    query = query.offset(offset).limit(limit)

    executions = query.all()

    return {
        "executions": [
            {
                "execution_id": exec.execution_id,
                "agent_id": str(exec.agent_id) if exec.agent_id else None,
                "plan_generation_id": exec.plan_generation_id,  # Link to plan generation
                "title": exec.title,
                "summary": exec.summary,
                "status": exec.status.value if hasattr(exec.status, 'value') else exec.status,
                "total_tasks": exec.total_tasks,
                "completed_tasks": exec.completed_tasks,
                "failed_tasks": exec.failed_tasks or 0,
                "created_at": exec.created_at.isoformat() if exec.created_at else None,
                "started_at": exec.started_at.isoformat() if exec.started_at else None,
                "completed_at": exec.completed_at.isoformat() if exec.completed_at else None,
            }
            for exec in executions
        ],
        "total": query.count(),
        "limit": limit,
        "offset": offset,
    }


@router.get("/{execution_id}", response_model=PlanStatusResponse)
def get_plan_execution(
    execution_id: str,
    db: Session = Depends(get_db),
):
    """
    Get plan execution status and progress.

    Returns current status, completed tasks, and progress information.
    """
    plan_exec = db.query(PlanExecution).filter(
        PlanExecution.execution_id == execution_id
    ).first()

    if not plan_exec:
        raise HTTPException(status_code=404, detail="Plan execution not found")

    progress = 0.0
    if plan_exec.total_tasks > 0:
        progress = (plan_exec.completed_tasks / plan_exec.total_tasks) * 100

    return PlanStatusResponse(
        execution_id=plan_exec.execution_id,
        plan_generation_id=plan_exec.plan_generation_id,  # Include link to plan generation
        status=plan_exec.status.value if hasattr(plan_exec.status, 'value') else plan_exec.status,
        plan_title=plan_exec.title,
        total_tasks=plan_exec.total_tasks,
        completed_tasks=plan_exec.completed_tasks,
        failed_tasks=plan_exec.failed_tasks or 0,
        progress_percentage=progress,
        started_at=plan_exec.started_at,
        completed_at=plan_exec.completed_at,
        waiting_tasks=plan_exec.waiting_tasks or [],  # Include waiting tasks for continuation
        plan_json=plan_exec.plan_json,  # Include full plan for UI rendering
    )


@router.get("/{execution_id}/stream")
async def stream_plan_execution(
    execution_id: str,
    request: Request,
    last_event_id: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """
    Stream plan execution updates using Server-Sent Events (SSE).

    This endpoint streams real-time events from plan execution including:
    - Plan started/completed
    - Task started/completed/waiting for input
    - Tasks running in parallel
    - Progress updates

    Uses Redis event bus for real-time updates (200ms polling).
    Supports Last-Event-ID for reconnection and gap recovery.
    """

    async def generate_sse():
        """Generate Server-Sent Events from Redis"""
        import time

        # Parse Last-Event-ID for reconnection
        last_known_id = last_event_id or request.headers.get("Last-Event-ID")
        last_counter = 0

        if last_known_id:
            try:
                parts = last_known_id.split("_")
                if len(parts) >= 2 and parts[0] == execution_id:
                    last_counter = int(parts[1])
                    logger.info(
                        "plan_stream_reconnection",
                        execution_id=execution_id[:8],
                        last_counter=last_counter
                    )
            except (ValueError, IndexError):
                logger.warning("invalid_last_event_id", execution_id=execution_id[:8])
                last_counter = 0

        # Event ID counter
        event_id_counter = last_counter

        def generate_event_id() -> str:
            nonlocal event_id_counter
            event_id_counter += 1
            return f"{execution_id}_{event_id_counter}_{int(time.time() * 1000000)}"

        try:
            # Verify plan execution exists
            plan_exec = db.query(PlanExecution).filter(
                PlanExecution.execution_id == execution_id
            ).first()

            if not plan_exec:
                raise HTTPException(status_code=404, detail="Plan execution not found")

            # Get Redis client
            redis_client = get_redis_client()
            if not redis_client:
                logger.error("redis_not_available", execution_id=execution_id[:8])
                raise HTTPException(
                    status_code=503,
                    detail="Event streaming unavailable (Redis not configured)"
                )

            # Redis key for plan events
            redis_key = f"plan-execution:{execution_id}:events"
            last_redis_event_index = -1

            logger.info(
                "plan_stream_started",
                execution_id=execution_id[:8],
                redis_key=redis_key
            )

            # Polling loop (200ms interval, same as agent worker)
            while True:
                # Check if client disconnected
                if await request.is_disconnected():
                    logger.info("plan_stream_client_disconnected", execution_id=execution_id[:8])
                    break

                # Get current events from Redis
                redis_events = await redis_client.lrange(redis_key, 0, -1)
                total_events = len(redis_events)

                if total_events > (last_redis_event_index + 1):
                    # New events available
                    chronological_events = list(reversed(redis_events))  # LPUSH stores in reverse

                    # Send only NEW events
                    for i in range(last_redis_event_index + 1, len(chronological_events)):
                        event_json = chronological_events[i]

                        try:
                            event_data = json.loads(event_json)
                            event_type = event_data.get("event_type", "unknown")
                            payload = event_data.get("data", {})

                            # Generate SSE event
                            event_id = generate_event_id()
                            yield f"id: {event_id}\n"
                            yield f"event: {event_type}\n"
                            yield f"data: {json.dumps(payload)}\n\n"

                            last_redis_event_index = i

                        except json.JSONDecodeError:
                            logger.warning(
                                "malformed_event_skipped",
                                execution_id=execution_id[:8],
                                index=i
                            )
                            continue

                # Check if plan is complete
                if plan_exec.status in [
                    PlanExecutionStatus.COMPLETED,
                    PlanExecutionStatus.FAILED,
                    PlanExecutionStatus.CANCELLED,
                ]:
                    # Send final done event
                    event_id = generate_event_id()
                    yield f"id: {event_id}\n"
                    yield f"event: done\n"
                    yield f"data: {json.dumps({'status': plan_exec.status})}\n\n"
                    logger.info("plan_stream_complete", execution_id=execution_id[:8])
                    break

                # Check if plan is waiting for user input (paused)
                if plan_exec.status == PlanExecutionStatus.PENDING_USER_INPUT:
                    # Send waiting_for_user_input event with details
                    event_id = generate_event_id()
                    waiting_data = {
                        "status": "pending_user_input",
                        "waiting_tasks": plan_exec.waiting_tasks or [],
                        "message": "Plan paused - waiting for user input",
                    }
                    yield f"id: {event_id}\n"
                    yield f"event: plan_waiting_for_input\n"
                    yield f"data: {json.dumps(waiting_data)}\n\n"
                    logger.info("plan_paused_for_user_input", execution_id=execution_id[:8])
                    # Keep streaming (don't break) - stream will continue when user provides input
                    # But add a longer sleep to reduce polling when paused
                    await asyncio.sleep(2.0)  # 2 seconds when paused
                    db.refresh(plan_exec)
                    continue

                # Refresh plan exec status from DB
                db.refresh(plan_exec)

                # Wait 200ms before next poll (same as agent worker)
                await asyncio.sleep(0.2)

        except HTTPException:
            raise
        except Exception as e:
            logger.error(
                "plan_stream_error",
                execution_id=execution_id[:8],
                error=str(e)
            )
            # Send error event
            event_id = generate_event_id()
            yield f"id: {event_id}\n"
            yield f"event: error\n"
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    return StreamingResponse(
        generate_sse(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",  # Disable nginx buffering
        }
    )


# =============================================================================
# WebSocket Streaming for Plan Execution
# =============================================================================

class PlanConnectionManager:
    """
    Manages WebSocket connections for plan execution streaming.

    Similar to ClientConnectionManager in websocket_client.py but specific to plans.
    """

    def __init__(self):
        # execution_id -> WebSocket
        self._connections: Dict[str, WebSocket] = {}
        # organization_id -> Set[execution_id]
        self._org_connections: Dict[str, set] = {}
        # Statistics
        self._stats = {
            "total_connections": 0,
            "active_connections": 0,
            "messages_sent": 0,
            "errors": 0,
        }

    async def connect(
        self,
        execution_id: str,
        organization_id: str,
        websocket: WebSocket,
    ) -> None:
        """Register a new plan WebSocket connection."""
        await websocket.accept()

        self._connections[execution_id] = websocket

        if organization_id not in self._org_connections:
            self._org_connections[organization_id] = set()
        self._org_connections[organization_id].add(execution_id)

        self._stats["total_connections"] += 1
        self._stats["active_connections"] = len(self._connections)

        logger.info(
            "plan_websocket_connected",
            execution_id=execution_id[:8],
            organization_id=organization_id[:8],
            active_connections=self._stats["active_connections"],
        )

    async def disconnect(self, execution_id: str, organization_id: str) -> None:
        """Unregister a plan WebSocket connection."""
        if execution_id in self._connections:
            del self._connections[execution_id]

        if organization_id in self._org_connections:
            self._org_connections[organization_id].discard(execution_id)
            if not self._org_connections[organization_id]:
                del self._org_connections[organization_id]

        self._stats["active_connections"] = len(self._connections)

        logger.info(
            "plan_websocket_disconnected",
            execution_id=execution_id[:8],
            active_connections=self._stats["active_connections"],
        )

    def get_stats(self) -> Dict[str, int]:
        """Get connection statistics."""
        return self._stats.copy()


# Global connection manager for plan WebSocket connections
plan_connection_manager = PlanConnectionManager()


async def send_plan_json(websocket: WebSocket, event_type: str, data: Any) -> None:
    """
    Send JSON message via WebSocket for plan events.

    Args:
        websocket: WebSocket connection
        event_type: Event type (e.g., 'plan_started', 'task_completed')
        data: Event data payload
    """
    try:
        message = {
            "type": event_type,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            **data
        }
        await websocket.send_text(json.dumps(message))
        plan_connection_manager._stats["messages_sent"] += 1
        logger.debug("plan_websocket_message_sent", event_type=event_type)
    except Exception as e:
        logger.error("failed_to_send_plan_websocket_message", error=str(e), event_type=event_type)
        plan_connection_manager._stats["errors"] += 1
        raise


async def handle_plan_auth(websocket: WebSocket, token: str) -> Optional[str]:
    """
    Handle authentication message for plan WebSocket.

    Args:
        websocket: WebSocket connection
        token: JWT authentication token

    Returns:
        organization_id if authentication successful, None otherwise
    """
    try:
        decoded = decode_jwt_token(token)

        if not decoded:
            logger.error("plan_jwt_decode_failed", reason="Invalid token format")
            await send_plan_json(websocket, "auth_error", {
                "error": "Invalid authentication token",
                "code": "INVALID_TOKEN",
            })
            return None

        # Extract organization ID from token claims
        organization_id = (
            decoded.get('https://kubiya.ai/org_id') or
            decoded.get('org_id') or
            decoded.get('organization_id') or
            decoded.get('organization') or
            decoded.get('org')
        )

        if not organization_id:
            logger.error("plan_org_id_missing", decoded_claims=list(decoded.keys()))
            await send_plan_json(websocket, "auth_error", {
                "error": "Organization ID not found in token",
                "code": "ORG_ID_MISSING",
            })
            return None

        user_id = decoded.get('sub')

        logger.info(
            "plan_websocket_authenticated",
            organization_id=organization_id[:8] if len(organization_id) > 8 else organization_id,
            user_id=user_id[:8] if user_id and len(user_id) > 8 else user_id,
        )

        await send_plan_json(websocket, "auth_success", {
            "organization_id": organization_id,
            "user_id": user_id,
            "authenticated_at": datetime.now(timezone.utc).isoformat(),
        })

        return organization_id

    except Exception as e:
        logger.error("plan_authentication_failed", error=str(e), error_type=type(e).__name__)
        await send_plan_json(websocket, "auth_error", {
            "error": "Authentication failed",
            "code": "AUTH_FAILED",
        })
        return None


@router.websocket("/ws/{execution_id}")
async def websocket_plan_execution_stream(
    websocket: WebSocket,
    execution_id: str,
    last_event_id: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """
    WebSocket endpoint for plan execution streaming.

    Streams plan execution events to frontend clients with automatic reconnection support.
    This is the WebSocket equivalent of the SSE endpoint at /{execution_id}/stream.

    Args:
        websocket: WebSocket connection
        execution_id: Plan execution ID to stream
        last_event_id: Last received event ID (for resumption)
        db: Database session

    Flow:
        1. Accept WebSocket connection
        2. Wait for auth message with JWT token
        3. Validate token and extract organization_id
        4. Send 'connected' event
        5. Stream events from Redis (plan_started, task_completed, etc.)
        6. Handle ping/pong for keepalive
        7. Support resumption via last_event_id

    Event Types:
        - connected: Connection established
        - auth_success: Authentication successful
        - auth_error: Authentication failed
        - plan_started: Plan execution started
        - todo_list_initialized: Task list prepared
        - todo_item_updated: Task status changed
        - task_started: Individual task started
        - task_completed: Individual task completed
        - task_waiting_for_input: Task needs user input
        - done: Plan execution completed
        - error: Error occurred
    """
    organization_id: Optional[str] = None
    authenticated = False

    try:
        # Accept connection first
        await websocket.accept()

        # Track connection in pending state
        plan_connection_manager._connections[execution_id] = websocket
        plan_connection_manager._org_connections.setdefault("pending", set()).add(execution_id)
        plan_connection_manager._stats["total_connections"] += 1
        plan_connection_manager._stats["active_connections"] = len(plan_connection_manager._connections)

        logger.info(
            "plan_websocket_connection_started",
            execution_id=execution_id[:8],
            last_event_id=last_event_id,
        )

        # Wait for authentication message (timeout after 5 seconds)
        try:
            auth_message = await asyncio.wait_for(websocket.receive_text(), timeout=5.0)
            auth_data = json.loads(auth_message)

            if auth_data.get("type") == "auth" and "token" in auth_data:
                organization_id = await handle_plan_auth(websocket, auth_data["token"])
                if not organization_id:
                    await websocket.close(code=4001, reason="Authentication failed")
                    return

                authenticated = True

                # Update connection from pending to actual org
                if "pending" in plan_connection_manager._org_connections:
                    plan_connection_manager._org_connections["pending"].discard(execution_id)
                    if not plan_connection_manager._org_connections["pending"]:
                        del plan_connection_manager._org_connections["pending"]

                plan_connection_manager._org_connections.setdefault(organization_id, set()).add(execution_id)

        except asyncio.TimeoutError:
            logger.error("plan_auth_timeout", execution_id=execution_id[:8])
            await websocket.close(code=4002, reason="Authentication timeout")
            return
        except json.JSONDecodeError:
            logger.error("plan_invalid_auth_message", execution_id=execution_id[:8])
            await websocket.close(code=4003, reason="Invalid authentication message")
            return

        # Verify plan execution exists
        plan_exec = db.query(PlanExecution).filter(
            PlanExecution.execution_id == execution_id
        ).first()

        if not plan_exec:
            await send_plan_json(websocket, "error", {"error": "Plan execution not found"})
            await websocket.close(code=4004, reason="Plan execution not found")
            return

        # Send connected event
        await send_plan_json(websocket, "connected", {
            "execution_id": execution_id,
            "organization_id": organization_id,
            "plan_title": plan_exec.title,
            "total_tasks": plan_exec.total_tasks,
            "status": plan_exec.status.value if hasattr(plan_exec.status, 'value') else plan_exec.status,
            "connected_at": datetime.now(timezone.utc).isoformat(),
        })

        # Get Redis client
        redis_client = get_redis_client()
        if not redis_client:
            await send_plan_json(websocket, "error", {"error": "Redis not available"})
            await websocket.close(code=503, reason="Event streaming unavailable")
            return

        # Redis key for plan events
        redis_key = f"plan-execution:{execution_id}:events"

        # Parse last_event_id for reconnection
        last_redis_event_index = -1
        if last_event_id:
            try:
                parts = last_event_id.split("_")
                if len(parts) >= 2 and parts[0] == execution_id:
                    last_redis_event_index = int(parts[1]) - 1  # Convert to 0-indexed
                    logger.info(
                        "plan_websocket_reconnection",
                        execution_id=execution_id[:8],
                        last_index=last_redis_event_index
                    )
            except (ValueError, IndexError):
                logger.warning("plan_invalid_last_event_id", execution_id=execution_id[:8])

        event_id_counter = last_redis_event_index + 1

        def generate_event_id() -> str:
            nonlocal event_id_counter
            event_id_counter += 1
            return f"{execution_id}_{event_id_counter}_{int(datetime.now(timezone.utc).timestamp() * 1000000)}"

        logger.info("plan_websocket_streaming_started", execution_id=execution_id[:8])

        # Listen for both Redis events and client messages
        async def listen_redis():
            """Listen for plan events from Redis."""
            nonlocal last_redis_event_index

            try:
                while True:
                    # Get current events from Redis
                    redis_events = await redis_client.lrange(redis_key, 0, -1)
                    total_events = len(redis_events)

                    if total_events > (last_redis_event_index + 1):
                        # New events available - Redis LPUSH stores in reverse order
                        chronological_events = list(reversed(redis_events))

                        # Send only NEW events
                        for i in range(last_redis_event_index + 1, len(chronological_events)):
                            event_json = chronological_events[i]

                            try:
                                event_data = json.loads(event_json)
                                event_type = event_data.get("event_type", "unknown")
                                payload = event_data.get("data", {})

                                # Add event ID for client tracking
                                payload["event_id"] = generate_event_id()

                                await send_plan_json(websocket, event_type, payload)
                                last_redis_event_index = i

                            except json.JSONDecodeError:
                                logger.warning(
                                    "plan_malformed_event_skipped",
                                    execution_id=execution_id[:8],
                                    index=i
                                )
                                continue

                    # Refresh plan execution status from DB
                    db.refresh(plan_exec)

                    # Check if plan is complete
                    if plan_exec.status in [
                        PlanExecutionStatus.COMPLETED,
                        PlanExecutionStatus.FAILED,
                        PlanExecutionStatus.CANCELLED,
                    ]:
                        # Send final done event
                        await send_plan_json(websocket, "done", {
                            "event_id": generate_event_id(),
                            "status": plan_exec.status.value if hasattr(plan_exec.status, 'value') else plan_exec.status,
                            "completed_tasks": plan_exec.completed_tasks,
                            "failed_tasks": plan_exec.failed_tasks or 0,
                            "total_tasks": plan_exec.total_tasks,
                        })
                        logger.info("plan_websocket_complete", execution_id=execution_id[:8])
                        return

                    # Check if waiting for user input
                    if plan_exec.status == PlanExecutionStatus.PENDING_USER_INPUT:
                        await send_plan_json(websocket, "plan_waiting_for_input", {
                            "event_id": generate_event_id(),
                            "status": "pending_user_input",
                            "waiting_tasks": plan_exec.waiting_tasks or [],
                            "message": "Plan paused - waiting for user input",
                        })
                        # Longer sleep when paused
                        await asyncio.sleep(2.0)
                        continue

                    # Normal polling interval (200ms)
                    await asyncio.sleep(0.2)

            except Exception as e:
                logger.error("plan_redis_stream_error", error=str(e), error_type=type(e).__name__)
                raise

        async def listen_client():
            """Listen for client messages (ping, etc.)."""
            try:
                while True:
                    message = await websocket.receive_text()
                    data = json.loads(message)

                    if data.get("type") == "ping":
                        await send_plan_json(websocket, "pong", {
                            "timestamp": int(datetime.now(timezone.utc).timestamp() * 1000)
                        })

                    elif data.get("type") == "resume":
                        logger.info(
                            "plan_resume_requested",
                            execution_id=execution_id[:8],
                            last_event_id=data.get("last_event_id")
                        )

            except WebSocketDisconnect:
                pass
            except Exception as e:
                logger.error("plan_client_message_error", error=str(e))

        # Run both listeners concurrently
        redis_task = asyncio.create_task(listen_redis())
        client_task = asyncio.create_task(listen_client())

        # Wait for either task to complete
        done, pending = await asyncio.wait(
            {redis_task, client_task},
            return_when=asyncio.FIRST_COMPLETED
        )

        # Cancel pending tasks
        for task in pending:
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass

    except WebSocketDisconnect:
        logger.info("plan_client_disconnected", execution_id=execution_id[:8])

    except Exception as e:
        logger.error(
            "plan_websocket_error",
            execution_id=execution_id[:8],
            error=str(e),
            error_type=type(e).__name__,
        )
        try:
            await send_plan_json(websocket, "error", {"error": str(e)})
        except:
            pass

    finally:
        # Cleanup
        if organization_id:
            await plan_connection_manager.disconnect(execution_id, organization_id)

        logger.info("plan_websocket_closed", execution_id=execution_id[:8])


@router.get("/ws/stats")
async def plan_websocket_stats():
    """Get plan WebSocket connection statistics."""
    return plan_connection_manager.get_stats()


@router.post("/events/{execution_id}")
async def publish_plan_event(
    execution_id: str,
    event: dict,
):
    """
    Publish a plan event to Redis (called by Temporal activities).

    This endpoint receives events from plan activities and publishes them to Redis
    for the streaming endpoint to consume.
    """
    try:
        redis_client = get_redis_client()
        if not redis_client:
            logger.warning("redis_not_available", execution_id=execution_id[:8])
            return {"success": False, "error": "Redis not available"}

        # Event should have: event_type, data, timestamp
        message_json = json.dumps(event)

        # Redis keys
        list_key = f"plan-execution:{execution_id}:events"
        channel = f"plan-execution:{execution_id}:stream"

        # Store in list (for replay)
        await redis_client.lpush(list_key, message_json)
        await redis_client.ltrim(list_key, 0, 999)
        await redis_client.expire(list_key, 3600)

        # Publish to pub/sub (for real-time)
        await redis_client.publish(channel, message_json)

        logger.debug(
            "plan_event_published_to_redis",
            execution_id=execution_id[:8],
            event_type=event.get("event_type"),
        )

        return {"success": True}

    except Exception as e:
        logger.error(
            "plan_event_publish_error",
            execution_id=execution_id[:8],
            error=str(e),
        )
        return {"success": False, "error": str(e)}


@router.patch("/{execution_id}")
def update_plan_execution(
    execution_id: str,
    updates: dict,
    db: Session = Depends(get_db),
):
    """
    Update plan execution state (called by Temporal activities).

    Internal endpoint used by workflows to update plan state.
    """
    plan_exec = db.query(PlanExecution).filter(
        PlanExecution.execution_id == execution_id
    ).first()

    if not plan_exec:
        raise HTTPException(status_code=404, detail="Plan execution not found")

    # Update fields
    for key, value in updates.items():
        if hasattr(plan_exec, key):
            setattr(plan_exec, key, value)

    plan_exec.updated_at = datetime.utcnow()
    db.commit()

    logger.info(
        "plan_execution_updated",
        execution_id=execution_id,
        updates=list(updates.keys()),
    )

    return {"success": True}


@router.post("/{execution_id}/continue")
async def continue_plan_execution(
    execution_id: str,
    request: dict,
    http_request: Request,
    db: Session = Depends(get_db),
):
    """
    Continue a plan execution that's waiting for user input.

    This endpoint:
    1. Accepts batch responses for multiple waiting tasks
    2. Sends messages to each agent execution
    3. Restarts the workflow to continue plan execution

    Body:
        {
            "responses": [
                {
                    "execution_id": "agent-exec-abc-123",
                    "message": "5 + 3"
                },
                {
                    "execution_id": "agent-exec-xyz-456",
                    "message": "Calculate for today"
                }
            ]
        }
    """
    try:
        # Extract auth token
        auth_header = http_request.headers.get("authorization", "")
        jwt_token = auth_header.replace("Bearer ", "").replace("UserKey ", "") if auth_header else None

        if not jwt_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authorization token required"
            )

        # Get responses from request
        responses = request.get("responses", [])
        if not responses:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="'responses' array is required"
            )

        # Verify plan execution exists
        plan_exec = db.query(PlanExecution).filter(
            PlanExecution.execution_id == execution_id
        ).first()

        if not plan_exec:
            raise HTTPException(status_code=404, detail="Plan execution not found")

        if plan_exec.status != "pending_user_input":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Plan is not waiting for user input (status: {plan_exec.status})"
            )

        # Get waiting tasks from plan
        waiting_tasks = plan_exec.waiting_tasks or []
        if not waiting_tasks:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No tasks are waiting for user input"
            )

        # Validate that provided execution_ids exist in waiting tasks
        waiting_execution_ids = {task["execution_id"] for task in waiting_tasks}
        provided_execution_ids = {resp["execution_id"] for resp in responses}

        invalid_ids = provided_execution_ids - waiting_execution_ids
        if invalid_ids:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid execution_ids: {invalid_ids}. Not in waiting tasks."
            )

        # Send messages to each agent execution FIRST (before signaling workflow)
        # This allows agents to process and complete before workflow resumes
        import httpx
        control_plane_url = os.getenv("CONTROL_PLANE_URL", "https://control-plane.kubiya.ai")

        sent_messages = []
        async with httpx.AsyncClient(timeout=30.0) as client:
            for response in responses:
                exec_id = response["execution_id"]
                message = response["message"]

                # Send message to agent execution
                try:
                    msg_response = await client.post(
                        f"{control_plane_url}/api/v1/executions/{exec_id}/message",
                        json={"message": message},
                        headers={"Authorization": f"Bearer {jwt_token}"}
                    )

                    if msg_response.status_code not in (200, 201, 202):
                        logger.error(
                            "failed_to_send_message_to_execution",
                            execution_id=exec_id,
                            status=msg_response.status_code,
                            error=msg_response.text
                        )
                        raise Exception(f"Failed to send message to {exec_id}: {msg_response.text}")

                    sent_messages.append(exec_id)
                    logger.info("message_sent_to_execution", execution_id=exec_id)

                except Exception as e:
                    logger.error("send_message_failed", execution_id=exec_id, error=str(e))
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail=f"Failed to send message to {exec_id}: {str(e)}"
                    )

        # Wait a moment for agents to process messages
        import asyncio
        await asyncio.sleep(2)

        # Update plan status back to RUNNING and clear waiting tasks for the ones we responded to
        remaining_waiting = [
            task for task in waiting_tasks
            if task["execution_id"] not in provided_execution_ids
        ]

        new_status = "pending_user_input" if remaining_waiting else "running"

        plan_exec.status = new_status
        plan_exec.waiting_tasks = remaining_waiting
        plan_exec.updated_at = datetime.utcnow()
        db.commit()

        logger.info(
            "plan_continuation_initiated",
            execution_id=execution_id,
            responses_count=len(responses),
            remaining_waiting=len(remaining_waiting),
            new_status=new_status,
        )

        # Signal the paused workflow to continue (send signal for each task)
        try:
            temporal_client = await get_temporal_client()
            workflow_id = f"plan-{execution_id}"
            workflow_handle = temporal_client.get_workflow_handle(workflow_id)

            # Map execution_id to task_id
            task_id_map = {task["execution_id"]: task["task_id"] for task in waiting_tasks}

            signals_sent = []
            for response in responses:
                exec_id = response["execution_id"]
                message = response["message"]
                task_id = task_id_map.get(exec_id)

                if task_id is not None:
                    # Send signal to workflow to continue this task
                    await workflow_handle.signal(
                        "continue_task_signal",
                        {"task_id": task_id, "user_message": message}
                    )
                    signals_sent.append(task_id)
                    logger.info(
                        "workflow_signal_sent",
                        execution_id=execution_id,
                        task_id=task_id,
                        workflow_id=workflow_id
                    )

            logger.info(
                "plan_workflow_signaled",
                execution_id=execution_id,
                signals_sent=len(signals_sent),
                task_ids=signals_sent
            )

        except Exception as e:
            logger.error("failed_to_signal_workflow", error=str(e), execution_id=execution_id)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to signal workflow: {str(e)}"
            )

        return {
            "success": True,
            "execution_id": execution_id,
            "messages_sent": len(sent_messages),
            "sent_to_executions": sent_messages,
            "signals_sent": len(signals_sent),
            "task_ids": signals_sent,
            "remaining_waiting_tasks": len(remaining_waiting),
            "plan_status": new_status,
            "workflow_signaled": True,
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error("continue_plan_error", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to continue plan: {str(e)}"
        )


@router.post("/{execution_id}/tasks/{task_id}/message")
async def send_task_message(
    execution_id: str,
    task_id: int,
    request: dict,
    http_request: Request,
    db: Session = Depends(get_db),
):
    """
    Send a message to a task that's waiting for user input.

    This endpoint:
    1. Verifies the plan execution and task exist
    2. Signals the Temporal workflow to continue the task with the user's message
    3. The workflow will resume the agent execution and continue streaming

    Body:
        {
            "message": "user's message to continue the conversation"
        }
    """
    try:
        # Extract auth token
        auth_header = http_request.headers.get("authorization", "")
        jwt_token = auth_header.replace("Bearer ", "").replace("UserKey ", "") if auth_header else None

        if not jwt_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authorization token required"
            )

        # Get message from request
        user_message = request.get("message")
        if not user_message:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="'message' field is required"
            )

        # Verify plan execution exists
        plan_exec = db.query(PlanExecution).filter(
            PlanExecution.execution_id == execution_id
        ).first()

        if not plan_exec:
            raise HTTPException(status_code=404, detail="Plan execution not found")

        # Verify task exists in plan
        plan_data = plan_exec.plan_json.get("plan", plan_exec.plan_json)
        if plan_data.get("team_breakdown"):
            tasks = plan_data["team_breakdown"][0].get("tasks", [])
            task = next((t for t in tasks if t.get("id") == task_id), None)

            if not task:
                raise HTTPException(status_code=404, detail=f"Task {task_id} not found in plan")

        # Signal the Temporal workflow
        try:
            temporal_client = await get_temporal_client()
            workflow_id = f"plan-{execution_id}"

            # Send signal to workflow
            workflow_handle = temporal_client.get_workflow_handle(workflow_id)
            await workflow_handle.signal(
                "continue_task_signal",
                {"task_id": task_id, "user_message": user_message}
            )

            logger.info(
                "task_continuation_signal_sent",
                execution_id=execution_id,
                task_id=task_id,
                workflow_id=workflow_id,
            )

            return {
                "success": True,
                "execution_id": execution_id,
                "task_id": task_id,
                "message_sent": True,
                "workflow_signaled": True,
            }

        except Exception as e:
            logger.error(
                "failed_to_signal_workflow",
                error=str(e),
                execution_id=execution_id,
                task_id=task_id,
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to signal workflow: {str(e)}"
            )

    except HTTPException:
        raise
    except Exception as e:
        logger.error("send_task_message_error", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to send message: {str(e)}"
        )
