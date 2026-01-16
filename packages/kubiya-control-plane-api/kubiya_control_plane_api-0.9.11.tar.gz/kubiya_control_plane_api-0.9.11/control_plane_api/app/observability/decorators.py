"""
Decorators for automatic endpoint instrumentation.

These decorators wrap FastAPI endpoints with OpenTelemetry spans automatically.
"""

import functools
from typing import Callable, Any
from fastapi import Request
from control_plane_api.app.observability import (
    create_span_with_context,
    add_span_event,
    add_span_error,
)


def instrument_endpoint(operation_name: str = None):
    """
    Decorator to automatically instrument FastAPI endpoints with OpenTelemetry spans.

    Usage:
        @router.post("/agents")
        @instrument_endpoint("agents.create")
        async def create_agent(
            request: AgentRequest,
            organization: dict = Depends(get_current_organization),
        ):
            # Your code here
            return {"agent_id": "123"}

    This automatically:
    - Creates a span with operation name "agents.create"
    - Adds organization context
    - Logs the start of the operation
    - Logs success/failure
    - Captures errors

    Args:
        operation_name: Name for the span (e.g., "agents.create", "executions.list")
                       If not provided, uses module.function_name
    """
    def decorator(func: Callable) -> Callable:
        # Determine operation name
        span_name = operation_name or f"{func.__module__}.{func.__name__}"

        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            import time
            start_time = time.time()

            # Extract organization from kwargs (injected by FastAPI Depends)
            organization = kwargs.get('organization', {})
            org_id = organization.get('id') if isinstance(organization, dict) else None
            user_email = organization.get('user_email') if isinstance(organization, dict) else None

            # Extract request if available
            request = kwargs.get('request')
            request_id = None
            request_method = None
            request_path = None
            if isinstance(request, Request):
                request_id = request.headers.get('X-Request-ID')
                request_method = request.method
                request_path = request.url.path

            # Build detailed attributes
            attributes = {
                "endpoint.name": span_name,
                "function.name": func.__name__,
            }

            if request_id:
                attributes['request.id'] = request_id
            if request_method:
                attributes['http.method'] = request_method
            if request_path:
                attributes['http.path'] = request_path
            if org_id:
                attributes['organization.id'] = org_id
            if user_email:
                attributes['user.email'] = user_email

            # Add any ID parameters from path
            id_params = {}
            for key, value in kwargs.items():
                if key.endswith('_id') and isinstance(value, str):
                    attributes[key] = value
                    id_params[key] = value

            # Log request payload info (non-sensitive)
            request_data = {}
            for key, value in kwargs.items():
                if key not in ['request', 'organization', 'db', 'background_tasks']:
                    # Log type info for complex objects
                    if hasattr(value, '__class__'):
                        request_data[key] = f"<{value.__class__.__name__}>"
                    elif isinstance(value, (str, int, bool, float)):
                        # Log simple types directly (truncated)
                        str_val = str(value)
                        request_data[key] = str_val[:100] if len(str_val) > 100 else str_val

            # Create span
            with create_span_with_context(
                span_name,
                organization_id=org_id,
                attributes=attributes
            ) as span:
                try:
                    # Log detailed operation start
                    start_event_attrs = {
                        **attributes,
                        "timestamp": time.time(),
                    }
                    if id_params:
                        start_event_attrs['resource_ids'] = str(id_params)
                    if request_data:
                        start_event_attrs['request_params'] = str(request_data)

                    add_span_event(
                        f"Starting {span_name}",
                        start_event_attrs
                    )

                    # Execute the actual endpoint function
                    result = await func(*args, **kwargs)

                    # Calculate duration
                    duration_ms = (time.time() - start_time) * 1000

                    # Extract result metadata if available
                    result_info = {}
                    if isinstance(result, dict):
                        # Log IDs from result
                        for key in ['id', 'agent_id', 'execution_id', 'worker_id', 'queue_id']:
                            if key in result:
                                result_info[key] = result[key]
                        # Log status if present
                        if 'status' in result:
                            result_info['result_status'] = result['status']
                    elif isinstance(result, list):
                        result_info['result_count'] = len(result)
                        # Sample first item if list contains dicts
                        if result and isinstance(result[0], dict):
                            result_info['sample_keys'] = list(result[0].keys())[:5]

                    # Log detailed success
                    success_attrs = {
                        "operation": span_name,
                        "duration_ms": f"{duration_ms:.2f}",
                        "status": "success",
                    }
                    if result_info:
                        success_attrs.update(result_info)

                    add_span_event(
                        f"Completed {span_name} successfully",
                        success_attrs
                    )

                    span.set_attribute("operation.status", "success")
                    span.set_attribute("operation.duration_ms", duration_ms)
                    if result_info:
                        for key, val in result_info.items():
                            span.set_attribute(f"result.{key}", str(val))

                    return result

                except Exception as e:
                    # Calculate duration even on error
                    duration_ms = (time.time() - start_time) * 1000

                    # Log detailed error
                    error_attrs = {
                        "operation": span_name,
                        "error_type": type(e).__name__,
                        "error_message": str(e)[:200],  # Truncate long errors
                        "duration_ms": f"{duration_ms:.2f}",
                        "status": "error",
                    }

                    add_span_event(
                        f"Failed {span_name}",
                        error_attrs
                    )

                    add_span_error(e, error_attrs)
                    span.set_attribute("operation.status", "error")
                    span.set_attribute("operation.duration_ms", duration_ms)
                    raise

        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs):
            import time
            start_time = time.time()

            # Extract organization from kwargs
            organization = kwargs.get('organization', {})
            org_id = organization.get('id') if isinstance(organization, dict) else None
            user_email = organization.get('user_email') if isinstance(organization, dict) else None

            # Extract request if available
            request = kwargs.get('request')
            request_id = None
            request_method = None
            request_path = None
            if isinstance(request, Request):
                request_id = request.headers.get('X-Request-ID')
                request_method = request.method
                request_path = request.url.path

            # Build detailed attributes
            attributes = {
                "endpoint.name": span_name,
                "function.name": func.__name__,
            }

            if request_id:
                attributes['request.id'] = request_id
            if request_method:
                attributes['http.method'] = request_method
            if request_path:
                attributes['http.path'] = request_path
            if org_id:
                attributes['organization.id'] = org_id
            if user_email:
                attributes['user.email'] = user_email

            # Add any ID parameters from path
            id_params = {}
            for key, value in kwargs.items():
                if key.endswith('_id') and isinstance(value, str):
                    attributes[key] = value
                    id_params[key] = value

            # Log request payload info (non-sensitive)
            request_data = {}
            for key, value in kwargs.items():
                if key not in ['request', 'organization', 'db', 'background_tasks']:
                    if hasattr(value, '__class__'):
                        request_data[key] = f"<{value.__class__.__name__}>"
                    elif isinstance(value, (str, int, bool, float)):
                        str_val = str(value)
                        request_data[key] = str_val[:100] if len(str_val) > 100 else str_val

            with create_span_with_context(
                span_name,
                organization_id=org_id,
                attributes=attributes
            ) as span:
                try:
                    # Log detailed operation start
                    start_event_attrs = {
                        **attributes,
                        "timestamp": time.time(),
                    }
                    if id_params:
                        start_event_attrs['resource_ids'] = str(id_params)
                    if request_data:
                        start_event_attrs['request_params'] = str(request_data)

                    add_span_event(
                        f"Starting {span_name}",
                        start_event_attrs
                    )

                    # Execute function
                    result = func(*args, **kwargs)

                    # Calculate duration
                    duration_ms = (time.time() - start_time) * 1000

                    # Extract result metadata
                    result_info = {}
                    if isinstance(result, dict):
                        for key in ['id', 'agent_id', 'execution_id', 'worker_id', 'queue_id']:
                            if key in result:
                                result_info[key] = result[key]
                        if 'status' in result:
                            result_info['result_status'] = result['status']
                    elif isinstance(result, list):
                        result_info['result_count'] = len(result)
                        if result and isinstance(result[0], dict):
                            result_info['sample_keys'] = list(result[0].keys())[:5]

                    # Log detailed success
                    success_attrs = {
                        "operation": span_name,
                        "duration_ms": f"{duration_ms:.2f}",
                        "status": "success",
                    }
                    if result_info:
                        success_attrs.update(result_info)

                    add_span_event(
                        f"Completed {span_name} successfully",
                        success_attrs
                    )

                    span.set_attribute("operation.status", "success")
                    span.set_attribute("operation.duration_ms", duration_ms)
                    if result_info:
                        for key, val in result_info.items():
                            span.set_attribute(f"result.{key}", str(val))

                    return result

                except Exception as e:
                    # Calculate duration even on error
                    duration_ms = (time.time() - start_time) * 1000

                    # Log detailed error
                    error_attrs = {
                        "operation": span_name,
                        "error_type": type(e).__name__,
                        "error_message": str(e)[:200],
                        "duration_ms": f"{duration_ms:.2f}",
                        "status": "error",
                    }

                    add_span_event(
                        f"Failed {span_name}",
                        error_attrs
                    )

                    add_span_error(e, error_attrs)
                    span.set_attribute("operation.status", "error")
                    span.set_attribute("operation.duration_ms", duration_ms)
                    raise

        # Return appropriate wrapper based on whether function is async
        import inspect
        if inspect.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper

    return decorator
