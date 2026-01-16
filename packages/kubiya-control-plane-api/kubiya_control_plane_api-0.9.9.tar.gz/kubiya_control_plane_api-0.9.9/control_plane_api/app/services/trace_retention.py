"""
Trace Retention Service.

Handles automatic cleanup of old traces based on configurable retention period.
Also provides storage statistics per organization.

Features:
- Configurable retention period (default: 30 days)
- Per-organization storage stats
- Batch deletion for performance
- Scheduled cleanup job support
"""

import structlog
from datetime import datetime, timezone, timedelta
from typing import Optional, Dict, Any

from sqlalchemy.orm import Session
from sqlalchemy import func, delete

from control_plane_api.app.config import settings
from control_plane_api.app.database import get_session_local
from control_plane_api.app.models.trace import Trace, Span

logger = structlog.get_logger()

# Configuration
RETENTION_DAYS = getattr(settings, 'OTEL_LOCAL_STORAGE_RETENTION_DAYS', 30)
BATCH_SIZE = 1000  # Number of traces to delete per batch


class TraceRetentionService:
    """Service for managing trace retention and cleanup."""

    def __init__(self, retention_days: int = None):
        """
        Initialize the retention service.

        Args:
            retention_days: Number of days to retain traces (default from config)
        """
        self.retention_days = retention_days or RETENTION_DAYS
        self._stats = {
            "last_cleanup": None,
            "traces_deleted": 0,
            "spans_deleted": 0,
            "errors": 0,
        }

    def get_cutoff_date(self) -> datetime:
        """Get the cutoff date for trace retention."""
        return datetime.now(timezone.utc) - timedelta(days=self.retention_days)

    async def cleanup_old_traces(
        self,
        organization_id: Optional[str] = None,
        batch_size: int = BATCH_SIZE,
    ) -> Dict[str, int]:
        """
        Delete traces older than the retention period.

        Args:
            organization_id: Optional org to limit cleanup to
            batch_size: Number of traces to delete per batch

        Returns:
            Dict with deletion statistics
        """
        cutoff_date = self.get_cutoff_date()
        total_traces_deleted = 0
        total_spans_deleted = 0

        logger.info(
            "trace_cleanup_starting",
            retention_days=self.retention_days,
            cutoff_date=cutoff_date.isoformat(),
            organization_id=organization_id,
        )

        try:
            SessionLocal = get_session_local()
            session = SessionLocal()

            try:
                while True:
                    # Find old traces to delete
                    query = session.query(Trace).filter(
                        Trace.started_at < cutoff_date
                    )

                    if organization_id:
                        query = query.filter(Trace.organization_id == organization_id)

                    # Get batch of trace IDs
                    traces_to_delete = query.limit(batch_size).all()

                    if not traces_to_delete:
                        break

                    trace_ids = [t.trace_id for t in traces_to_delete]

                    # Count spans being deleted (for stats)
                    span_count = session.query(func.count(Span.id)).filter(
                        Span.trace_id.in_(trace_ids)
                    ).scalar()

                    # Delete traces (cascade will delete spans due to FK)
                    for trace in traces_to_delete:
                        session.delete(trace)

                    session.commit()

                    total_traces_deleted += len(trace_ids)
                    total_spans_deleted += span_count

                    logger.info(
                        "trace_cleanup_batch_completed",
                        traces_deleted=len(trace_ids),
                        spans_deleted=span_count,
                        total_traces_deleted=total_traces_deleted,
                    )

            except Exception as e:
                session.rollback()
                self._stats["errors"] += 1
                logger.error("trace_cleanup_batch_failed", error=str(e), exc_info=True)
                raise

            finally:
                session.close()

        except Exception as e:
            self._stats["errors"] += 1
            logger.error("trace_cleanup_failed", error=str(e), exc_info=True)
            raise

        # Update stats
        self._stats["last_cleanup"] = datetime.now(timezone.utc).isoformat()
        self._stats["traces_deleted"] += total_traces_deleted
        self._stats["spans_deleted"] += total_spans_deleted

        logger.info(
            "trace_cleanup_completed",
            total_traces_deleted=total_traces_deleted,
            total_spans_deleted=total_spans_deleted,
            retention_days=self.retention_days,
        )

        return {
            "traces_deleted": total_traces_deleted,
            "spans_deleted": total_spans_deleted,
            "cutoff_date": cutoff_date.isoformat(),
        }

    async def get_storage_stats(
        self,
        organization_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Get storage statistics for traces.

        Args:
            organization_id: Optional org to get stats for

        Returns:
            Dict with storage statistics
        """
        try:
            SessionLocal = get_session_local()
            session = SessionLocal()

            try:
                # Base queries
                trace_query = session.query(Trace)
                span_query = session.query(Span)

                if organization_id:
                    trace_query = trace_query.filter(Trace.organization_id == organization_id)
                    span_query = span_query.filter(Span.organization_id == organization_id)

                # Total counts
                total_traces = trace_query.count()
                total_spans = span_query.count()

                # Counts by status
                success_count = trace_query.filter(Trace.status == "success").count()
                error_count = trace_query.filter(Trace.status == "error").count()
                running_count = trace_query.filter(Trace.status == "running").count()

                # Date range
                oldest_trace = trace_query.order_by(Trace.started_at.asc()).first()
                newest_trace = trace_query.order_by(Trace.started_at.desc()).first()

                # Average metrics
                avg_duration = session.query(func.avg(Trace.duration_ms)).filter(
                    Trace.duration_ms.isnot(None)
                )
                avg_span_count = session.query(func.avg(Trace.span_count))

                if organization_id:
                    avg_duration = avg_duration.filter(Trace.organization_id == organization_id)
                    avg_span_count = avg_span_count.filter(Trace.organization_id == organization_id)

                avg_duration_val = avg_duration.scalar()
                avg_span_count_val = avg_span_count.scalar()

                # Retention info
                cutoff_date = self.get_cutoff_date()
                traces_to_expire = trace_query.filter(Trace.started_at < cutoff_date).count()

                return {
                    "total_traces": total_traces,
                    "total_spans": total_spans,
                    "status_breakdown": {
                        "success": success_count,
                        "error": error_count,
                        "running": running_count,
                    },
                    "date_range": {
                        "oldest": oldest_trace.started_at.isoformat() if oldest_trace else None,
                        "newest": newest_trace.started_at.isoformat() if newest_trace else None,
                    },
                    "averages": {
                        "duration_ms": round(avg_duration_val, 2) if avg_duration_val else None,
                        "span_count": round(avg_span_count_val, 2) if avg_span_count_val else None,
                    },
                    "retention": {
                        "retention_days": self.retention_days,
                        "cutoff_date": cutoff_date.isoformat(),
                        "traces_to_expire": traces_to_expire,
                    },
                    "organization_id": organization_id,
                    "retrieved_at": datetime.now(timezone.utc).isoformat(),
                }

            finally:
                session.close()

        except Exception as e:
            logger.error("get_storage_stats_failed", error=str(e), exc_info=True)
            raise

    def get_service_stats(self) -> Dict[str, Any]:
        """Get retention service statistics."""
        return {
            **self._stats,
            "retention_days": self.retention_days,
        }


# Singleton instance
_retention_service: Optional[TraceRetentionService] = None


def get_retention_service() -> TraceRetentionService:
    """Get the singleton retention service instance."""
    global _retention_service
    if _retention_service is None:
        _retention_service = TraceRetentionService()
    return _retention_service


async def run_cleanup_job():
    """
    Run the trace cleanup job.

    This function can be called from a scheduled job (e.g., Temporal workflow,
    cron job, or APScheduler).
    """
    service = get_retention_service()
    result = await service.cleanup_old_traces()

    logger.info(
        "scheduled_trace_cleanup_completed",
        **result
    )

    return result
