"""
WebSocket Endpoint for Trace Streaming.

Provides persistent WebSocket connections for frontend clients to receive
real-time trace and span updates for the observability UI.

Features:
- Organization-scoped live trace streaming
- Single trace detail streaming (for waterfall view)
- Authentication via JWT tokens
- Heartbeat/keepalive mechanism
- Redis pub/sub for event distribution

Architecture:
    Browser → WebSocket → Control Plane API → Redis Pub/Sub → Trace Events
                                            ↓
                                        LocalStorageSpanProcessor

This enables real-time updates in the Observability UI without polling.
"""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from typing import Optional, Dict, Any, Set
import structlog
import json
import asyncio
from datetime import datetime, timezone

from control_plane_api.app.lib.redis_client import get_redis_client
from control_plane_api.app.database import get_db
from control_plane_api.app.models.trace import Trace
from sqlalchemy.orm import Session

logger = structlog.get_logger()

router = APIRouter()


class TraceConnectionManager:
    """
    Manages WebSocket connections for trace streaming.

    Features:
    - Per-organization trace list streaming
    - Per-trace detail streaming
    - Connection tracking and cleanup
    """

    def __init__(self):
        # organization_id -> Set[WebSocket]
        self._org_connections: Dict[str, Set[WebSocket]] = {}

        # trace_id -> Set[WebSocket]
        self._trace_connections: Dict[str, Set[WebSocket]] = {}

        # WebSocket -> organization_id
        self._ws_to_org: Dict[WebSocket, str] = {}

        # WebSocket -> trace_id
        self._ws_to_trace: Dict[WebSocket, str] = {}

        # Statistics
        self._stats = {
            "total_connections": 0,
            "active_connections": 0,
            "messages_sent": 0,
            "errors": 0,
        }

    async def connect_org(
        self,
        organization_id: str,
        websocket: WebSocket,
    ) -> None:
        """Register a new organization-level WebSocket connection."""
        await websocket.accept()

        if organization_id not in self._org_connections:
            self._org_connections[organization_id] = set()
        self._org_connections[organization_id].add(websocket)
        self._ws_to_org[websocket] = organization_id

        self._stats["total_connections"] += 1
        self._stats["active_connections"] += 1

        logger.info(
            "trace_websocket_org_connected",
            organization_id=organization_id[:8] if len(organization_id) > 8 else organization_id,
            active_connections=self._stats["active_connections"],
        )

    async def connect_trace(
        self,
        trace_id: str,
        organization_id: str,
        websocket: WebSocket,
    ) -> None:
        """Register a new trace-level WebSocket connection."""
        await websocket.accept()

        if trace_id not in self._trace_connections:
            self._trace_connections[trace_id] = set()
        self._trace_connections[trace_id].add(websocket)
        self._ws_to_trace[websocket] = trace_id
        self._ws_to_org[websocket] = organization_id

        self._stats["total_connections"] += 1
        self._stats["active_connections"] += 1

        logger.info(
            "trace_websocket_trace_connected",
            trace_id=trace_id[:8],
            organization_id=organization_id[:8] if len(organization_id) > 8 else organization_id,
            active_connections=self._stats["active_connections"],
        )

    async def disconnect(self, websocket: WebSocket) -> None:
        """Unregister a WebSocket connection."""
        # Remove from org connections
        org_id = self._ws_to_org.pop(websocket, None)
        if org_id and org_id in self._org_connections:
            self._org_connections[org_id].discard(websocket)
            if not self._org_connections[org_id]:
                del self._org_connections[org_id]

        # Remove from trace connections
        trace_id = self._ws_to_trace.pop(websocket, None)
        if trace_id and trace_id in self._trace_connections:
            self._trace_connections[trace_id].discard(websocket)
            if not self._trace_connections[trace_id]:
                del self._trace_connections[trace_id]

        self._stats["active_connections"] = max(0, self._stats["active_connections"] - 1)

        logger.info(
            "trace_websocket_disconnected",
            organization_id=org_id[:8] if org_id and len(org_id) > 8 else org_id,
            trace_id=trace_id[:8] if trace_id else None,
            active_connections=self._stats["active_connections"],
        )

    def get_org_connections(self, organization_id: str) -> Set[WebSocket]:
        """Get all WebSocket connections for an organization."""
        return self._org_connections.get(organization_id, set())

    def get_trace_connections(self, trace_id: str) -> Set[WebSocket]:
        """Get all WebSocket connections for a trace."""
        return self._trace_connections.get(trace_id, set())

    def get_stats(self) -> Dict[str, int]:
        """Get connection statistics."""
        return self._stats.copy()


# Global connection manager
trace_manager = TraceConnectionManager()


async def send_json(websocket: WebSocket, event_type: str, data: Any) -> bool:
    """
    Send JSON message via WebSocket.

    Returns True if successful, False if failed.
    """
    try:
        message = {
            "type": event_type,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            **(data if isinstance(data, dict) else {"data": data})
        }
        await websocket.send_text(json.dumps(message, default=str))
        trace_manager._stats["messages_sent"] += 1
        return True
    except Exception as e:
        logger.error("failed_to_send_websocket_message", error=str(e), event_type=event_type)
        trace_manager._stats["errors"] += 1
        return False


async def handle_auth(websocket: WebSocket, token: str) -> Optional[str]:
    """
    Handle authentication message.

    Returns organization_id if authentication successful, None otherwise.
    """
    try:
        from control_plane_api.app.middleware.auth import decode_jwt_token

        decoded = decode_jwt_token(token)

        if not decoded:
            logger.error("jwt_decode_failed", reason="Invalid token format")
            await send_json(websocket, "auth_error", {
                "error": "Invalid authentication token",
                "code": "INVALID_TOKEN",
            })
            return None

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
            "trace_websocket_authenticated",
            organization_id=organization_id[:8] if len(organization_id) > 8 else organization_id,
            user_id=user_id[:8] if user_id and len(user_id) > 8 else user_id,
        )

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


async def subscribe_to_redis_channel(
    websocket: WebSocket,
    channel: str,
    organization_id: str,
    trace_id: Optional[str] = None,
):
    """
    Subscribe to Redis pub/sub channel and forward events to WebSocket.

    This runs until the WebSocket disconnects or an error occurs.
    """
    redis_client = get_redis_client()
    if not redis_client:
        logger.warning("redis_not_available", channel=channel)
        return

    try:
        # Get the underlying redis connection for pub/sub
        # Note: This depends on the type of redis client
        if hasattr(redis_client, '_redis'):
            # StandardRedisClient
            pubsub = redis_client._redis.pubsub()
            await pubsub.subscribe(channel)

            logger.info(
                "redis_channel_subscribed",
                channel=channel,
                organization_id=organization_id[:8] if len(organization_id) > 8 else organization_id,
            )

            # Listen for messages
            while True:
                try:
                    message = await pubsub.get_message(
                        ignore_subscribe_messages=True,
                        timeout=1.0
                    )

                    if message and message.get("type") == "message":
                        data = message.get("data")
                        if isinstance(data, bytes):
                            data = data.decode("utf-8")

                        try:
                            event = json.loads(data)
                            event_type = event.get("type", "trace_event")

                            # Filter by trace_id if this is a trace-specific connection
                            if trace_id:
                                event_trace_id = event.get("data", {}).get("trace_id")
                                if event_trace_id != trace_id:
                                    continue

                            success = await send_json(websocket, event_type, event.get("data", {}))
                            if not success:
                                break

                        except json.JSONDecodeError:
                            logger.warning("invalid_redis_message", data=str(data)[:100])

                except asyncio.TimeoutError:
                    # Send keepalive ping
                    try:
                        await send_json(websocket, "ping", {})
                    except Exception:
                        break

        else:
            # UpstashRedisClient doesn't support pub/sub subscription
            # Fall back to polling approach
            logger.warning(
                "redis_pubsub_not_supported",
                client_type=type(redis_client).__name__,
                message="Upstash REST API doesn't support pub/sub subscription",
            )

            # Simple keepalive loop until disconnect
            while True:
                await asyncio.sleep(30)
                try:
                    await send_json(websocket, "ping", {})
                except Exception:
                    break

    except asyncio.CancelledError:
        logger.info("redis_subscription_cancelled", channel=channel)
        raise
    except Exception as e:
        logger.error("redis_subscription_error", error=str(e), channel=channel)
    finally:
        # Cleanup
        if hasattr(redis_client, '_redis') and 'pubsub' in dir():
            try:
                await pubsub.unsubscribe(channel)
                await pubsub.close()
            except Exception:
                pass


@router.websocket("/ws/traces/live")
async def websocket_trace_list_stream(
    websocket: WebSocket,
    db: Session = Depends(get_db),
):
    """
    WebSocket endpoint for live trace list streaming.

    Streams all new traces and trace updates for the authenticated organization.

    Flow:
        1. Accept WebSocket connection
        2. Wait for auth message with JWT token
        3. Validate token and extract organization_id
        4. Send 'connected' event
        5. Subscribe to Redis channel for trace events
        6. Stream events until client disconnects
    """
    organization_id: Optional[str] = None

    try:
        await websocket.accept()

        logger.info("trace_list_websocket_started")

        # Wait for authentication message
        try:
            auth_message = await asyncio.wait_for(websocket.receive_text(), timeout=5.0)
            auth_data = json.loads(auth_message)

            if auth_data.get("type") == "auth" and "token" in auth_data:
                organization_id = await handle_auth(websocket, auth_data["token"])
                if not organization_id:
                    await websocket.close(code=4001, reason="Authentication failed")
                    return
            else:
                await websocket.close(code=4003, reason="Invalid authentication message")
                return

        except asyncio.TimeoutError:
            logger.error("trace_auth_timeout")
            await websocket.close(code=4002, reason="Authentication timeout")
            return
        except json.JSONDecodeError:
            logger.error("trace_invalid_auth_message")
            await websocket.close(code=4003, reason="Invalid authentication message")
            return

        # Track connection
        if organization_id not in trace_manager._org_connections:
            trace_manager._org_connections[organization_id] = set()
        trace_manager._org_connections[organization_id].add(websocket)
        trace_manager._ws_to_org[websocket] = organization_id
        trace_manager._stats["active_connections"] += 1

        # Send connected event
        await send_json(websocket, "connected", {
            "organization_id": organization_id,
            "connected_at": datetime.now(timezone.utc).isoformat(),
            "subscription": "trace_list",
        })

        # Create tasks for Redis subscription and client message handling
        redis_task = asyncio.create_task(
            subscribe_to_redis_channel(
                websocket,
                f"traces:{organization_id}",
                organization_id,
            )
        )

        # Handle incoming messages (ping/pong, etc.)
        try:
            while True:
                try:
                    message = await asyncio.wait_for(websocket.receive_text(), timeout=60.0)
                    data = json.loads(message)

                    if data.get("type") == "ping":
                        await send_json(websocket, "pong", {
                            "timestamp": int(datetime.now(timezone.utc).timestamp() * 1000)
                        })

                except asyncio.TimeoutError:
                    # Send ping to keep connection alive
                    await send_json(websocket, "ping", {})

        except WebSocketDisconnect:
            logger.info("trace_list_websocket_disconnected")

        finally:
            redis_task.cancel()
            try:
                await redis_task
            except asyncio.CancelledError:
                pass

    except WebSocketDisconnect:
        logger.info("trace_list_websocket_disconnected_early")
    except Exception as e:
        logger.error("trace_list_websocket_error", error=str(e), exc_info=True)
    finally:
        if organization_id:
            await trace_manager.disconnect(websocket)


@router.websocket("/ws/traces/{trace_id}")
async def websocket_trace_detail_stream(
    websocket: WebSocket,
    trace_id: str,
    db: Session = Depends(get_db),
):
    """
    WebSocket endpoint for single trace detail streaming.

    Streams span updates for a specific trace (for waterfall view).

    Flow:
        1. Accept WebSocket connection
        2. Wait for auth message with JWT token
        3. Validate token and verify trace belongs to organization
        4. Send 'connected' event with initial trace data
        5. Subscribe to Redis channel filtered by trace_id
        6. Stream span events until client disconnects or trace completes
    """
    organization_id: Optional[str] = None

    try:
        await websocket.accept()

        logger.info("trace_detail_websocket_started", trace_id=trace_id[:8])

        # Wait for authentication message
        try:
            auth_message = await asyncio.wait_for(websocket.receive_text(), timeout=5.0)
            auth_data = json.loads(auth_message)

            if auth_data.get("type") == "auth" and "token" in auth_data:
                organization_id = await handle_auth(websocket, auth_data["token"])
                if not organization_id:
                    await websocket.close(code=4001, reason="Authentication failed")
                    return
            else:
                await websocket.close(code=4003, reason="Invalid authentication message")
                return

        except asyncio.TimeoutError:
            logger.error("trace_detail_auth_timeout", trace_id=trace_id[:8])
            await websocket.close(code=4002, reason="Authentication timeout")
            return
        except json.JSONDecodeError:
            logger.error("trace_detail_invalid_auth_message", trace_id=trace_id[:8])
            await websocket.close(code=4003, reason="Invalid authentication message")
            return

        # Verify trace exists and belongs to organization
        trace = db.query(Trace).filter(
            Trace.trace_id == trace_id,
            Trace.organization_id == organization_id,
        ).first()

        if not trace:
            await send_json(websocket, "error", {
                "error": f"Trace {trace_id} not found",
                "code": "TRACE_NOT_FOUND",
            })
            await websocket.close(code=4004, reason="Trace not found")
            return

        # Track connection
        if trace_id not in trace_manager._trace_connections:
            trace_manager._trace_connections[trace_id] = set()
        trace_manager._trace_connections[trace_id].add(websocket)
        trace_manager._ws_to_trace[websocket] = trace_id
        trace_manager._ws_to_org[websocket] = organization_id
        trace_manager._stats["active_connections"] += 1

        # Send connected event with trace info
        await send_json(websocket, "connected", {
            "trace_id": trace_id,
            "organization_id": organization_id,
            "trace_name": trace.name,
            "trace_status": trace.status.value if trace.status else "running",
            "connected_at": datetime.now(timezone.utc).isoformat(),
            "subscription": "trace_detail",
        })

        # Create tasks for Redis subscription and client message handling
        redis_task = asyncio.create_task(
            subscribe_to_redis_channel(
                websocket,
                f"traces:{organization_id}",
                organization_id,
                trace_id=trace_id,  # Filter by this trace
            )
        )

        # Handle incoming messages (ping/pong, etc.)
        try:
            while True:
                try:
                    message = await asyncio.wait_for(websocket.receive_text(), timeout=60.0)
                    data = json.loads(message)

                    if data.get("type") == "ping":
                        await send_json(websocket, "pong", {
                            "timestamp": int(datetime.now(timezone.utc).timestamp() * 1000)
                        })

                except asyncio.TimeoutError:
                    # Check if trace is still running
                    db.refresh(trace)
                    if trace.status and trace.status.value != "running":
                        await send_json(websocket, "trace_completed", {
                            "trace_id": trace_id,
                            "status": trace.status.value,
                            "duration_ms": trace.duration_ms,
                        })
                        break

                    # Send ping to keep connection alive
                    await send_json(websocket, "ping", {})

        except WebSocketDisconnect:
            logger.info("trace_detail_websocket_disconnected", trace_id=trace_id[:8])

        finally:
            redis_task.cancel()
            try:
                await redis_task
            except asyncio.CancelledError:
                pass

    except WebSocketDisconnect:
        logger.info("trace_detail_websocket_disconnected_early", trace_id=trace_id[:8])
    except Exception as e:
        logger.error("trace_detail_websocket_error", error=str(e), trace_id=trace_id[:8], exc_info=True)
    finally:
        if organization_id:
            await trace_manager.disconnect(websocket)
