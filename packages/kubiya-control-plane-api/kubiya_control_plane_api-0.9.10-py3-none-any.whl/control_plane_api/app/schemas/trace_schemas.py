"""
Pydantic schemas for trace API endpoints.

These schemas define the request/response models for the traces REST API.
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class TraceStatus(str, Enum):
    """Trace status enum"""
    SUCCESS = "success"
    ERROR = "error"
    RUNNING = "running"


class SpanKind(str, Enum):
    """OTEL span kind enum"""
    INTERNAL = "INTERNAL"
    SERVER = "SERVER"
    CLIENT = "CLIENT"
    PRODUCER = "PRODUCER"
    CONSUMER = "CONSUMER"


class SpanStatusCode(str, Enum):
    """OTEL span status code enum"""
    UNSET = "UNSET"
    OK = "OK"
    ERROR = "ERROR"


# Response schemas

class SpanResponse(BaseModel):
    """Span response schema"""
    id: str
    trace_id: str
    span_id: str
    parent_span_id: Optional[str] = None
    organization_id: str
    name: str
    kind: SpanKind
    status_code: SpanStatusCode
    status_message: Optional[str] = None
    start_time_unix_nano: int
    end_time_unix_nano: Optional[int] = None
    duration_ns: Optional[int] = None
    duration_ms: Optional[float] = None
    attributes: Dict[str, Any] = Field(default_factory=dict)
    resource_attributes: Dict[str, Any] = Field(default_factory=dict)
    events: List[Dict[str, Any]] = Field(default_factory=list)
    links: List[Dict[str, Any]] = Field(default_factory=list)
    created_at: datetime

    # Nested children for tree structure
    children: List["SpanResponse"] = Field(default_factory=list)

    class Config:
        from_attributes = True


class TraceListItem(BaseModel):
    """Trace list item for list view"""
    id: str
    trace_id: str
    organization_id: str
    name: str
    service_name: Optional[str] = None
    status: TraceStatus
    execution_id: Optional[str] = None
    execution_type: Optional[str] = None
    user_id: Optional[str] = None
    user_email: Optional[str] = None
    user_name: Optional[str] = None
    user_avatar: Optional[str] = None
    started_at: datetime
    ended_at: Optional[datetime] = None
    duration_ms: Optional[int] = None
    span_count: int = 0
    error_count: int = 0
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class TraceDetailResponse(BaseModel):
    """Detailed trace response with spans"""
    id: str
    trace_id: str
    organization_id: str
    name: str
    service_name: Optional[str] = None
    status: TraceStatus
    execution_id: Optional[str] = None
    execution_type: Optional[str] = None
    user_id: Optional[str] = None
    user_email: Optional[str] = None
    user_name: Optional[str] = None
    user_avatar: Optional[str] = None
    started_at: datetime
    ended_at: Optional[datetime] = None
    duration_ms: Optional[int] = None
    span_count: int = 0
    error_count: int = 0
    created_at: datetime
    updated_at: Optional[datetime] = None

    # Spans as tree structure (root spans with nested children)
    spans: List[SpanResponse] = Field(default_factory=list)

    class Config:
        from_attributes = True


class TraceListResponse(BaseModel):
    """Paginated trace list response"""
    items: List[TraceListItem]
    total: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_previous: bool


class TraceStatsResponse(BaseModel):
    """Trace statistics response"""
    total_traces: int
    success_count: int
    error_count: int
    running_count: int
    error_rate: float
    avg_duration_ms: Optional[float] = None
    total_spans: int
    # Stats by time period
    period_start: Optional[datetime] = None
    period_end: Optional[datetime] = None


class DeleteTraceResponse(BaseModel):
    """Delete trace response"""
    trace_id: str
    deleted: bool
    message: str


# Request/Query schemas

class TraceFilters(BaseModel):
    """Query filters for trace list"""
    status: Optional[TraceStatus] = None
    time_from: Optional[datetime] = None
    time_to: Optional[datetime] = None
    search: Optional[str] = None
    execution_id: Optional[str] = None
    service_name: Optional[str] = None
    user_id: Optional[str] = None
    has_errors: Optional[bool] = None


# Allow forward references for self-referencing SpanResponse
SpanResponse.model_rebuild()
