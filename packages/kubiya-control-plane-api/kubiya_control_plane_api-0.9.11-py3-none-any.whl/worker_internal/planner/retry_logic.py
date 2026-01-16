"""Intelligent retry logic for task execution."""

from typing import List, Dict, Any, Optional
from datetime import datetime, timezone

from worker_internal.planner.models import (
    TaskRetryAttempt,
    TaskRetryContext,
    TaskExecutionResult,
    PlanTask,
)


MAX_RETRY_ATTEMPTS = 5


def should_retry_task(result: TaskExecutionResult, attempt: int) -> bool:
    """Determine if a task should be retried based on its result and attempt number."""
    from worker_internal.planner.models import TaskStatus

    if result.status != TaskStatus.FAILED:
        return False

    if attempt >= MAX_RETRY_ATTEMPTS:
        return False

    return True


def build_retry_context(
    retry_history: List[TaskRetryAttempt],
    current_attempt: int,
) -> TaskRetryContext:
    """Build retry context from previous failures."""
    return TaskRetryContext(
        current_attempt=current_attempt,
        max_attempts=MAX_RETRY_ATTEMPTS,
        previous_failures=retry_history,
    )


def create_retry_attempt_record(
    result: TaskExecutionResult,
    attempt_number: int,
) -> TaskRetryAttempt:
    """Create a retry attempt record from a failed result."""
    return TaskRetryAttempt(
        attempt_number=attempt_number,
        error=result.error or "Unknown error",
        output=result.output,
        events=result.events,
        started_at=result.started_at or datetime.now(timezone.utc),
        completed_at=result.completed_at or datetime.now(timezone.utc),
    )


def format_retry_context_for_prompt(retry_context: TaskRetryContext) -> str:
    """Format retry context into a detailed prompt for the agent."""
    if not retry_context.previous_failures:
        return ""

    lines = [
        "\n" + "=" * 80,
        f"⚠️  RETRY ATTEMPT {retry_context.current_attempt}/{retry_context.max_attempts}",
        "=" * 80,
        "",
        "This task has failed in previous attempts. Learn from these failures and fix the issues:",
        "",
    ]

    for failure in retry_context.previous_failures:
        lines.extend([
            f"--- Attempt #{failure.attempt_number} ---",
            f"Error: {failure.error}",
            "",
        ])

        if failure.output:
            lines.extend([
                "Output from failed attempt:",
                failure.output[:1000],
                "",
            ])

        if failure.events:
            lines.append("Key events from execution:")
            for event in failure.events[-5:]:
                event_type = event.get("type", "unknown")
                lines.append(f"  • {event_type}")
            lines.append("")

    lines.extend([
        "=" * 80,
        "INSTRUCTIONS FOR RETRY:",
        "1. Carefully analyze the error messages above",
        "2. Identify the root cause of the failure",
        "3. Fix the issue completely (don't just work around it)",
        "4. Test your solution to ensure it works",
        "=" * 80,
        "",
    ])

    return "\n".join(lines)


def enrich_task_with_retry_context(
    task: PlanTask,
    retry_context: Optional[TaskRetryContext],
) -> PlanTask:
    """Create a new task with retry context added to its description."""
    if not retry_context or not retry_context.previous_failures:
        return task

    retry_prompt = format_retry_context_for_prompt(retry_context)

    enriched_task = task.model_copy(deep=True)
    enriched_task.details = f"{task.details}\n\n{retry_prompt}"

    return enriched_task


def extract_error_summary(events: List[Dict[str, Any]]) -> Optional[str]:
    """Extract error summary from event stream."""
    for event in reversed(events):
        if event.get("type") == "error":
            return event.get("error", "Unknown error")

        content = event.get("content", {})
        if isinstance(content, dict):
            error = content.get("error")
            if error:
                return error

    return None
