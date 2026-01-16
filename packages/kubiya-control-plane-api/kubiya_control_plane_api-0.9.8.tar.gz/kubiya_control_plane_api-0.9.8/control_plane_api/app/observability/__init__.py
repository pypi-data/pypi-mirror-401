"""
OpenTelemetry observability module for distributed tracing.

This module provides:
- Tracer initialization and configuration
- OTLP exporter setup
- Custom span creation utilities
- Trace context propagation helpers
- Automatic endpoint instrumentation decorators

Falls back gracefully when OpenTelemetry is not available.
"""

from control_plane_api.app.observability.optional import HAS_OPENTELEMETRY

if HAS_OPENTELEMETRY:
    try:
        from control_plane_api.app.observability.tracing import (
            setup_telemetry,
            get_tracer,
            create_span_with_context,
            get_current_trace_id,
            get_current_span_id,
            add_span_event,
            add_span_error,
            shutdown_telemetry,
        )
        from control_plane_api.app.observability.decorators import (
            instrument_endpoint,
        )
        from control_plane_api.app.observability.context_logging import (
            trace_operation,
            log_db_query,
            log_llm_call,
            log_worker_operation,
            log_workflow_step,
            log_external_api_call,
            log_business_event,
            log_state_change,
            log_cache_operation,
            log_validation_result,
        )
    except ImportError:
        HAS_OPENTELEMETRY = False

if not HAS_OPENTELEMETRY:
    # No-op implementations
    async def setup_telemetry() -> None:
        """No-op setup when OpenTelemetry is not available."""
        pass

    async def shutdown_telemetry() -> None:
        """No-op shutdown when OpenTelemetry is not available."""
        pass

    def get_tracer(name: str, version: str = ""):
        """No-op tracer."""
        from control_plane_api.app.observability.optional import get_tracer as _get_tracer
        return _get_tracer(name, version)

    def create_span_with_context(*args, **kwargs):
        """No-op span creator."""
        from contextlib import nullcontext
        return nullcontext()

    def get_current_trace_id() -> str:
        """No-op trace ID getter."""
        return ""

    def get_current_span_id() -> str:
        """No-op span ID getter."""
        return ""

    def add_span_event(*args, **kwargs):
        """No-op event adder."""
        pass

    def add_span_error(*args, **kwargs):
        """No-op error adder."""
        pass

    def instrument_endpoint(func):
        """No-op decorator."""
        return func

    def trace_operation(*args, **kwargs):
        """No-op operation tracer."""
        from contextlib import nullcontext
        return nullcontext()

    # All logging helpers are no-ops
    log_db_query = trace_operation
    log_llm_call = trace_operation
    log_worker_operation = trace_operation
    log_workflow_step = trace_operation
    log_external_api_call = trace_operation
    log_business_event = trace_operation
    log_state_change = trace_operation
    log_cache_operation = trace_operation
    log_validation_result = trace_operation

__all__ = [
    # Core tracing
    "setup_telemetry",
    "get_tracer",
    "create_span_with_context",
    "get_current_trace_id",
    "get_current_span_id",
    "add_span_event",
    "add_span_error",
    "shutdown_telemetry",
    "instrument_endpoint",
    # Context logging helpers
    "trace_operation",
    "log_db_query",
    "log_llm_call",
    "log_worker_operation",
    "log_workflow_step",
    "log_external_api_call",
    "log_business_event",
    "log_state_change",
    "log_cache_operation",
    "log_validation_result",
]
