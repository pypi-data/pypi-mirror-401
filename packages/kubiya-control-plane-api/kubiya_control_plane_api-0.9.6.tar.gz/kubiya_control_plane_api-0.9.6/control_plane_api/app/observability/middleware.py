"""
OpenTelemetry middleware for FastAPI.

This module provides middleware to:
- Add trace ID to response headers (X-Trace-ID)
- Enrich spans with organizational and user context from request.state
- Set span status based on HTTP status codes
"""

import structlog
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from opentelemetry import trace
from opentelemetry.trace import Status, StatusCode

logger = structlog.get_logger(__name__)


class TraceContextMiddleware(BaseHTTPMiddleware):
    """
    Middleware to enrich spans with organizational context and add trace ID to responses.

    This middleware should be added AFTER the OpenTelemetry FastAPI instrumentation,
    so that it can enrich the automatically created spans.
    """

    # Paths to exclude from tracing (health checks, metrics, etc.)
    EXCLUDED_PATHS = {
        "/api/health",
        "/health",
        "/health/live",
        "/health/ready",
        "/health/detailed",
        "/health/event-bus",
        "/health/temporal-credentials",
        "/ready",
        "/metrics",
        "/favicon.ico"
    }

    async def dispatch(self, request: Request, call_next):
        """
        Process request and enrich span with organizational context.

        Args:
            request: Incoming HTTP request
            call_next: Next middleware in chain

        Returns:
            HTTP response with X-Trace-ID header
        """
        # Skip tracing for health checks and other excluded paths
        if request.url.path in self.EXCLUDED_PATHS:
            return await call_next(request)

        # Get current span (created by FastAPI instrumentation)
        span = trace.get_current_span()

        # Add span event for request received
        if span and span.is_recording():
            from control_plane_api.app.observability import add_span_event
            add_span_event(
                f"HTTP request received: {request.method} {request.url.path}",
                {
                    "http.method": request.method,
                    "http.path": request.url.path,
                    "http.query": request.url.query if request.url.query else "",
                    "client.host": request.client.host if request.client else "unknown",
                }
            )

        # Capture request body for non-GET requests (for debugging)
        request_body = None
        if request.method in ("POST", "PUT", "PATCH"):
            try:
                body_bytes = await request.body()
                if body_bytes and len(body_bytes) < 10000:  # Only capture if < 10KB
                    request_body = body_bytes.decode('utf-8')
                    # Re-create request with body for downstream handlers
                    async def receive():
                        return {"type": "http.request", "body": body_bytes}
                    request._receive = receive
            except Exception as e:
                logger.warning("failed_to_capture_request_body", error=str(e))

        # Enrich span with organizational context from request.state
        # These are set by the auth dependency (get_current_organization)
        if span and span.is_recording():
            try:
                # Debug: Check if organization exists
                has_org = hasattr(request.state, "organization")
                logger.debug(
                    "trace_context_check",
                    has_organization=has_org,
                    path=request.url.path
                )

                # Add organization context
                if has_org:
                    org = request.state.organization
                    if isinstance(org, dict):
                        span.set_attribute("organization.id", org.get("id", ""))
                        span.set_attribute("organization.name", org.get("name", ""))

                        from control_plane_api.app.observability import add_span_event
                        add_span_event(
                            "Organizational context added to span",
                            {
                                "organization.id": org.get("id", ""),
                                "organization.name": org.get("name", ""),
                                "user.email": org.get("user_email", ""),
                            }
                        )

                        logger.info(
                            "span_enriched_with_org",
                            org_id=org.get("id"),
                            path=request.url.path
                        )

                        # Add user context
                        if org.get("user_id"):
                            span.set_attribute("user.id", org["user_id"])
                        if org.get("user_email"):
                            span.set_attribute("user.email", org["user_email"])
                        if org.get("user_name"):
                            span.set_attribute("user.name", org["user_name"])
                        if org.get("user_avatar"):
                            span.set_attribute("user.avatar", org["user_avatar"])

                # Add request ID
                if hasattr(request.state, "request_id"):
                    span.set_attribute("request.id", request.state.request_id)

                # Add request path and method
                span.set_attribute("http.route", request.url.path)
                span.set_attribute("http.method", request.method)

                # Add query parameters
                if request.url.query:
                    span.set_attribute("http.query", request.url.query)

                # Add request body for debugging (sanitize sensitive data)
                if request_body:
                    # Sanitize passwords, tokens, etc.
                    sanitized_body = request_body
                    for sensitive_key in ["password", "token", "secret", "api_key", "apiKey"]:
                        if sensitive_key in sanitized_body.lower():
                            sanitized_body = sanitized_body[:100] + "...[REDACTED]"
                            break
                    span.set_attribute("http.request.body", sanitized_body[:500])  # Max 500 chars

            except Exception as e:
                logger.warning(
                    "span_enrichment_failed",
                    error=str(e),
                    exc_info=True
                )

        # Get trace ID before processing request for logging correlation
        trace_id = None
        span_id = None
        if span and span.is_recording():
            trace_id = format(span.get_span_context().trace_id, '032x')
            span_id = format(span.get_span_context().span_id, '016x')

        # Process request
        response = await call_next(request)

        # Add trace ID to response headers and capture response
        if span and span.is_recording():
            try:
                response.headers["X-Trace-ID"] = trace_id
                response.headers["X-Span-ID"] = span_id

                # Set span status based on HTTP status code
                from control_plane_api.app.observability import add_span_event
                if response.status_code >= 500:
                    span.set_status(Status(StatusCode.ERROR, f"HTTP {response.status_code}"))
                    span.set_attribute("error", True)
                    add_span_event(
                        f"HTTP response: Server error {response.status_code}",
                        {
                            "http.status_code": response.status_code,
                            "status": "error",
                        }
                    )
                elif response.status_code >= 400:
                    # Client errors are not span errors (they're expected)
                    span.set_attribute("http.client_error", True)
                    span.set_status(Status(StatusCode.OK))
                    add_span_event(
                        f"HTTP response: Client error {response.status_code}",
                        {
                            "http.status_code": response.status_code,
                            "status": "client_error",
                        }
                    )
                else:
                    span.set_status(Status(StatusCode.OK))
                    add_span_event(
                        f"HTTP response: Success {response.status_code}",
                        {
                            "http.status_code": response.status_code,
                            "status": "success",
                        }
                    )

                # Add HTTP status code attribute
                span.set_attribute("http.status_code", response.status_code)

                # NOW enrich span with user context (AFTER route handler ran, so organization is set)
                # This is the correct place because auth dependency sets request.state.organization
                if hasattr(request.state, "organization"):
                    org = request.state.organization
                    if isinstance(org, dict):
                        span.set_attribute("organization.id", org.get("id", ""))
                        if org.get("user_id"):
                            span.set_attribute("user.id", org["user_id"])
                        if org.get("user_email"):
                            span.set_attribute("user.email", org["user_email"])
                        if org.get("user_name"):
                            span.set_attribute("user.name", org["user_name"])
                        if org.get("user_avatar"):
                            span.set_attribute("user.avatar", org["user_avatar"])

                # Log request completion with trace correlation
                logger.info(
                    "http_request_completed",
                    method=request.method,
                    path=request.url.path,
                    status_code=response.status_code,
                    trace_id=trace_id,
                    span_id=span_id,
                    organization_id=getattr(request.state, "organization", {}).get("id") if hasattr(request.state, "organization") else None
                )

            except Exception as e:
                logger.warning(
                    "trace_id_header_failed",
                    error=str(e),
                    exc_info=True
                )

        return response
