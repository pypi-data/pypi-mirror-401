"""Database model for plan executions."""

from sqlalchemy import Column, String, DateTime, Text, Integer, Numeric, Index
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
from datetime import datetime
import uuid
import enum

from control_plane_api.app.database import Base


class PlanExecutionStatus(str, enum.Enum):
    """Plan execution status"""
    PENDING = "pending"
    RUNNING = "running"
    PENDING_USER_INPUT = "pending_user_input"  # Waiting for user to provide input
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class PlanExecution(Base):
    """Model for tracking multi-task plan executions."""

    __tablename__ = "plan_executions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)

    # Execution identifier (Temporal workflow ID)
    execution_id = Column(String(255), unique=True, nullable=False, index=True)

    # Organization and agent
    organization_id = Column(String(255), nullable=False, index=True)
    agent_id = Column(UUID(as_uuid=True), nullable=True)  # Primary agent for the plan

    # Link to plan generation (for traceability)
    plan_generation_id = Column(String(255), nullable=True, index=True)  # Execution ID of the plan generation

    # Plan metadata
    title = Column(Text, nullable=False)
    summary = Column(Text, nullable=True)
    total_tasks = Column(Integer, nullable=False, default=0)
    completed_tasks = Column(Integer, nullable=False, default=0)
    failed_tasks = Column(Integer, nullable=True, default=0)

    # Status tracking
    status = Column(String(50), nullable=False, default=PlanExecutionStatus.RUNNING.value, index=True)

    # DAG state (stores dependency graph and task status)
    dag_state = Column(JSONB, default={}, nullable=True)

    # Waiting tasks (for user input continuation)
    # Format: [{"task_id": 1, "execution_id": "abc-123", "question": "What?", "waiting_since": "2025-12-18T10:00:00Z"}]
    waiting_tasks = Column(JSONB, default=[], nullable=True)

    # Aggregated metrics
    total_tokens = Column(Integer, default=0, nullable=True)
    total_execution_time_seconds = Column(Integer, default=0, nullable=True)
    estimated_cost_usd = Column(Numeric(10, 4), nullable=True)
    actual_cost_usd = Column(Numeric(10, 4), nullable=True)

    # Plan JSON (store original plan for reference)
    plan_json = Column(JSONB, nullable=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)

    # Indexes for common queries
    __table_args__ = (
        Index('idx_plan_executions_org_status', 'organization_id', 'status'),
        Index('idx_plan_executions_created', 'created_at'),
    )

    def to_dict(self):
        """Convert to dictionary for API responses."""
        return {
            "id": str(self.id),
            "execution_id": self.execution_id,
            "organization_id": self.organization_id,
            "agent_id": str(self.agent_id) if self.agent_id else None,
            "title": self.title,
            "summary": self.summary,
            "total_tasks": self.total_tasks,
            "completed_tasks": self.completed_tasks,
            "failed_tasks": self.failed_tasks,
            "status": self.status,
            "dag_state": self.dag_state,
            "waiting_tasks": self.waiting_tasks,
            "total_tokens": self.total_tokens,
            "total_execution_time_seconds": self.total_execution_time_seconds,
            "estimated_cost_usd": float(self.estimated_cost_usd) if self.estimated_cost_usd else None,
            "actual_cost_usd": float(self.actual_cost_usd) if self.actual_cost_usd else None,
            "plan_json": self.plan_json,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
        }
