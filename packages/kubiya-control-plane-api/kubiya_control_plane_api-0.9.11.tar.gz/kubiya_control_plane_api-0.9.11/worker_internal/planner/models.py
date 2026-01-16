"""Pydantic models for plan orchestration."""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum


class PlanStatus(str, Enum):
    """Plan execution status"""
    PENDING = "pending"
    RUNNING = "running"
    PENDING_USER_INPUT = "pending_user_input"  # Paused, waiting for user to provide input
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class TaskStatus(str, Enum):
    """Task execution status"""
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    WAITING_FOR_INPUT = "waiting_for_input"  # Task paused, needs user input to continue
    VALIDATING = "validating"


class PlanTask(BaseModel):
    """Task definition from plan"""
    id: int
    title: str
    description: str
    details: str
    test_strategy: Optional[str] = None
    priority: str = "medium"
    dependencies: List[int] = Field(default_factory=list)
    status: TaskStatus = TaskStatus.PENDING
    subtasks: List[Any] = Field(default_factory=list)
    skills_to_use: List[str] = Field(default_factory=list)
    env_vars_to_use: List[str] = Field(default_factory=list)
    secrets_to_use: List[str] = Field(default_factory=list)
    knowledge_references: List[str] = Field(default_factory=list)
    agent_id: Optional[str] = None
    worker_queue_id: Optional[str] = None


class AgentInfo(BaseModel):
    """Agent metadata from plan"""
    team_id: Optional[str] = None
    team_name: str
    agent_id: str
    agent_name: str
    responsibilities: List[str] = Field(default_factory=list)
    estimated_time_hours: float = 0.0
    model_info: Dict[str, Any] = Field(default_factory=dict)
    expected_tools: List[Dict[str, Any]] = Field(default_factory=list)
    agent_cost: float = 0.0
    tasks: List[PlanTask] = Field(default_factory=list)


class Plan(BaseModel):
    """Plan definition"""
    title: str
    summary: str
    complexity: Dict[str, Any] = Field(default_factory=dict)
    team_breakdown: List[AgentInfo] = Field(default_factory=list)
    recommended_execution: Dict[str, Any] = Field(default_factory=dict)
    cost_estimate: Dict[str, Any] = Field(default_factory=dict)
    realized_savings: Dict[str, Any] = Field(default_factory=dict)
    risks: List[str] = Field(default_factory=list)
    prerequisites: List[str] = Field(default_factory=list)
    success_criteria: List[str] = Field(default_factory=list)
    has_questions: bool = False
    questions: Optional[Any] = None


class PlanOrchestratorInput(BaseModel):
    """Input for plan orchestrator workflow"""
    plan: Plan
    organization_id: str
    agent_id: str
    worker_queue_id: str  # Worker queue ID for routing task executions
    user_id: Optional[str] = None
    execution_id: Optional[str] = None
    # Auth context
    jwt_token: Optional[str] = None
    # Continuation context
    is_continuation: bool = False  # True if this is resuming a paused plan
    previous_task_results: Optional[Dict[int, Dict[str, Any]]] = None  # Previous task results for continuation


class TaskRetryAttempt(BaseModel):
    """Single retry attempt record"""
    attempt_number: int
    error: str
    output: str
    events: List[Dict[str, Any]] = Field(default_factory=list)
    started_at: datetime
    completed_at: datetime


class TaskRetryContext(BaseModel):
    """Context for retrying a failed task"""
    current_attempt: int
    max_attempts: int
    previous_failures: List[TaskRetryAttempt]


class TaskExecutionResult(BaseModel):
    """Result of task execution"""
    task_id: int
    status: TaskStatus
    execution_id: str
    output: str
    events: List[Dict[str, Any]] = Field(default_factory=list)
    tokens: int = 0
    cost: float = 0.0
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    error: Optional[str] = None
    needs_continuation: bool = False
    user_question: Optional[str] = None
    retry_count: int = 0
    retry_history: List[TaskRetryAttempt] = Field(default_factory=list)


class TaskValidationResult(BaseModel):
    """Result of task validation"""
    task_id: int
    status: TaskStatus
    reason: str
    confidence: float
    suggestions: Optional[str] = None


class PlanExecutionSummary(BaseModel):
    """Final plan execution summary"""
    plan_execution_id: str
    status: PlanStatus
    total_tasks: int
    completed_tasks: int
    failed_tasks: int
    total_tokens: int
    total_cost: float
    started_at: datetime
    completed_at: Optional[datetime] = None
    execution_time_seconds: float = 0.0
    task_results: Dict[int, TaskExecutionResult] = Field(default_factory=dict)


# Activity inputs/outputs

class CreatePlanExecutionInput(BaseModel):
    """Input for create_plan_execution activity"""
    execution_id: str
    organization_id: str
    agent_id: str
    title: str
    summary: Optional[str] = None
    total_tasks: int
    plan_json: Dict[str, Any]
    estimated_cost_usd: Optional[float] = None


class UpdatePlanStateInput(BaseModel):
    """Input for update_plan_state activity"""
    plan_execution_id: str
    status: Optional[PlanStatus] = None
    completed_tasks: Optional[int] = None
    failed_tasks: Optional[int] = None
    current_task_id: Optional[int] = None
    current_task_status: Optional[TaskStatus] = None
    dag_state: Optional[Dict[int, Any]] = None
    total_tokens: Optional[int] = None
    actual_cost_usd: Optional[float] = None
    waiting_tasks: Optional[List[Dict[str, Any]]] = None  # List of tasks waiting for user input


class ExecuteAgentInput(BaseModel):
    """Input for executing an agent (child workflow)"""
    execution_id: str
    agent_id: str
    organization_id: str
    prompt: str
    system_prompt: Optional[str] = None
    model_id: Optional[str] = None
    task_metadata: Dict[str, Any] = Field(default_factory=dict)
    jwt_token: Optional[str] = None


class AgentToolContext(BaseModel):
    """Context passed to agent tools"""
    plan_execution_id: str
    organization_id: str
    agent_id: str
    plan: Plan
    task_results: Dict[int, TaskExecutionResult] = Field(default_factory=dict)
    jwt_token: Optional[str] = None
