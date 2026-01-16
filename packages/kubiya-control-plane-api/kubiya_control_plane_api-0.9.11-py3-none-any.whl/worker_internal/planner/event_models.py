"""Pydantic models for plan execution streaming events."""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime


class PlanEventBase(BaseModel):
    """Base model for all plan events."""
    execution_id: str
    timestamp: Optional[datetime] = Field(default_factory=lambda: datetime.utcnow())


class PlanStartedEvent(PlanEventBase):
    """Plan execution started."""
    title: str
    total_tasks: int
    agent_id: str


class TaskStartedEvent(PlanEventBase):
    """Task execution started."""
    task_id: int
    title: str
    description: str
    agent_id: str
    task_execution_id: str  # Agent execution ID for this task
    dependencies: List[int] = Field(default_factory=list)


class TaskRunningEvent(PlanEventBase):
    """Task execution progress update."""
    task_id: int
    status: str
    message: Optional[str] = None


class TasksParallelEvent(PlanEventBase):
    """Multiple tasks running in parallel."""
    task_ids: List[int]
    message: str


class TaskWaitingForInputEvent(PlanEventBase):
    """Task paused, waiting for user input."""
    task_id: int
    question: str
    task_execution_id: str


class TaskValidationStartedEvent(PlanEventBase):
    """Task validation started."""
    task_id: int
    title: str


class TaskValidationCompleteEvent(PlanEventBase):
    """Task validation completed."""
    task_id: int
    is_valid: bool
    reason: str
    confidence: float


class TaskRetryEvent(PlanEventBase):
    """Task is being retried after failure."""
    task_id: int
    title: str
    attempt_number: int
    max_attempts: int
    previous_error: str


class TaskCompletedEvent(PlanEventBase):
    """Task execution completed."""
    task_id: int
    title: str
    status: str
    output: str
    error: Optional[str] = None
    tokens: int = 0
    cost: float = 0.0
    retry_count: int = 0
    had_retries: bool = False


class PlanStatusUpdateEvent(PlanEventBase):
    """Overall plan progress update."""
    completed_tasks: int
    failed_tasks: int
    total_tasks: int
    current_task_id: Optional[int] = None
    progress_percentage: float


class PlanCompletedEvent(PlanEventBase):
    """Plan execution completed."""
    status: str  # "completed" or "failed"
    completed_tasks: int
    failed_tasks: int
    total_tasks: int
    total_tokens: int
    total_cost: float
    duration_seconds: float


class TodoItem(BaseModel):
    """Single TODO item for UI checklist."""
    task_id: int
    title: str
    description: str
    status: str  # "pending", "running", "completed", "failed", "waiting_for_input"
    dependencies: List[int] = Field(default_factory=list)
    agent_id: Optional[str] = None


class TodoListInitializedEvent(PlanEventBase):
    """Initial TODO list with all tasks."""
    title: str
    total_tasks: int
    items: List[TodoItem]


class TodoItemUpdatedEvent(PlanEventBase):
    """Individual TODO item status update."""
    task_id: int
    title: str
    old_status: str
    new_status: str
    message: Optional[str] = None


# Event type mapping for serialization
EVENT_TYPE_MAP = {
    "plan_started": PlanStartedEvent,
    "task_started": TaskStartedEvent,
    "task_running": TaskRunningEvent,
    "tasks_parallel": TasksParallelEvent,
    "task_retry": TaskRetryEvent,
    "task_waiting_for_input": TaskWaitingForInputEvent,
    "task_validation_started": TaskValidationStartedEvent,
    "task_validation_complete": TaskValidationCompleteEvent,
    "task_completed": TaskCompletedEvent,
    "plan_status_update": PlanStatusUpdateEvent,
    "plan_completed": PlanCompletedEvent,
    "todo_list_initialized": TodoListInitializedEvent,
    "todo_item_updated": TodoItemUpdatedEvent,
}
