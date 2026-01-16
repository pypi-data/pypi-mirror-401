"""
OpenTelemetry tracing configuration and utilities.

This module sets up the OpenTelemetry SDK with OTLP exporter support
and provides helper functions for creating spans with organizational context.
"""

import structlog
from typing import Optional, Dict, Any
from contextlib import contextmanager

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.resources import Resource, SERVICE_NAME, SERVICE_VERSION
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter as GRPCExporter
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter as HTTPExporter
from opentelemetry.sdk.trace.sampling import (
    ParentBasedTraceIdRatio,
    ParentBased,
    ALWAYS_ON,
    ALWAYS_OFF,
)

from control_plane_api.app.config import settings

logger = structlog.get_logger(__name__)

# Global tracer instance
_tracer: Optional[trace.Tracer] = None
_tracer_provider: Optional[TracerProvider] = None
_local_storage_processor = None  # LocalStorageSpanProcessor instance


def _parse_resource_attributes() -> Dict[str, str]:
    """Parse OTEL_RESOURCE_ATTRIBUTES from environment variable.

    Format: "key1=value1,key2=value2"
    """
    attributes = {}
    if settings.OTEL_RESOURCE_ATTRIBUTES:
        for pair in settings.OTEL_RESOURCE_ATTRIBUTES.split(","):
            if "=" in pair:
                key, value = pair.split("=", 1)
                attributes[key.strip()] = value.strip()
    return attributes


def _create_sampler():
    """Create appropriate sampler based on configuration."""
    sampler_name = settings.OTEL_TRACES_SAMPLER.lower()

    if sampler_name == "always_off":
        return ALWAYS_OFF
    elif sampler_name == "always_on":
        return ALWAYS_ON
    elif sampler_name == "parentbased_always_on":
        return ParentBased(root=ALWAYS_ON)
    elif sampler_name == "parentbased_always_off":
        return ParentBased(root=ALWAYS_OFF)
    elif sampler_name == "parentbased_traceidratio":
        ratio = settings.OTEL_TRACES_SAMPLER_ARG or 1.0
        return ParentBased(root=ParentBasedTraceIdRatio(ratio))
    elif sampler_name == "traceidratio":
        ratio = settings.OTEL_TRACES_SAMPLER_ARG or 1.0
        return ParentBasedTraceIdRatio(ratio)
    else:
        logger.warning(
            "unknown_sampler_type",
            sampler=sampler_name,
            fallback="parentbased_always_on"
        )
        return ParentBased(root=ALWAYS_ON)


def setup_telemetry() -> None:
    """
    Initialize OpenTelemetry SDK with OTLP exporter and/or local storage.

    This should be called once at application startup.
    If OTEL_ENABLED is False, tracing will be disabled (no-op tracer).
    Local storage can work independently without external OTLP endpoint.
    """
    global _tracer, _tracer_provider

    if not settings.OTEL_ENABLED:
        logger.info("otel_disabled", reason="OTEL_ENABLED=false")
        # Set no-op tracer
        trace.set_tracer_provider(trace.NoOpTracerProvider())
        _tracer = trace.get_tracer(__name__)
        return

    # Check if we have any tracing destination (external OTLP or local storage)
    has_otlp_endpoint = bool(settings.OTEL_EXPORTER_OTLP_ENDPOINT)
    has_local_storage = getattr(settings, 'OTEL_LOCAL_STORAGE_ENABLED', True)

    if not has_otlp_endpoint and not has_local_storage:
        logger.warning(
            "otel_no_destination_configured",
            message="Neither OTLP endpoint nor local storage enabled, tracing disabled"
        )
        # Set no-op tracer
        trace.set_tracer_provider(trace.NoOpTracerProvider())
        _tracer = trace.get_tracer(__name__)
        return

    try:
        # Create resource with service information
        resource_attributes = {
            SERVICE_NAME: settings.OTEL_SERVICE_NAME,
            SERVICE_VERSION: settings.api_version,
            "deployment.environment": settings.environment,
        }

        # Add custom resource attributes from config
        resource_attributes.update(_parse_resource_attributes())

        resource = Resource.create(resource_attributes)

        # Create sampler
        sampler = _create_sampler()

        # Create tracer provider
        _tracer_provider = TracerProvider(resource=resource, sampler=sampler)

        # Only add OTLP exporter if endpoint is configured
        if has_otlp_endpoint:
            # Create appropriate exporter based on protocol
            if settings.OTEL_EXPORTER_OTLP_PROTOCOL == "http":
                # HTTP/protobuf exporter
                endpoint = settings.OTEL_EXPORTER_OTLP_ENDPOINT
                if not endpoint.endswith("/v1/traces"):
                    endpoint = f"{endpoint}/v1/traces"
                exporter = HTTPExporter(endpoint=endpoint)
                logger.info(
                    "otel_exporter_configured",
                    protocol="http",
                    endpoint=endpoint
                )
            else:
                # gRPC exporter (default)
                exporter = GRPCExporter(
                    endpoint=settings.OTEL_EXPORTER_OTLP_ENDPOINT,
                    insecure=True  # TODO: Configure TLS for production
                )
                logger.info(
                    "otel_exporter_configured",
                    protocol="grpc",
                    endpoint=settings.OTEL_EXPORTER_OTLP_ENDPOINT
                )

            # Add batch span processor with exporter
            span_processor = BatchSpanProcessor(exporter)
            _tracer_provider.add_span_processor(span_processor)
        else:
            logger.info(
                "otel_exporter_skipped",
                reason="No OTLP endpoint configured, using local storage only"
            )

        # Add local storage processor for observability UI
        global _local_storage_processor
        if settings.OTEL_LOCAL_STORAGE_ENABLED:
            try:
                from control_plane_api.app.observability.local_span_processor import (
                    setup_local_storage_processor,
                )
                _local_storage_processor = setup_local_storage_processor(
                    _tracer_provider,
                )
            except Exception as e:
                logger.warning(
                    "local_storage_processor_setup_failed",
                    error=str(e),
                    message="Continuing without local trace storage"
                )

        # Set global tracer provider
        trace.set_tracer_provider(_tracer_provider)

        # Create tracer instance
        _tracer = trace.get_tracer(
            instrumenting_module_name="control_plane_api",
            instrumenting_library_version=settings.api_version
        )

        logger.info(
            "otel_initialized",
            service_name=settings.OTEL_SERVICE_NAME,
            otlp_endpoint=settings.OTEL_EXPORTER_OTLP_ENDPOINT or "none",
            otlp_protocol=settings.OTEL_EXPORTER_OTLP_PROTOCOL if has_otlp_endpoint else "disabled",
            local_storage=bool(_local_storage_processor),
            sampler=settings.OTEL_TRACES_SAMPLER,
            sampler_arg=settings.OTEL_TRACES_SAMPLER_ARG,
        )

    except Exception as e:
        logger.error(
            "otel_initialization_failed",
            error=str(e),
            exc_info=True
        )
        # Fall back to no-op tracer on error
        trace.set_tracer_provider(trace.NoOpTracerProvider())
        _tracer = trace.get_tracer(__name__)


def get_tracer() -> trace.Tracer:
    """Get the global tracer instance."""
    global _tracer
    if _tracer is None:
        # Return default tracer if not initialized
        return trace.get_tracer(__name__)
    return _tracer


@contextmanager
def create_span_with_context(
    name: str,
    organization_id: Optional[str] = None,
    user_id: Optional[str] = None,
    user_email: Optional[str] = None,
    user_name: Optional[str] = None,
    user_avatar: Optional[str] = None,
    execution_id: Optional[str] = None,
    request_id: Optional[str] = None,
    **attributes: Any,
):
    """
    Create a span with standard organizational and user context.

    Args:
        name: Span name (e.g., "streaming.phase_1_connect")
        organization_id: Organization slug (e.g., "kubiya-ai")
        user_id: User UUID
        user_email: User email address
        user_name: User display name
        user_avatar: User avatar URL
        execution_id: Execution UUID (if applicable)
        request_id: Request ID from middleware
        **attributes: Additional span attributes

    Usage:
        with create_span_with_context(
            "worker.registration",
            organization_id="kubiya-ai",
            user_id="user-123",
            user_email="user@example.com",
            user_name="John Doe",
            worker_queue_id="queue-456"
        ) as span:
            # Do work
            span.set_attribute("worker.id", worker_id)
    """
    tracer = get_tracer()

    with tracer.start_as_current_span(name) as span:
        # Add standard organizational context
        if organization_id:
            span.set_attribute("organization.id", organization_id)

        if user_id:
            span.set_attribute("user.id", user_id)

        if user_email:
            span.set_attribute("user.email", user_email)

        if user_name:
            span.set_attribute("user.name", user_name)

        if user_avatar:
            span.set_attribute("user.avatar", user_avatar)

        if execution_id:
            span.set_attribute("execution.id", execution_id)

        if request_id:
            span.set_attribute("request.id", request_id)

        # Add custom attributes
        for key, value in attributes.items():
            if value is not None:
                # Convert value to string for non-primitive types
                if isinstance(value, (str, int, float, bool)):
                    span.set_attribute(key, value)
                else:
                    span.set_attribute(key, str(value))

        yield span


def get_current_trace_id() -> Optional[str]:
    """
    Get the current trace ID as a hex string.

    Returns:
        Trace ID in format: "4bf92f3577b34da6a3ce929d0e0e4736"
        None if no active span
    """
    span = trace.get_current_span()
    if span and span.is_recording():
        trace_id = span.get_span_context().trace_id
        return format(trace_id, '032x')
    return None


def get_current_span_id() -> Optional[str]:
    """
    Get the current span ID as a hex string.

    Returns:
        16-character hex string of the 64-bit span ID, or None if no active span
    """
    span = trace.get_current_span()
    if span and span.is_recording():
        span_id = span.get_span_context().span_id
        return format(span_id, '016x')
    return None


def add_span_event(name: str, attributes: Optional[Dict[str, Any]] = None) -> None:
    """
    Add an event (log) to the current span for better trace visibility.

    This makes logs visible in the Jaeger UI as span events.

    Args:
        name: Event name (e.g., "Database query started", "LLM response received")
        attributes: Optional key-value pairs with event details

    Example:
        add_span_event("Agent execution started", {"agent_id": "abc123", "prompt": "Deploy app"})
        # ... do work ...
        add_span_event("Agent execution completed", {"status": "success", "duration_ms": 1234})
    """
    span = trace.get_current_span()
    if span and span.is_recording():
        event_attrs = attributes or {}
        span.add_event(name, event_attrs)


def add_span_error(error: Exception, attributes: Optional[Dict[str, Any]] = None) -> None:
    """
    Record an error in the current span with full context.

    Args:
        error: The exception that occurred
        attributes: Optional additional context about the error

    Example:
        try:
            risky_operation()
        except Exception as e:
            add_span_error(e, {"operation": "database_write", "table": "users"})
            raise
    """
    span = trace.get_current_span()
    if span and span.is_recording():
        from opentelemetry.trace import StatusCode

        span.set_status(StatusCode.ERROR, str(error))
        span.record_exception(error)

        if attributes:
            for key, value in attributes.items():
                span.set_attribute(f"error.{key}", str(value))


def shutdown_telemetry() -> None:
    """
    Shutdown the OpenTelemetry SDK and flush remaining spans.

    This should be called during application shutdown.
    """
    global _tracer_provider

    if _tracer_provider:
        try:
            _tracer_provider.shutdown()
            logger.info("otel_shutdown_complete")
        except Exception as e:
            logger.error("otel_shutdown_failed", error=str(e), exc_info=True)
