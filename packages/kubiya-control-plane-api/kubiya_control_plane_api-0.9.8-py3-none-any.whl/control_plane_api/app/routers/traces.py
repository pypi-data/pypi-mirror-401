"""
Multi-tenant traces router for OTEL observability.

This router handles trace queries for the authenticated organization.
Provides endpoints for listing, filtering, and viewing trace details
with waterfall visualization support.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from starlette import status as http_status
from typing import Optional, List
from datetime import datetime, timezone, timedelta
import structlog
import math

from sqlalchemy.orm import Session
from sqlalchemy import desc, asc, func, or_

from control_plane_api.app.middleware.auth import get_current_organization
from control_plane_api.app.database import get_db
from control_plane_api.app.models.trace import Trace, Span, TraceStatus, SpanKind, SpanStatusCode
from control_plane_api.app.schemas.trace_schemas import (
    TraceListItem,
    TraceListResponse,
    TraceDetailResponse,
    SpanResponse,
    TraceStatsResponse,
    DeleteTraceResponse,
    TraceStatus as TraceStatusEnum,
)
from control_plane_api.app.observability import (
    create_span_with_context,
    add_span_event,
)
from control_plane_api.app.services.trace_retention import get_retention_service

logger = structlog.get_logger()

router = APIRouter()


def _span_to_response(span: Span, children: List[SpanResponse] = None) -> SpanResponse:
    """Convert Span model to SpanResponse schema"""
    duration_ms = None
    if span.duration_ns:
        duration_ms = span.duration_ns / 1_000_000

    return SpanResponse(
        id=str(span.id),
        trace_id=span.trace_id,
        span_id=span.span_id,
        parent_span_id=span.parent_span_id,
        organization_id=span.organization_id,
        name=span.name,
        kind=span.kind.value if span.kind else "INTERNAL",
        status_code=span.status_code.value if span.status_code else "UNSET",
        status_message=span.status_message,
        start_time_unix_nano=span.start_time_unix_nano,
        end_time_unix_nano=span.end_time_unix_nano,
        duration_ns=span.duration_ns,
        duration_ms=duration_ms,
        attributes=span.attributes or {},
        resource_attributes=span.resource_attributes or {},
        events=span.events or [],
        links=span.links or [],
        created_at=span.created_at,
        children=children or [],
    )


def _build_span_tree(spans: List[Span]) -> List[SpanResponse]:
    """Build hierarchical span tree from flat list"""
    # Create lookup maps
    span_map = {}
    children_map = {}

    for span in spans:
        span_map[span.span_id] = span
        if span.parent_span_id:
            if span.parent_span_id not in children_map:
                children_map[span.parent_span_id] = []
            children_map[span.parent_span_id].append(span)

    def build_node(span: Span) -> SpanResponse:
        children_spans = children_map.get(span.span_id, [])
        # Sort children by start time
        children_spans.sort(key=lambda s: s.start_time_unix_nano or 0)
        children = [build_node(child) for child in children_spans]
        return _span_to_response(span, children)

    # Find root spans (no parent)
    root_spans = [s for s in spans if not s.parent_span_id]
    root_spans.sort(key=lambda s: s.start_time_unix_nano or 0)

    return [build_node(root) for root in root_spans]


@router.get(
    "/traces",
    response_model=TraceListResponse,
    summary="List traces",
    description="Get paginated list of traces with optional filtering",
)
async def list_traces(
    # Pagination
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    # Sorting
    sort: str = Query("-started_at", description="Sort field with - prefix for descending"),
    # Filters
    status: Optional[str] = Query(None, description="Filter by status: success, error, running"),
    time_from: Optional[datetime] = Query(None, description="Filter traces starting after this time"),
    time_to: Optional[datetime] = Query(None, description="Filter traces starting before this time"),
    search: Optional[str] = Query(None, description="Search in trace/span names"),
    execution_id: Optional[str] = Query(None, description="Filter by linked execution ID"),
    service_name: Optional[str] = Query(None, description="Filter by service name"),
    user_id: Optional[str] = Query(None, description="Filter by user ID"),
    has_errors: Optional[bool] = Query(None, description="Filter traces with/without errors"),
    # Auth
    org=Depends(get_current_organization),
    db: Session = Depends(get_db),
):
    """List traces with filtering and pagination"""
    organization_id = org["id"]

    with create_span_with_context(
        "traces.list",
        organization_id=organization_id,
        user_id=org.get("user_id"),
        user_email=org.get("user_email"),
        user_name=org.get("user_name"),
        user_avatar=org.get("user_avatar"),
        page=page,
        page_size=page_size,
    ) as span:
        try:
            # Base query
            query = db.query(Trace).filter(Trace.organization_id == organization_id)

            # Apply filters
            if status:
                try:
                    # TraceStatus enum uses lowercase keys (success, error, running)
                    status_enum = TraceStatus[status.lower()]
                    query = query.filter(Trace.status == status_enum)
                except KeyError:
                    raise HTTPException(
                        status_code=http_status.HTTP_400_BAD_REQUEST,
                        detail=f"Invalid status: {status}. Must be one of: success, error, running"
                    )

            if time_from:
                query = query.filter(Trace.started_at >= time_from)

            if time_to:
                query = query.filter(Trace.started_at <= time_to)

            if search:
                search_pattern = f"%{search}%"
                query = query.filter(
                    or_(
                        Trace.name.ilike(search_pattern),
                        Trace.service_name.ilike(search_pattern),
                    )
                )

            if execution_id:
                query = query.filter(Trace.execution_id == execution_id)

            if service_name:
                query = query.filter(Trace.service_name == service_name)

            if user_id:
                query = query.filter(Trace.user_id == user_id)

            if has_errors is not None:
                if has_errors:
                    query = query.filter(Trace.error_count > 0)
                else:
                    query = query.filter(Trace.error_count == 0)

            # Get total count
            total = query.count()

            # Apply sorting
            sort_desc = sort.startswith("-")
            sort_field = sort.lstrip("-")

            sort_column_map = {
                "started_at": Trace.started_at,
                "ended_at": Trace.ended_at,
                "duration_ms": Trace.duration_ms,
                "span_count": Trace.span_count,
                "error_count": Trace.error_count,
                "name": Trace.name,
                "created_at": Trace.created_at,
            }

            sort_column = sort_column_map.get(sort_field, Trace.started_at)
            if sort_desc:
                query = query.order_by(desc(sort_column))
            else:
                query = query.order_by(asc(sort_column))

            # Apply pagination
            offset = (page - 1) * page_size
            traces = query.offset(offset).limit(page_size).all()

            # Calculate pagination metadata
            total_pages = math.ceil(total / page_size) if total > 0 else 1

            items = [
                TraceListItem(
                    id=str(t.id),
                    trace_id=t.trace_id,
                    organization_id=t.organization_id,
                    name=t.name,
                    service_name=t.service_name,
                    status=t.status.value if t.status else "running",
                    execution_id=t.execution_id,
                    execution_type=t.execution_type,
                    user_id=t.user_id,
                    user_email=t.user_email,
                    user_name=t.user_name,
                    user_avatar=t.user_avatar,
                    started_at=t.started_at,
                    ended_at=t.ended_at,
                    duration_ms=t.duration_ms,
                    span_count=t.span_count,
                    error_count=t.error_count,
                    created_at=t.created_at,
                    updated_at=t.updated_at,
                )
                for t in traces
            ]

            add_span_event("traces_fetched", {"count": len(items), "total": total})

            return TraceListResponse(
                items=items,
                total=total,
                page=page,
                page_size=page_size,
                total_pages=total_pages,
                has_next=page < total_pages,
                has_previous=page > 1,
            )

        except HTTPException:
            raise
        except Exception as e:
            logger.error("list_traces_failed", error=str(e), exc_info=True)
            raise HTTPException(
                status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to list traces: {str(e)}"
            )


@router.get(
    "/traces/stats",
    response_model=TraceStatsResponse,
    summary="Get trace statistics",
    description="Get aggregated statistics for traces",
)
async def get_trace_stats(
    time_from: Optional[datetime] = Query(None, description="Start of time range"),
    time_to: Optional[datetime] = Query(None, description="End of time range"),
    org=Depends(get_current_organization),
    db: Session = Depends(get_db),
):
    """Get trace statistics"""
    organization_id = org["id"]

    with create_span_with_context(
        "traces.stats",
        organization_id=organization_id,
        user_id=org.get("user_id"),
        user_email=org.get("user_email"),
        user_name=org.get("user_name"),
        user_avatar=org.get("user_avatar"),
    ) as span:
        try:
            # Default to last 24 hours if no time range specified
            if not time_from and not time_to:
                time_to = datetime.now(timezone.utc)
                time_from = time_to - timedelta(hours=24)

            # Base filters for all queries
            base_filters = [Trace.organization_id == organization_id]
            if time_from:
                base_filters.append(Trace.started_at >= time_from)
            if time_to:
                base_filters.append(Trace.started_at <= time_to)

            # Get counts by status - use separate queries to avoid mutation
            total_traces = db.query(Trace).filter(*base_filters).count()

            # Use lowercase string values to match PostgreSQL enum (not Python enum names)
            success_count = db.query(Trace).filter(*base_filters, Trace.status == "success").count()
            error_count = db.query(Trace).filter(*base_filters, Trace.status == "error").count()
            running_count = db.query(Trace).filter(*base_filters, Trace.status == "running").count()

            # Calculate error rate
            error_rate = (error_count / total_traces * 100) if total_traces > 0 else 0.0

            # Get average duration (only for completed traces)
            avg_duration = db.query(func.avg(Trace.duration_ms)).filter(
                *base_filters,
                Trace.duration_ms.isnot(None),
            ).scalar()

            # Get total spans
            total_spans_count = db.query(func.sum(Trace.span_count)).filter(
                *base_filters
            ).scalar() or 0

            return TraceStatsResponse(
                total_traces=total_traces,
                success_count=success_count,
                error_count=error_count,
                running_count=running_count,
                error_rate=round(error_rate, 2),
                avg_duration_ms=round(avg_duration, 2) if avg_duration else None,
                total_spans=total_spans_count,
                period_start=time_from,
                period_end=time_to,
            )

        except Exception as e:
            logger.error("get_trace_stats_failed", error=str(e), exc_info=True)
            raise HTTPException(
                status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to get trace stats: {str(e)}"
            )


@router.get(
    "/traces/{trace_id}",
    response_model=TraceDetailResponse,
    summary="Get trace details",
    description="Get detailed trace information with all spans in tree structure",
)
async def get_trace(
    trace_id: str,
    flat: bool = Query(False, description="Return spans as flat list instead of tree"),
    org=Depends(get_current_organization),
    db: Session = Depends(get_db),
):
    """Get trace details with spans"""
    organization_id = org["id"]

    with create_span_with_context(
        "traces.get",
        organization_id=organization_id,
        user_id=org.get("user_id"),
        user_email=org.get("user_email"),
        user_name=org.get("user_name"),
        user_avatar=org.get("user_avatar"),
        trace_id=trace_id,
    ) as span:
        try:
            # Get trace
            trace = db.query(Trace).filter(
                Trace.trace_id == trace_id,
                Trace.organization_id == organization_id,
            ).first()

            if not trace:
                raise HTTPException(
                    status_code=http_status.HTTP_404_NOT_FOUND,
                    detail=f"Trace {trace_id} not found"
                )

            # Get all spans for this trace
            spans = db.query(Span).filter(
                Span.trace_id == trace_id,
                Span.organization_id == organization_id,
            ).order_by(asc(Span.start_time_unix_nano)).all()

            # Build span response
            if flat:
                span_responses = [_span_to_response(s) for s in spans]
            else:
                span_responses = _build_span_tree(spans)

            add_span_event("trace_fetched", {"span_count": len(spans)})

            return TraceDetailResponse(
                id=str(trace.id),
                trace_id=trace.trace_id,
                organization_id=trace.organization_id,
                name=trace.name,
                service_name=trace.service_name,
                status=trace.status.value if trace.status else "running",
                execution_id=trace.execution_id,
                execution_type=trace.execution_type,
                user_id=trace.user_id,
                user_email=trace.user_email,
                user_name=trace.user_name,
                user_avatar=trace.user_avatar,
                started_at=trace.started_at,
                ended_at=trace.ended_at,
                duration_ms=trace.duration_ms,
                span_count=trace.span_count,
                error_count=trace.error_count,
                created_at=trace.created_at,
                updated_at=trace.updated_at,
                spans=span_responses,
            )

        except HTTPException:
            raise
        except Exception as e:
            logger.error("get_trace_failed", error=str(e), exc_info=True)
            raise HTTPException(
                status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to get trace: {str(e)}"
            )


@router.get(
    "/traces/{trace_id}/spans",
    response_model=List[SpanResponse],
    summary="Get trace spans",
    description="Get all spans for a trace",
)
async def get_trace_spans(
    trace_id: str,
    flat: bool = Query(False, description="Return spans as flat list instead of tree"),
    org=Depends(get_current_organization),
    db: Session = Depends(get_db),
):
    """Get spans for a trace"""
    organization_id = org["id"]

    with create_span_with_context(
        "traces.get_spans",
        organization_id=organization_id,
        user_id=org.get("user_id"),
        user_email=org.get("user_email"),
        user_name=org.get("user_name"),
        user_avatar=org.get("user_avatar"),
        trace_id=trace_id,
    ) as span:
        try:
            # Verify trace exists and belongs to org
            trace = db.query(Trace).filter(
                Trace.trace_id == trace_id,
                Trace.organization_id == organization_id,
            ).first()

            if not trace:
                raise HTTPException(
                    status_code=http_status.HTTP_404_NOT_FOUND,
                    detail=f"Trace {trace_id} not found"
                )

            # Get all spans
            spans = db.query(Span).filter(
                Span.trace_id == trace_id,
                Span.organization_id == organization_id,
            ).order_by(asc(Span.start_time_unix_nano)).all()

            if flat:
                return [_span_to_response(s) for s in spans]
            else:
                return _build_span_tree(spans)

        except HTTPException:
            raise
        except Exception as e:
            logger.error("get_trace_spans_failed", error=str(e), exc_info=True)
            raise HTTPException(
                status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to get trace spans: {str(e)}"
            )


@router.delete(
    "/traces/{trace_id}",
    response_model=DeleteTraceResponse,
    summary="Delete trace",
    description="Delete a trace and all its spans",
)
async def delete_trace(
    trace_id: str,
    org=Depends(get_current_organization),
    db: Session = Depends(get_db),
):
    """Delete a trace and all its spans"""
    organization_id = org["id"]

    with create_span_with_context(
        "traces.delete",
        organization_id=organization_id,
        user_id=org.get("user_id"),
        user_email=org.get("user_email"),
        user_name=org.get("user_name"),
        user_avatar=org.get("user_avatar"),
        trace_id=trace_id,
    ) as span:
        try:
            # Get trace
            trace = db.query(Trace).filter(
                Trace.trace_id == trace_id,
                Trace.organization_id == organization_id,
            ).first()

            if not trace:
                raise HTTPException(
                    status_code=http_status.HTTP_404_NOT_FOUND,
                    detail=f"Trace {trace_id} not found"
                )

            # Delete trace (cascade will delete spans due to FK relationship)
            db.delete(trace)
            db.commit()

            logger.info(
                "trace_deleted",
                trace_id=trace_id,
                organization_id=organization_id,
            )

            return DeleteTraceResponse(
                trace_id=trace_id,
                deleted=True,
                message=f"Trace {trace_id} and all spans deleted successfully",
            )

        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            logger.error("delete_trace_failed", error=str(e), exc_info=True)
            raise HTTPException(
                status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to delete trace: {str(e)}"
            )


@router.get(
    "/traces/storage/stats",
    summary="Get trace storage statistics",
    description="Get storage statistics and retention info for traces",
)
async def get_storage_stats(
    org=Depends(get_current_organization),
):
    """Get trace storage statistics"""
    organization_id = org["id"]

    with create_span_with_context(
        "traces.storage_stats",
        organization_id=organization_id,
        user_id=org.get("user_id"),
        user_email=org.get("user_email"),
        user_name=org.get("user_name"),
        user_avatar=org.get("user_avatar"),
    ) as span:
        try:
            retention_service = get_retention_service()
            stats = await retention_service.get_storage_stats(organization_id)
            return stats

        except Exception as e:
            logger.error("get_storage_stats_failed", error=str(e), exc_info=True)
            raise HTTPException(
                status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to get storage stats: {str(e)}"
            )
