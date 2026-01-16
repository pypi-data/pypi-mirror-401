"""
WebSocket Client Endpoint for Execution Streaming.

Provides persistent WebSocket connections for frontend clients to receive
real-time execution updates, eliminating the 300-second HTTP timeout limitation.

Features:
- Long-running execution streaming (no timeout)
- Authentication via JWT tokens
- Automatic reconnection support with Last-Event-ID
- Heartbeat/keepalive mechanism (ping/pong)
- Gap detection and recovery
- Graceful degradation when services unavailable

Architecture:
    Browser → WebSocket → Control Plane API → Redis → Execution Events
                                            ↓
                                        PostgreSQL (historical messages)

This replaces the SSE-based streaming with a more robust WebSocket solution.
"""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, status
from typing import Optional, Dict, Any
import structlog
import json
import asyncio
from datetime import datetime, timezone

from control_plane_api.app.middleware.auth import get_current_organization
from control_plane_api.app.lib.redis_client import get_redis_client
from control_plane_api.app.routers.executions.streaming.streamer import ExecutionStreamer
from control_plane_api.app.models.execution import Execution
from control_plane_api.app.database import get_db
from control_plane_api.app.lib.temporal_client import get_temporal_client
from sqlalchemy.orm import Session

logger = structlog.get_logger()

router = APIRouter()


class ClientConnectionManager:
    """
    Manages WebSocket connections for frontend clients.

    Features:
    - Per-organization connection limits
    - Connection tracking and cleanup
    - Statistics and monitoring
    """

    def __init__(self):
        # execution_id -> WebSocket
        self._connections: Dict[str, WebSocket] = {}

        # organization_id -> Set[execution_id]
        self._org_connections: Dict[str, set] = {}

        # Connection statistics
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
        """Register a new client WebSocket connection."""
        await websocket.accept()

        # Track connection
        self._connections[execution_id] = websocket

        if organization_id not in self._org_connections:
            self._org_connections[organization_id] = set()
        self._org_connections[organization_id].add(execution_id)

        # Update stats
        self._stats["total_connections"] += 1
        self._stats["active_connections"] = len(self._connections)

        logger.info(
            "client_websocket_connected",
            execution_id=execution_id[:8],
            organization_id=organization_id[:8],
            active_connections=self._stats["active_connections"],
        )

    async def disconnect(self, execution_id: str, organization_id: str) -> None:
        """Unregister a client WebSocket connection."""
        if execution_id in self._connections:
            del self._connections[execution_id]

        if organization_id in self._org_connections:
            self._org_connections[organization_id].discard(execution_id)
            if not self._org_connections[organization_id]:
                del self._org_connections[organization_id]

        self._stats["active_connections"] = len(self._connections)

        logger.info(
            "client_websocket_disconnected",
            execution_id=execution_id[:8],
            organization_id=organization_id[:8],
            active_connections=self._stats["active_connections"],
        )

    def get_stats(self) -> Dict[str, int]:
        """Get connection statistics."""
        return self._stats.copy()


# Global connection manager
client_manager = ClientConnectionManager()


async def send_json(websocket: WebSocket, event_type: str, data: Any) -> None:
    """
    Send JSON message via WebSocket.

    Args:
        websocket: WebSocket connection
        event_type: Event type (e.g., 'message', 'status', 'connected')
        data: Event data payload
    """
    try:
        message = {
            "type": event_type,
            **data
        }
        await websocket.send_text(json.dumps(message))
        client_manager._stats["messages_sent"] += 1
        logger.info("websocket_message_sent", event_type=event_type, data_keys=list(data.keys()))
    except Exception as e:
        logger.error("failed_to_send_websocket_message", error=str(e), event_type=event_type)
        client_manager._stats["errors"] += 1
        raise


async def handle_ping_pong(websocket: WebSocket) -> None:
    """
    Handle ping/pong heartbeat messages.

    Responds to ping messages with pong to keep connection alive.
    """
    try:
        await send_json(websocket, "pong", {"timestamp": int(datetime.now(timezone.utc).timestamp() * 1000)})
    except Exception as e:
        logger.error("failed_to_send_pong", error=str(e))


async def handle_auth(websocket: WebSocket, token: str) -> Optional[str]:
    """
    Handle authentication message.

    Args:
        websocket: WebSocket connection
        token: JWT authentication token

    Returns:
        organization_id if authentication successful, None otherwise
    """
    try:
        # Import JWT decoding utility
        from control_plane_api.app.middleware.auth import decode_jwt_token

        # Decode JWT token to extract organization ID
        decoded = decode_jwt_token(token)

        if not decoded:
            logger.error("jwt_decode_failed", reason="Invalid token format")
            await send_json(websocket, "auth_error", {
                "error": "Invalid authentication token",
                "code": "INVALID_TOKEN",
            })
            return None

        # Extract organization ID from token claims
        # Auth0 tokens store org_id in custom claims namespace
        organization_id = (
            decoded.get('https://kubiya.ai/org_id') or
            decoded.get('org_id') or
            decoded.get('organization_id')
        )

        if not organization_id:
            logger.error("org_id_missing", decoded_claims=list(decoded.keys()))
            await send_json(websocket, "auth_error", {
                "error": "Organization ID not found in token",
                "code": "ORG_ID_MISSING",
            })
            return None

        user_id = decoded.get('sub')

        logger.info(
            "websocket_authenticated",
            organization_id=organization_id[:8] if len(organization_id) > 8 else organization_id,
            user_id=user_id[:8] if user_id and len(user_id) > 8 else user_id,
        )

        # Send auth success
        await send_json(websocket, "auth_success", {
            "organization_id": organization_id,
            "user_id": user_id,
            "authenticated_at": datetime.now(timezone.utc).isoformat(),
        })

        return organization_id

    except Exception as e:
        logger.error("authentication_failed", error=str(e), error_type=type(e).__name__)
        await send_json(websocket, "auth_error", {
            "error": "Authentication failed",
            "code": "AUTH_FAILED",
        })
        return None


@router.websocket("/ws/executions/{execution_id}")
async def websocket_execution_stream(
    websocket: WebSocket,
    execution_id: str,
    last_event_id: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """
    WebSocket endpoint for execution streaming.

    Streams execution events to frontend clients with automatic reconnection support.

    Args:
        websocket: WebSocket connection
        execution_id: Execution ID to stream
        last_event_id: Last received event ID (for resumption)
        db: Database session

    Flow:
        1. Accept WebSocket connection
        2. Wait for auth message with JWT token
        3. Validate token and extract organization_id
        4. Send 'connected' event
        5. Load and stream historical messages (last 200)
        6. Subscribe to Redis for live events
        7. Stream events until execution completes or client disconnects
        8. Handle ping/pong for keepalive
        9. Support resumption via last_event_id
    """
    organization_id: Optional[str] = None
    authenticated = False

    try:
        # Accept connection first (before manager tracks it)
        await websocket.accept()

        # Track connection in manager
        client_manager._connections[execution_id] = websocket
        client_manager._org_connections.setdefault("pending", set()).add(execution_id)
        client_manager._stats["total_connections"] += 1
        client_manager._stats["active_connections"] = len(client_manager._connections)

        logger.info(
            "client_websocket_connection_started",
            execution_id=execution_id[:8],
            last_event_id=last_event_id,
        )

        # Wait for authentication message (timeout after 5 seconds)
        try:
            auth_message = await asyncio.wait_for(websocket.receive_text(), timeout=5.0)
            auth_data = json.loads(auth_message)

            if auth_data.get("type") == "auth" and "token" in auth_data:
                organization_id = await handle_auth(websocket, auth_data["token"])
                if not organization_id:
                    await websocket.close(code=4001, reason="Authentication failed")
                    return

                authenticated = True

                # Update connection with actual org_id
                # Remove from pending
                if "pending" in client_manager._org_connections:
                    client_manager._org_connections["pending"].discard(execution_id)
                    if not client_manager._org_connections["pending"]:
                        del client_manager._org_connections["pending"]

                # Add to actual org
                client_manager._org_connections.setdefault(organization_id, set()).add(execution_id)

        except asyncio.TimeoutError:
            logger.error("auth_timeout", execution_id=execution_id[:8])
            await websocket.close(code=4002, reason="Authentication timeout")
            return
        except json.JSONDecodeError:
            logger.error("invalid_auth_message", execution_id=execution_id[:8])
            await websocket.close(code=4003, reason="Invalid authentication message")
            return

        # Send connected event
        await send_json(websocket, "connected", {
            "execution_id": execution_id,
            "organization_id": organization_id,
            "connected_at": datetime.now(timezone.utc).isoformat(),
        })

        # Initialize streaming
        redis_client = get_redis_client()
        temporal_client = await get_temporal_client()

        # Get execution type from database
        execution = db.query(Execution).filter(Execution.id == execution_id).first()
        execution_type = execution.execution_type if execution else "AGENT"

        streamer = ExecutionStreamer(
            execution_id=execution_id,
            organization_id=organization_id,
            db_session=db,
            redis_client=redis_client,
            temporal_client=temporal_client,
            last_event_id=last_event_id,
            timeout_seconds=0,  # No timeout for WebSocket
            execution_type=execution_type,
        )

        logger.info("streaming_initialized", execution_id=execution_id[:8])

        # Helper to parse SSE events and convert to WebSocket JSON
        def parse_sse_event(sse_text: str) -> tuple[str, dict]:
            """Parse SSE format to (event_type, data_dict)."""
            lines = sse_text.strip().split('\n')
            event_type = "message"
            data_lines = []

            # Check for keepalive (just comment lines, no event/data)
            is_keepalive = all(line.startswith(':') or not line.strip() for line in lines)
            if is_keepalive:
                return "keepalive", {}

            for line in lines:
                if line.startswith("event: "):
                    event_type = line[7:].strip()
                elif line.startswith("data: "):
                    # Collect data line (could be multiline)
                    data_lines.append(line[6:])
                elif line and not line.startswith("id:") and not line.startswith(':') and data_lines:
                    # Continuation of data line
                    data_lines.append(line)

            # Join all data lines
            data_str = ''.join(data_lines).strip()

            try:
                data = json.loads(data_str) if data_str else {}
            except json.JSONDecodeError as e:
                logger.warning("json_decode_error", error=str(e), data_str=data_str[:200])
                data = {"raw": data_str}

            return event_type, data

        # Listen for both streaming events and client messages (ping/pong)
        async def listen_stream():
            """Listen for streaming events from ExecutionStreamer."""
            try:
                async for sse_event in streamer.stream():
                    # Parse SSE event and convert to WebSocket JSON
                    event_type, data = parse_sse_event(sse_event)

                    # Skip keepalive messages
                    if event_type == "keepalive":
                        continue

                    # DEBUG: Log what we're parsing
                    logger.info(
                        "parsed_sse_event",
                        event_type=event_type,
                        data_keys=list(data.keys()) if isinstance(data, dict) else [],
                        sse_preview=sse_event[:200] if len(sse_event) > 200 else sse_event
                    )

                    await send_json(websocket, event_type, data)
            except Exception as e:
                logger.error("streaming_error", error=str(e), error_type=type(e).__name__)
                raise

        async def listen_client():
            """Listen for client messages (ping, resume, etc.)."""
            try:
                while True:
                    message = await websocket.receive_text()
                    data = json.loads(message)

                    if data.get("type") == "ping":
                        await handle_ping_pong(websocket)

                    elif data.get("type") == "resume":
                        # Handle resume request
                        logger.info("resume_requested", execution_id=execution_id[:8], last_event_id=data.get("last_event_id"))

            except WebSocketDisconnect:
                pass
            except Exception as e:
                logger.error("client_message_error", error=str(e))

        # Run both listeners concurrently
        # When one finishes (e.g., client disconnect), cancel the other
        stream_task = asyncio.create_task(listen_stream())
        client_task = asyncio.create_task(listen_client())

        # Wait for either task to complete
        done, pending = await asyncio.wait(
            {stream_task, client_task},
            return_when=asyncio.FIRST_COMPLETED
        )

        # Cancel any pending tasks
        for task in pending:
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass

    except WebSocketDisconnect:
        logger.info("client_disconnected", execution_id=execution_id[:8])

    except Exception as e:
        logger.error(
            "websocket_error",
            execution_id=execution_id[:8],
            error=str(e),
            error_type=type(e).__name__,
        )
        try:
            await send_json(websocket, "error", {"error": str(e)})
        except:
            pass

    finally:
        # Cleanup
        if organization_id:
            await client_manager.disconnect(execution_id, organization_id)

        logger.info("client_websocket_closed", execution_id=execution_id[:8])


@router.get("/ws/stats")
async def websocket_stats():
    """
    Get WebSocket connection statistics.

    Returns statistics about active connections, messages sent, etc.
    """
    return client_manager.get_stats()
