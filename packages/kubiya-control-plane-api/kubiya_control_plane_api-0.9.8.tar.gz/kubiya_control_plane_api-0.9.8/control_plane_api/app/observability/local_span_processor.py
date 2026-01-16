"""
LocalStorageSpanProcessor - Async OTEL SpanProcessor for local trace storage.

This processor intercepts completed spans from the OTEL SDK and stores them
in PostgreSQL for local querying. It's designed to be fully async and non-blocking
to avoid impacting application performance.

Features:
- Fully async database operations using asyncio
- Non-blocking span queuing with bounded queue
- Bulk inserts for performance
- Publishes events to Redis for real-time WebSocket streaming
- Configurable via OTEL_LOCAL_STORAGE_ENABLED env var
- Graceful degradation on errors - never blocks the main application

Usage:
    from control_plane_api.app.observability.local_span_processor import (
        LocalStorageSpanProcessor,
        setup_local_storage_processor
    )

    # In setup_telemetry():
    setup_local_storage_processor(tracer_provider)
"""

import structlog
import asyncio
import threading
from collections import deque
from typing import Optional, List, Dict, Any, Deque
from datetime import datetime, timezone
import json

from opentelemetry.sdk.trace import SpanProcessor, ReadableSpan
from opentelemetry.trace import SpanKind as OTELSpanKind
from opentelemetry.trace.status import StatusCode

from control_plane_api.app.config import settings

logger = structlog.get_logger(__name__)

# Configuration from settings
LOCAL_STORAGE_ENABLED = getattr(settings, 'OTEL_LOCAL_STORAGE_ENABLED', True)
LOCAL_STORAGE_BATCH_SIZE = getattr(settings, 'OTEL_LOCAL_STORAGE_BATCH_SIZE', 100)
LOCAL_STORAGE_FLUSH_INTERVAL = getattr(settings, 'OTEL_LOCAL_STORAGE_FLUSH_INTERVAL', 1000)  # ms

# Maximum queue size to prevent memory issues
MAX_QUEUE_SIZE = 10000


def _span_kind_to_string(kind: OTELSpanKind) -> str:
    """Convert OTEL SpanKind to our enum string"""
    mapping = {
        OTELSpanKind.INTERNAL: "INTERNAL",
        OTELSpanKind.SERVER: "SERVER",
        OTELSpanKind.CLIENT: "CLIENT",
        OTELSpanKind.PRODUCER: "PRODUCER",
        OTELSpanKind.CONSUMER: "CONSUMER",
    }
    return mapping.get(kind, "INTERNAL")


def _status_code_to_string(status: StatusCode) -> str:
    """Convert OTEL StatusCode to our enum string"""
    mapping = {
        StatusCode.UNSET: "UNSET",
        StatusCode.OK: "OK",
        StatusCode.ERROR: "ERROR",
    }
    return mapping.get(status, "UNSET")


def _extract_attributes(span: ReadableSpan) -> Dict[str, Any]:
    """Extract span attributes as a dictionary"""
    attrs = {}
    if span.attributes:
        for key, value in span.attributes.items():
            if isinstance(value, (str, int, float, bool)):
                attrs[key] = value
            elif isinstance(value, (list, tuple)):
                attrs[key] = list(value)
            else:
                attrs[key] = str(value)
    return attrs


def _extract_resource_attributes(span: ReadableSpan) -> Dict[str, Any]:
    """Extract resource attributes as a dictionary"""
    attrs = {}
    if span.resource and span.resource.attributes:
        for key, value in span.resource.attributes.items():
            if isinstance(value, (str, int, float, bool)):
                attrs[key] = value
            elif isinstance(value, (list, tuple)):
                attrs[key] = list(value)
            else:
                attrs[key] = str(value)
    return attrs


def _extract_events(span: ReadableSpan) -> List[Dict[str, Any]]:
    """Extract span events as a list of dictionaries"""
    events = []
    if span.events:
        for event in span.events:
            event_dict = {
                "name": event.name,
                "timestamp": event.timestamp,
                "attributes": {}
            }
            if event.attributes:
                for key, value in event.attributes.items():
                    if isinstance(value, (str, int, float, bool)):
                        event_dict["attributes"][key] = value
                    else:
                        event_dict["attributes"][key] = str(value)
            events.append(event_dict)
    return events


def _extract_links(span: ReadableSpan) -> List[Dict[str, Any]]:
    """Extract span links as a list of dictionaries"""
    links = []
    if span.links:
        for link in span.links:
            link_dict = {
                "trace_id": format(link.context.trace_id, '032x'),
                "span_id": format(link.context.span_id, '016x'),
                "attributes": {}
            }
            if link.attributes:
                for key, value in link.attributes.items():
                    if isinstance(value, (str, int, float, bool)):
                        link_dict["attributes"][key] = value
                    else:
                        link_dict["attributes"][key] = str(value)
            links.append(link_dict)
    return links


class LocalStorageSpanProcessor(SpanProcessor):
    """
    Async SpanProcessor that stores spans locally in PostgreSQL.

    Design principles:
    - NEVER block the main application thread
    - Use bounded queues to prevent memory issues
    - Bulk insert for database efficiency
    - Graceful degradation on errors
    """

    def __init__(
        self,
        enabled: bool = True,
        batch_size: int = 100,
        flush_interval_ms: int = 1000,
    ):
        self.enabled = enabled
        self.batch_size = batch_size
        self.flush_interval_ms = flush_interval_ms

        # Thread-safe bounded queue using deque with maxlen
        self._span_queue: Deque[Dict[str, Any]] = deque(maxlen=MAX_QUEUE_SIZE)
        self._queue_lock = threading.Lock()

        # Async event loop for background processing
        self._loop: Optional[asyncio.AbstractEventLoop] = None
        self._task: Optional[asyncio.Task] = None
        self._shutdown_event = asyncio.Event()

        # Stats for monitoring
        self._stats = {
            "spans_received": 0,
            "spans_stored": 0,
            "spans_dropped": 0,
            "batch_inserts": 0,
            "errors": 0,
        }

        if self.enabled:
            self._start_async_worker()
            logger.info(
                "local_storage_span_processor_initialized",
                batch_size=self.batch_size,
                flush_interval_ms=self.flush_interval_ms,
            )
        else:
            logger.info("local_storage_span_processor_disabled")

    def _start_async_worker(self):
        """Start the async background worker in a separate thread"""
        def run_async_loop():
            self._loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self._loop)
            try:
                self._loop.run_until_complete(self._async_batch_worker())
            except Exception as e:
                logger.error("async_worker_crashed", error=str(e), exc_info=True)
            finally:
                self._loop.close()

        thread = threading.Thread(
            target=run_async_loop,
            name="LocalStorageAsyncWorker",
            daemon=True,
        )
        thread.start()

    async def _async_batch_worker(self):
        """Async worker that batches and inserts spans using raw asyncpg"""
        import asyncpg
        import ssl as ssl_module

        flush_interval_sec = self.flush_interval_ms / 1000.0

        # Get database URL from settings
        database_url = settings.database_url
        if not database_url:
            logger.warning("async_batch_worker_no_db", message="DATABASE_URL not configured, spans will not be stored")
            return

        # Convert to asyncpg format
        if database_url.startswith("postgresql://"):
            asyncpg_url = database_url.replace("postgresql://", "postgres://", 1)
        else:
            asyncpg_url = database_url

        # Remove sslmode from URL - we'll handle SSL separately
        import re
        asyncpg_url = re.sub(r'[?&]sslmode=[^&]*', '', asyncpg_url)
        asyncpg_url = asyncpg_url.rstrip('?').replace('&&', '&').rstrip('&')

        # Check if SSL is needed
        requires_ssl = 'sslmode' in database_url and 'sslmode=disable' not in database_url

        ssl_context = None
        if requires_ssl:
            ssl_context = ssl_module.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl_module.CERT_NONE

        logger.info("async_batch_worker_starting", ssl_enabled=requires_ssl)

        while True:
            try:
                # Wait for flush interval
                await asyncio.sleep(flush_interval_sec)

                # Check for shutdown
                if self._shutdown_event.is_set():
                    await self._flush_batch_asyncpg(asyncpg_url, ssl_context)
                    break

                # Flush current batch
                await self._flush_batch_asyncpg(asyncpg_url, ssl_context)

            except Exception as e:
                self._stats["errors"] += 1
                logger.error("async_batch_worker_error", error=str(e), exc_info=True)
                await asyncio.sleep(1)  # Back off on error

    async def _flush_batch_asyncpg(self, db_url: str, ssl_context):
        """Flush pending spans to database using raw asyncpg"""
        import asyncpg

        # Get batch from queue (thread-safe)
        batch = []
        with self._queue_lock:
            while self._span_queue and len(batch) < self.batch_size:
                batch.append(self._span_queue.popleft())

        if not batch:
            return

        try:
            # Create a fresh connection for each batch
            # prepared_statement_cache_size=0 is critical for PgBouncer
            conn = await asyncpg.connect(
                db_url,
                ssl=ssl_context,
                statement_cache_size=0,  # Disable statement cache for PgBouncer
            )

            try:
                await self._bulk_insert_spans_asyncpg(conn, batch)
                self._stats["spans_stored"] += len(batch)
                self._stats["batch_inserts"] += 1

                logger.debug(
                    "batch_flushed",
                    spans=len(batch),
                    queue_size=len(self._span_queue),
                )
            finally:
                await conn.close()

        except Exception as e:
            self._stats["errors"] += 1
            logger.error("batch_flush_failed", error=str(e), spans=len(batch))

    async def _bulk_insert_spans_asyncpg(self, conn, batch: List[Dict[str, Any]]):
        """Bulk insert spans using raw asyncpg (PgBouncer compatible)"""
        # Group spans by trace_id for processing
        traces_to_create = {}
        traces_to_complete = {}  # Root spans that have ended
        traces_user_info = {}  # Track user info from ANY span that has it
        spans_data = []
        trace_span_counts = {}  # Count spans per trace
        trace_error_counts = {}  # Count errors per trace

        for span_data in batch:
            trace_id = span_data["trace_id"]
            org_id = span_data.get("organization_id")

            if not org_id:
                continue

            # Track span counts per trace
            trace_span_counts[trace_id] = trace_span_counts.get(trace_id, 0) + 1

            # Track error counts
            if span_data["status_code"] == "ERROR":
                trace_error_counts[trace_id] = trace_error_counts.get(trace_id, 0) + 1

            # Extract user info from ANY span that has it (not just root spans)
            # The HTTP root span from FastAPI Instrumentor has user attributes set by auth middleware
            span_user_email = span_data["attributes"].get("user.email")
            span_user_name = span_data["attributes"].get("user.name")
            if span_user_email or span_user_name:
                # Found user info on this span - track it for the trace
                if trace_id not in traces_user_info:
                    traces_user_info[trace_id] = {}
                # Use first non-null values found
                if span_user_email and not traces_user_info[trace_id].get("user_email"):
                    traces_user_info[trace_id]["user_email"] = span_user_email
                if span_user_name and not traces_user_info[trace_id].get("user_name"):
                    traces_user_info[trace_id]["user_name"] = span_user_name
                if span_data["attributes"].get("user.id") and not traces_user_info[trace_id].get("user_id"):
                    traces_user_info[trace_id]["user_id"] = span_data["attributes"].get("user.id")
                if span_data["attributes"].get("user.avatar") and not traces_user_info[trace_id].get("user_avatar"):
                    traces_user_info[trace_id]["user_avatar"] = span_data["attributes"].get("user.avatar")

            # Handle root spans (no parent) - these define the trace
            if span_data["parent_span_id"] is None:
                service_name = span_data["resource_attributes"].get("service.name", "unknown")

                # Determine status based on span status
                if span_data["status_code"] == "ERROR":
                    trace_status = "error"
                elif span_data.get("end_time_unix_nano"):
                    trace_status = "success"  # Completed without error
                else:
                    trace_status = "running"

                # Calculate duration in ms if span has ended
                duration_ms = None
                if span_data.get("duration_ns"):
                    duration_ms = span_data["duration_ns"] // 1_000_000

                # Get user info - prefer from tracked user info, fall back to this span's attributes
                user_info = traces_user_info.get(trace_id, {})
                user_id = user_info.get("user_id") or span_data["attributes"].get("user.id")
                user_email = user_info.get("user_email") or span_data["attributes"].get("user.email")
                user_name = user_info.get("user_name") or span_data["attributes"].get("user.name")
                user_avatar = user_info.get("user_avatar") or span_data["attributes"].get("user.avatar")

                trace_record = {
                    "trace_id": trace_id,
                    "organization_id": org_id,
                    "name": span_data["name"],
                    "service_name": service_name,
                    "status": trace_status,
                    "user_id": user_id,
                    "user_email": user_email,
                    "user_name": user_name,
                    "user_avatar": user_avatar,
                    "execution_id": span_data["attributes"].get("execution.id"),
                    "duration_ms": duration_ms,
                }

                # Always create trace first, then update if completed
                traces_to_create[trace_id] = trace_record
                if trace_status in ("success", "error"):
                    # Mark for completion update after creation
                    traces_to_complete[trace_id] = trace_record

            spans_data.append({
                "trace_id": trace_id,
                "span_id": span_data["span_id"],
                "parent_span_id": span_data["parent_span_id"],
                "organization_id": org_id,
                "name": span_data["name"],
                "kind": span_data["kind"],
                "status_code": span_data["status_code"],
                "status_message": span_data.get("status_message"),
                "start_time_unix_nano": span_data["start_time_unix_nano"],
                "end_time_unix_nano": span_data.get("end_time_unix_nano"),
                "duration_ns": span_data.get("duration_ns"),
                "attributes": span_data["attributes"],
                "resource_attributes": span_data["resource_attributes"],
                "events": span_data["events"],
                "links": span_data["links"],
            })

        # Use a transaction for atomicity
        async with conn.transaction():
            # Insert new traces using raw asyncpg execute
            # Use DO UPDATE to set user info if it's provided and current values are NULL
            # This handles the case where trace was created by a non-root span before the root span ends
            for trace in traces_to_create.values():
                await conn.execute(
                    """
                    INSERT INTO traces (trace_id, organization_id, name, service_name, status, user_id, user_email, user_name, user_avatar, execution_id, span_count, error_count)
                    VALUES ($1, $2, $3, $4, $5::trace_status, $6, $7, $8, $9, $10, 0, 0)
                    ON CONFLICT (trace_id) DO UPDATE SET
                        user_id = COALESCE(traces.user_id, EXCLUDED.user_id),
                        user_email = COALESCE(traces.user_email, EXCLUDED.user_email),
                        user_name = COALESCE(traces.user_name, EXCLUDED.user_name),
                        user_avatar = COALESCE(traces.user_avatar, EXCLUDED.user_avatar),
                        updated_at = NOW()
                    """,
                    trace["trace_id"],
                    trace["organization_id"],
                    trace["name"],
                    trace["service_name"],
                    trace["status"],
                    trace["user_id"],
                    trace["user_email"],
                    trace["user_name"],
                    trace["user_avatar"],
                    trace["execution_id"],
                )

            # Insert spans using raw asyncpg execute
            for span in spans_data:
                await conn.execute(
                    """
                    INSERT INTO spans (trace_id, span_id, parent_span_id, organization_id, name, kind, status_code, status_message, start_time_unix_nano, end_time_unix_nano, duration_ns, attributes, resource_attributes, events, links)
                    VALUES ($1, $2, $3, $4, $5, $6::span_kind, $7::span_status_code, $8, $9, $10, $11, $12::jsonb, $13::jsonb, $14::jsonb, $15::jsonb)
                    ON CONFLICT (trace_id, span_id) DO UPDATE SET
                        end_time_unix_nano = EXCLUDED.end_time_unix_nano,
                        duration_ns = EXCLUDED.duration_ns,
                        status_code = EXCLUDED.status_code,
                        status_message = EXCLUDED.status_message
                    """,
                    span["trace_id"],
                    span["span_id"],
                    span["parent_span_id"],
                    span["organization_id"],
                    span["name"],
                    span["kind"],
                    span["status_code"],
                    span["status_message"],
                    span["start_time_unix_nano"],
                    span["end_time_unix_nano"],
                    span["duration_ns"],
                    json.dumps(span["attributes"]),
                    json.dumps(span["resource_attributes"]),
                    json.dumps(span["events"]),
                    json.dumps(span["links"]),
                )

            # Update span counts for all traces in this batch
            for trace_id, count in trace_span_counts.items():
                error_count = trace_error_counts.get(trace_id, 0)
                await conn.execute(
                    """
                    UPDATE traces
                    SET span_count = span_count + $1,
                        error_count = error_count + $2,
                        updated_at = NOW()
                    WHERE trace_id = $3
                    """,
                    count,
                    error_count,
                    trace_id,
                )

            # Complete traces that have finished root spans
            for trace_id, trace in traces_to_complete.items():
                await conn.execute(
                    """
                    UPDATE traces
                    SET status = $1::trace_status,
                        duration_ms = $2,
                        ended_at = NOW(),
                        updated_at = NOW()
                    WHERE trace_id = $3
                    """,
                    trace["status"],
                    trace["duration_ms"],
                    trace_id,
                )

            # Update user info for traces where we found it on any span
            # This handles the case where trace was created before HTTP root span ended
            for trace_id, user_info in traces_user_info.items():
                if user_info:
                    await conn.execute(
                        """
                        UPDATE traces
                        SET user_id = COALESCE(user_id, $1),
                            user_email = COALESCE(user_email, $2),
                            user_name = COALESCE(user_name, $3),
                            user_avatar = COALESCE(user_avatar, $4),
                            updated_at = NOW()
                        WHERE trace_id = $5
                        """,
                        user_info.get("user_id"),
                        user_info.get("user_email"),
                        user_info.get("user_name"),
                        user_info.get("user_avatar"),
                        trace_id,
                    )

    def on_start(self, span: ReadableSpan, parent_context) -> None:
        """Called when a span starts - non-blocking"""
        # We don't store on start, only on end
        pass

    def on_end(self, span: ReadableSpan) -> None:
        """Called when a span ends - queue for async storage (non-blocking)"""
        if not self.enabled:
            return

        self._stats["spans_received"] += 1

        try:
            span_data = self._extract_span_data(span)

            # Non-blocking queue add
            with self._queue_lock:
                if len(self._span_queue) >= MAX_QUEUE_SIZE:
                    self._stats["spans_dropped"] += 1
                    # Queue is full, drop oldest
                    self._span_queue.popleft()
                self._span_queue.append(span_data)

        except Exception as e:
            self._stats["errors"] += 1
            logger.warning("span_extraction_failed", error=str(e))

    def _extract_span_data(self, span: ReadableSpan) -> Dict[str, Any]:
        """Extract all data from a span for storage"""
        span_context = span.get_span_context()
        trace_id = format(span_context.trace_id, '032x')
        span_id = format(span_context.span_id, '016x')

        parent_span_id = None
        if span.parent:
            parent_span_id = format(span.parent.span_id, '016x')

        attributes = _extract_attributes(span)
        org_id = attributes.get("organization.id") or attributes.get("organization_id")

        duration_ns = None
        if span.end_time and span.start_time:
            duration_ns = span.end_time - span.start_time

        return {
            "trace_id": trace_id,
            "span_id": span_id,
            "parent_span_id": parent_span_id,
            "organization_id": org_id,
            "name": span.name,
            "kind": _span_kind_to_string(span.kind),
            "status_code": _status_code_to_string(span.status.status_code),
            "status_message": span.status.description,
            "start_time_unix_nano": span.start_time,
            "end_time_unix_nano": span.end_time,
            "duration_ns": duration_ns,
            "attributes": attributes,
            "resource_attributes": _extract_resource_attributes(span),
            "events": _extract_events(span),
            "links": _extract_links(span),
        }

    def shutdown(self) -> None:
        """Shutdown the processor and flush remaining spans"""
        logger.info("local_storage_span_processor_shutting_down", stats=self._stats)

        if self._loop and self._loop.is_running():
            # Signal shutdown
            self._loop.call_soon_threadsafe(self._shutdown_event.set)

        logger.info("local_storage_span_processor_shutdown_complete", stats=self._stats)

    def force_flush(self, timeout_millis: int = 30000) -> bool:
        """Force flush all pending spans"""
        if not self.enabled:
            return True
        # Async flush will happen on next interval
        return True

    def get_stats(self) -> Dict[str, int]:
        """Get processor statistics"""
        return dict(self._stats)


def setup_local_storage_processor(
    tracer_provider,
) -> Optional[LocalStorageSpanProcessor]:
    """
    Set up and add the LocalStorageSpanProcessor to a TracerProvider.

    Args:
        tracer_provider: The TracerProvider to add the processor to

    Returns:
        The created LocalStorageSpanProcessor, or None if disabled
    """
    if not LOCAL_STORAGE_ENABLED:
        logger.info("local_storage_disabled", reason="OTEL_LOCAL_STORAGE_ENABLED=false")
        return None

    processor = LocalStorageSpanProcessor(
        enabled=True,
        batch_size=LOCAL_STORAGE_BATCH_SIZE,
        flush_interval_ms=LOCAL_STORAGE_FLUSH_INTERVAL,
    )

    tracer_provider.add_span_processor(processor)

    logger.info(
        "local_storage_processor_added",
        batch_size=LOCAL_STORAGE_BATCH_SIZE,
        flush_interval_ms=LOCAL_STORAGE_FLUSH_INTERVAL,
    )

    return processor
