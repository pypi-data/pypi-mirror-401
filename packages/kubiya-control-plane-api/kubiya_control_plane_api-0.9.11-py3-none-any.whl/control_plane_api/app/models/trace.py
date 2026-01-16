"""
Trace and Span models for OpenTelemetry observability.

These models store OTEL trace data locally in PostgreSQL for querying and visualization.
Traces are aggregated views, while Spans store individual operations within a trace.
"""

from sqlalchemy import Column, String, Integer, BigInteger, DateTime, Text, Index, ForeignKey, desc
from sqlalchemy.dialects.postgresql import UUID, JSONB, ENUM
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
import uuid
import enum

from control_plane_api.app.database import Base


class TraceStatus(str, enum.Enum):
    """Status of a trace execution - values match PostgreSQL enum (lowercase)"""
    success = "success"
    error = "error"
    running = "running"


class SpanKind(str, enum.Enum):
    """OTEL span kind - describes the relationship between the span and its parent"""
    INTERNAL = "INTERNAL"
    SERVER = "SERVER"
    CLIENT = "CLIENT"
    PRODUCER = "PRODUCER"
    CONSUMER = "CONSUMER"


class SpanStatusCode(str, enum.Enum):
    """OTEL span status code"""
    UNSET = "UNSET"
    OK = "OK"
    ERROR = "ERROR"


class Trace(Base):
    """
    Aggregated trace record for efficient listing and filtering.

    A trace represents a complete distributed transaction, containing multiple spans.
    This table stores denormalized summary data for fast querying.
    """

    __tablename__ = "traces"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)

    # OTEL trace ID (32-char hex string)
    trace_id = Column(String(64), nullable=False, unique=True, index=True)

    # Multi-tenant scoping
    organization_id = Column(String(255), nullable=False, index=True)

    # Trace metadata (from root span)
    name = Column(String(512), nullable=False)  # Root span name
    service_name = Column(String(255), nullable=True)  # Service that started the trace

    # Status
    status = Column(
        ENUM(TraceStatus, name='trace_status', create_type=False),
        nullable=False,
        default=TraceStatus.running
    )

    # Execution linkage (optional - links trace to agent/team/workflow execution)
    execution_id = Column(String(255), nullable=True, index=True)
    execution_type = Column(String(50), nullable=True)  # 'agent', 'team', 'workflow'

    # User attribution
    user_id = Column(String(255), nullable=True, index=True)
    user_email = Column(String(255), nullable=True)
    user_name = Column(String(255), nullable=True)  # User display name
    user_avatar = Column(String(512), nullable=True)  # Avatar URL

    # Timing
    started_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    ended_at = Column(DateTime(timezone=True), nullable=True)
    duration_ms = Column(BigInteger, nullable=True)  # Computed on completion

    # Denormalized stats (updated as spans complete)
    span_count = Column(Integer, nullable=False, default=0)
    error_count = Column(Integer, nullable=False, default=0)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    spans = relationship(
        "Span",
        back_populates="trace",
        cascade="all, delete-orphan",
        lazy="dynamic",  # Use dynamic for potentially large span collections
        order_by="Span.start_time_unix_nano"
    )

    __table_args__ = (
        # Composite indexes for common query patterns
        Index('ix_traces_org_started', 'organization_id', desc('started_at')),
        Index('ix_traces_org_status', 'organization_id', 'status'),
        Index('ix_traces_org_service', 'organization_id', 'service_name'),
        Index('ix_traces_org_user', 'organization_id', 'user_id'),
        # Execution lookup
        Index('ix_traces_execution', 'execution_id', postgresql_where='execution_id IS NOT NULL'),
    )

    def __repr__(self):
        return f"<Trace {self.trace_id[:8]}... ({self.status.value}) - {self.name}>"

    def to_dict(self):
        """Convert to dictionary for API response"""
        return {
            "id": str(self.id),
            "trace_id": self.trace_id,
            "organization_id": self.organization_id,
            "name": self.name,
            "service_name": self.service_name,
            "status": self.status.value if self.status else None,
            "execution_id": self.execution_id,
            "execution_type": self.execution_type,
            "user_id": self.user_id,
            "user_email": self.user_email,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "ended_at": self.ended_at.isoformat() if self.ended_at else None,
            "duration_ms": self.duration_ms,
            "span_count": self.span_count,
            "error_count": self.error_count,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class Span(Base):
    """
    Individual span record - represents a single operation within a trace.

    Spans form a tree structure via parent_span_id to represent the execution flow.
    Attributes, events, and links are stored as JSONB for flexibility.
    """

    __tablename__ = "spans"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)

    # OTEL identifiers
    trace_id = Column(
        String(64),
        ForeignKey("traces.trace_id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    span_id = Column(String(32), nullable=False, index=True)  # 16-char hex
    parent_span_id = Column(String(32), nullable=True, index=True)  # Null for root span

    # Denormalized for query efficiency (avoids joins)
    organization_id = Column(String(255), nullable=False, index=True)

    # Core span data
    name = Column(String(512), nullable=False)
    kind = Column(
        ENUM(SpanKind, name='span_kind', create_type=False),
        nullable=False,
        default=SpanKind.INTERNAL
    )
    status_code = Column(
        ENUM(SpanStatusCode, name='span_status_code', create_type=False),
        nullable=False,
        default=SpanStatusCode.UNSET
    )
    status_message = Column(Text, nullable=True)

    # Timing (nanosecond precision for OTEL compatibility)
    start_time_unix_nano = Column(BigInteger, nullable=False)
    end_time_unix_nano = Column(BigInteger, nullable=True)
    duration_ns = Column(BigInteger, nullable=True)  # Computed: end - start

    # JSONB columns for flexible OTEL data
    attributes = Column(JSONB, nullable=True, default=dict)  # Span attributes
    resource_attributes = Column(JSONB, nullable=True, default=dict)  # Resource info
    events = Column(JSONB, nullable=True, default=list)  # Span events array
    links = Column(JSONB, nullable=True, default=list)  # Links to other spans/traces

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    trace = relationship("Trace", back_populates="spans")

    __table_args__ = (
        # Composite indexes for efficient queries
        Index('ix_spans_trace_parent', 'trace_id', 'parent_span_id'),
        Index('ix_spans_trace_start', 'trace_id', 'start_time_unix_nano'),
        Index('ix_spans_org_name', 'organization_id', 'name'),
        Index('ix_spans_org_start', 'organization_id', desc('start_time_unix_nano')),
        # Unique constraint on span_id within a trace
        Index('ix_spans_trace_span_unique', 'trace_id', 'span_id', unique=True),
    )

    def __repr__(self):
        return f"<Span {self.span_id[:8]}... ({self.status_code.value}) - {self.name}>"

    @property
    def duration_ms(self) -> float | None:
        """Duration in milliseconds (computed from nanoseconds)"""
        if self.duration_ns is not None:
            return self.duration_ns / 1_000_000
        return None

    @property
    def start_time_iso(self) -> str | None:
        """Start time as ISO 8601 string"""
        if self.start_time_unix_nano:
            # Convert nanoseconds to seconds for datetime
            ts = self.start_time_unix_nano / 1_000_000_000
            return datetime.utcfromtimestamp(ts).isoformat() + "Z"
        return None

    @property
    def end_time_iso(self) -> str | None:
        """End time as ISO 8601 string"""
        if self.end_time_unix_nano:
            ts = self.end_time_unix_nano / 1_000_000_000
            return datetime.utcfromtimestamp(ts).isoformat() + "Z"
        return None

    def to_dict(self):
        """Convert to dictionary for API response"""
        return {
            "id": str(self.id),
            "trace_id": self.trace_id,
            "span_id": self.span_id,
            "parent_span_id": self.parent_span_id,
            "organization_id": self.organization_id,
            "name": self.name,
            "kind": self.kind.value if self.kind else None,
            "status_code": self.status_code.value if self.status_code else None,
            "status_message": self.status_message,
            "start_time_unix_nano": self.start_time_unix_nano,
            "end_time_unix_nano": self.end_time_unix_nano,
            "duration_ns": self.duration_ns,
            "duration_ms": self.duration_ms,
            "start_time": self.start_time_iso,
            "end_time": self.end_time_iso,
            "attributes": self.attributes or {},
            "resource_attributes": self.resource_attributes or {},
            "events": self.events or [],
            "links": self.links or [],
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
