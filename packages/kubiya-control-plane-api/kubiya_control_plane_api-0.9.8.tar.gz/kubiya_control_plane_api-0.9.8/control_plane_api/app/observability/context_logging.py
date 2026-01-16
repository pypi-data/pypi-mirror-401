"""
Rich contextual logging utilities for business logic and internal operations.

This module provides helpers to add detailed span events and logs throughout
the application, making traces rich with business context.
"""

import time
import structlog
from typing import Any, Dict, Optional
from contextlib import contextmanager
from control_plane_api.app.observability import (
    create_span_with_context,
    add_span_event,
    add_span_error,
)

logger = structlog.get_logger(__name__)


@contextmanager
def trace_operation(
    operation_name: str,
    **attributes
):
    """
    Context manager for tracing any operation with automatic timing and logging.

    Usage:
        with trace_operation("database.query", table="agents", action="select"):
            result = db.query(Agent).all()

        with trace_operation("llm.call", model="gpt-4", prompt_length=len(prompt)):
            response = llm.complete(prompt)
    """
    start_time = time.time()

    # Extract org context if present
    org_id = attributes.pop('organization_id', None)

    with create_span_with_context(operation_name, organization_id=org_id, attributes=attributes) as span:
        try:
            # Log operation start with all context
            add_span_event(
                f"Starting {operation_name}",
                {
                    **attributes,
                    "timestamp": start_time,
                }
            )

            logger.info(
                f"{operation_name}.started",
                operation=operation_name,
                **attributes
            )

            yield span

            # Calculate duration
            duration_ms = (time.time() - start_time) * 1000

            # Log success
            add_span_event(
                f"Completed {operation_name}",
                {
                    "duration_ms": f"{duration_ms:.2f}",
                    "status": "success",
                }
            )

            logger.info(
                f"{operation_name}.completed",
                operation=operation_name,
                duration_ms=duration_ms,
                status="success",
            )

            span.set_attribute("operation.status", "success")
            span.set_attribute("operation.duration_ms", duration_ms)

        except Exception as e:
            # Calculate duration even on error
            duration_ms = (time.time() - start_time) * 1000

            # Log error with context
            add_span_event(
                f"Failed {operation_name}",
                {
                    "error_type": type(e).__name__,
                    "error_message": str(e)[:200],
                    "duration_ms": f"{duration_ms:.2f}",
                    "status": "error",
                }
            )

            logger.error(
                f"{operation_name}.failed",
                operation=operation_name,
                error_type=type(e).__name__,
                error_message=str(e),
                duration_ms=duration_ms,
                exc_info=True,
            )

            add_span_error(e, {"operation": operation_name})
            span.set_attribute("operation.status", "error")
            span.set_attribute("operation.duration_ms", duration_ms)
            raise


def log_db_query(
    table: str,
    action: str,
    filters: Optional[Dict[str, Any]] = None,
    result_count: Optional[int] = None,
    duration_ms: Optional[float] = None,
):
    """
    Log database query with context.

    Args:
        table: Table name (e.g., "agents", "executions")
        action: Query action (e.g., "select", "insert", "update", "delete")
        filters: Query filters applied
        result_count: Number of results returned
        duration_ms: Query duration in milliseconds
    """
    attrs = {
        "db.table": table,
        "db.action": action,
    }

    if filters:
        attrs["db.filters"] = str(filters)[:200]
    if result_count is not None:
        attrs["db.result_count"] = result_count
    if duration_ms is not None:
        attrs["db.duration_ms"] = f"{duration_ms:.2f}"

    add_span_event(
        f"Database {action} on {table}",
        attrs
    )

    logger.info(
        "database.query",
        **attrs
    )


def log_llm_call(
    model: str,
    prompt_length: int,
    response_length: Optional[int] = None,
    tokens_used: Optional[int] = None,
    duration_ms: Optional[float] = None,
    error: Optional[str] = None,
):
    """
    Log LLM API call with context.

    Args:
        model: Model name (e.g., "gpt-4", "claude-3-opus")
        prompt_length: Length of prompt in characters
        response_length: Length of response in characters
        tokens_used: Total tokens consumed
        duration_ms: Call duration in milliseconds
        error: Error message if call failed
    """
    attrs = {
        "llm.model": model,
        "llm.prompt_length": prompt_length,
    }

    if response_length is not None:
        attrs["llm.response_length"] = response_length
    if tokens_used is not None:
        attrs["llm.tokens_used"] = tokens_used
    if duration_ms is not None:
        attrs["llm.duration_ms"] = f"{duration_ms:.2f}"

    if error:
        attrs["llm.error"] = error
        add_span_event(f"LLM call failed: {model}", attrs)
        logger.error("llm.call_failed", **attrs)
    else:
        add_span_event(f"LLM call completed: {model}", attrs)
        logger.info("llm.call_success", **attrs)


def log_worker_operation(
    worker_id: str,
    operation: str,
    task_type: Optional[str] = None,
    status: Optional[str] = None,
    **extra_attrs
):
    """
    Log worker operation with context.

    Args:
        worker_id: Worker identifier
        operation: Operation type (e.g., "heartbeat", "task_start", "task_complete")
        task_type: Type of task being processed
        status: Current status
        **extra_attrs: Additional attributes
    """
    attrs = {
        "worker.id": worker_id,
        "worker.operation": operation,
    }

    if task_type:
        attrs["worker.task_type"] = task_type
    if status:
        attrs["worker.status"] = status

    attrs.update(extra_attrs)

    add_span_event(
        f"Worker {operation}: {worker_id}",
        attrs
    )

    logger.info(
        "worker.operation",
        **attrs
    )


def log_workflow_step(
    workflow_id: str,
    step_name: str,
    status: str,
    input_summary: Optional[str] = None,
    output_summary: Optional[str] = None,
    duration_ms: Optional[float] = None,
    error: Optional[str] = None,
):
    """
    Log Temporal workflow step with context.

    Args:
        workflow_id: Workflow run ID
        step_name: Name of the workflow step/activity
        status: Status (e.g., "started", "completed", "failed")
        input_summary: Summary of input parameters
        output_summary: Summary of output/result
        duration_ms: Step duration in milliseconds
        error: Error message if step failed
    """
    attrs = {
        "workflow.id": workflow_id,
        "workflow.step": step_name,
        "workflow.status": status,
    }

    if input_summary:
        attrs["workflow.input"] = input_summary[:200]
    if output_summary:
        attrs["workflow.output"] = output_summary[:200]
    if duration_ms is not None:
        attrs["workflow.duration_ms"] = f"{duration_ms:.2f}"
    if error:
        attrs["workflow.error"] = error[:200]

    add_span_event(
        f"Workflow step {status}: {step_name}",
        attrs
    )

    logger.info(
        "workflow.step",
        **attrs
    )


def log_external_api_call(
    service: str,
    endpoint: str,
    method: str,
    status_code: Optional[int] = None,
    duration_ms: Optional[float] = None,
    error: Optional[str] = None,
):
    """
    Log external API call with context.

    Args:
        service: Service name (e.g., "github", "slack", "stripe")
        endpoint: API endpoint path
        method: HTTP method (GET, POST, etc.)
        status_code: HTTP status code
        duration_ms: Call duration in milliseconds
        error: Error message if call failed
    """
    attrs = {
        "external_api.service": service,
        "external_api.endpoint": endpoint,
        "external_api.method": method,
    }

    if status_code is not None:
        attrs["external_api.status_code"] = status_code
    if duration_ms is not None:
        attrs["external_api.duration_ms"] = f"{duration_ms:.2f}"
    if error:
        attrs["external_api.error"] = error[:200]

    if error or (status_code and status_code >= 400):
        add_span_event(f"External API call failed: {service} {endpoint}", attrs)
        logger.error("external_api.call_failed", **attrs)
    else:
        add_span_event(f"External API call: {service} {endpoint}", attrs)
        logger.info("external_api.call_success", **attrs)


def log_business_event(
    event_type: str,
    entity_type: str,
    entity_id: str,
    action: str,
    **extra_attrs
):
    """
    Log business event with context.

    Args:
        event_type: Type of event (e.g., "agent.created", "execution.started")
        entity_type: Type of entity (e.g., "agent", "execution", "workflow")
        entity_id: Entity identifier
        action: Action taken (e.g., "created", "updated", "deleted", "started")
        **extra_attrs: Additional business context
    """
    attrs = {
        "event.type": event_type,
        "entity.type": entity_type,
        "entity.id": entity_id,
        "event.action": action,
    }

    attrs.update(extra_attrs)

    add_span_event(
        f"Business event: {event_type}",
        attrs
    )

    logger.info(
        "business.event",
        **attrs
    )


def log_state_change(
    entity_type: str,
    entity_id: str,
    old_state: str,
    new_state: str,
    reason: Optional[str] = None,
    **extra_attrs
):
    """
    Log state transition with context.

    Args:
        entity_type: Type of entity (e.g., "execution", "worker", "agent")
        entity_id: Entity identifier
        old_state: Previous state
        new_state: New state
        reason: Reason for state change
        **extra_attrs: Additional context
    """
    attrs = {
        "state_change.entity_type": entity_type,
        "state_change.entity_id": entity_id,
        "state_change.old_state": old_state,
        "state_change.new_state": new_state,
    }

    if reason:
        attrs["state_change.reason"] = reason

    attrs.update(extra_attrs)

    add_span_event(
        f"State change: {entity_type} {old_state} → {new_state}",
        attrs
    )

    logger.info(
        "state.transition",
        **attrs
    )


def log_cache_operation(
    operation: str,
    key: str,
    hit: Optional[bool] = None,
    ttl: Optional[int] = None,
    size_bytes: Optional[int] = None,
):
    """
    Log cache operation with context.

    Args:
        operation: Operation type (e.g., "get", "set", "delete", "invalidate")
        key: Cache key
        hit: Whether cache hit occurred (for get operations)
        ttl: Time-to-live in seconds (for set operations)
        size_bytes: Size of cached data in bytes
    """
    attrs = {
        "cache.operation": operation,
        "cache.key": key[:100],  # Truncate long keys
    }

    if hit is not None:
        attrs["cache.hit"] = hit
    if ttl is not None:
        attrs["cache.ttl"] = ttl
    if size_bytes is not None:
        attrs["cache.size_bytes"] = size_bytes

    add_span_event(
        f"Cache {operation}: {key[:50]}",
        attrs
    )

    logger.info(
        "cache.operation",
        **attrs
    )


def log_validation_result(
    validation_type: str,
    valid: bool,
    errors: Optional[list] = None,
    warnings: Optional[list] = None,
    **extra_attrs
):
    """
    Log validation result with context.

    Args:
        validation_type: Type of validation (e.g., "input", "schema", "business_rule")
        valid: Whether validation passed
        errors: List of validation errors
        warnings: List of validation warnings
        **extra_attrs: Additional context
    """
    attrs = {
        "validation.type": validation_type,
        "validation.valid": valid,
    }

    if errors:
        attrs["validation.errors"] = str(errors)[:200]
        attrs["validation.error_count"] = len(errors)
    if warnings:
        attrs["validation.warnings"] = str(warnings)[:200]
        attrs["validation.warning_count"] = len(warnings)

    attrs.update(extra_attrs)

    event_name = f"Validation {'passed' if valid else 'failed'}: {validation_type}"
    add_span_event(event_name, attrs)

    if valid:
        logger.info("validation.passed", **attrs)
    else:
        logger.warning("validation.failed", **attrs)
