"""
Optional OpenTelemetry imports for environments with size constraints.

This module provides safe imports for OpenTelemetry that gracefully degrade
when the packages are not available (e.g., in Vercel serverless deployments
where package size matters).
"""

import os
from typing import Optional, Any
from contextlib import nullcontext

# Check if we should disable tracing entirely
TRACING_ENABLED = os.getenv("TRACING_ENABLED", "true").lower() in ("true", "1", "yes")

# Try to import OpenTelemetry, but fall back gracefully
try:
    if not TRACING_ENABLED:
        raise ImportError("Tracing disabled via TRACING_ENABLED env var")

    from opentelemetry import trace as _trace
    from opentelemetry.trace import Status, StatusCode, Span, Tracer

    HAS_OPENTELEMETRY = True
    trace = _trace

except ImportError:
    HAS_OPENTELEMETRY = False

    # Create no-op implementations
    class NoOpSpan:
        """No-op span that does nothing."""
        def set_attribute(self, key: str, value: Any) -> None:
            pass

        def set_attributes(self, attributes: dict) -> None:
            pass

        def set_status(self, status: Any) -> None:
            pass

        def record_exception(self, exception: Exception) -> None:
            pass

        def is_recording(self) -> bool:
            return False

        def get_span_context(self) -> Any:
            return None

        def __enter__(self):
            return self

        def __exit__(self, *args):
            pass

    class NoOpTracer:
        """No-op tracer that does nothing."""
        def start_as_current_span(self, name: str, *args, **kwargs):
            return nullcontext(NoOpSpan())

        def start_span(self, name: str, *args, **kwargs):
            return NoOpSpan()

    class NoOpTracerProvider:
        """No-op tracer provider."""
        def get_tracer(self, *args, **kwargs) -> NoOpTracer:
            return NoOpTracer()

    class NoOpTrace:
        """No-op trace module replacement."""
        @staticmethod
        def get_tracer(name: str, version: str = "") -> NoOpTracer:
            return NoOpTracer()

        @staticmethod
        def get_current_span() -> NoOpSpan:
            return NoOpSpan()

        @staticmethod
        def get_tracer_provider() -> NoOpTracerProvider:
            return NoOpTracerProvider()

        @staticmethod
        def set_tracer_provider(provider: Any) -> None:
            pass

    # Status and StatusCode placeholders
    class Status:
        """No-op Status."""
        def __init__(self, status_code: Any, description: str = ""):
            pass

    class StatusCode:
        """No-op StatusCode."""
        OK = "OK"
        ERROR = "ERROR"
        UNSET = "UNSET"

    # Type hints
    Span = NoOpSpan
    Tracer = NoOpTracer

    # Create the no-op trace module
    trace = NoOpTrace()


def get_tracer(name: str, version: str = "") -> Tracer:
    """Get a tracer, or a no-op tracer if OpenTelemetry is not available."""
    return trace.get_tracer(name, version)


def get_current_span() -> Span:
    """Get the current span, or a no-op span if OpenTelemetry is not available."""
    return trace.get_current_span()
