"""Event publishing utilities for plan orchestration."""

from typing import Optional, Dict, Any
import structlog
import httpx
import json as json_lib
import os

from worker_internal.planner.event_models import PlanEventBase

logger = structlog.get_logger(__name__)


async def publish_plan_event(
    execution_id: str,
    event_type: str,
    event_data: PlanEventBase,
) -> bool:
    """
    Publish plan event via HTTP to control plane (which handles Redis).

    This approach is more reliable than direct Redis access from activities
    because the control plane manages Redis connections and event storage.
    """
    try:
        control_plane_url = os.getenv("CONTROL_PLANE_URL", "http://localhost:8000")

        # Build event message (serialize datetime objects to strings)
        event_dict = json_lib.loads(json_lib.dumps(event_data.dict(), default=str))

        message = {
            "event_type": event_type,
            "data": event_dict,
            "timestamp": event_data.timestamp.isoformat() if event_data.timestamp else None,
        }

        # Publish via HTTP to control plane
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.post(
                f"{control_plane_url}/api/v1/tasks/plan/events/{execution_id}",
                json=message,
            )

            if response.status_code in (200, 201, 202):
                logger.debug(
                    "plan_event_published",
                    execution_id=execution_id[:8],
                    event_type=event_type,
                )
                return True
            else:
                logger.warning(
                    "plan_event_publish_failed",
                    execution_id=execution_id[:8],
                    event_type=event_type,
                    status=response.status_code,
                )
                return False

    except Exception as e:
        logger.error(
            "plan_event_publish_error",
            execution_id=execution_id[:8],
            event_type=event_type,
            error=str(e),
        )
        return False
