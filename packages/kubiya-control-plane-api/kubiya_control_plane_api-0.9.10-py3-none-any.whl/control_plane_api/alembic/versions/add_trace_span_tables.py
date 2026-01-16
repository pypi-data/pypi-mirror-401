"""add_trace_span_tables

Creates traces and spans tables for OTEL observability with
real-time streaming support.

Revision ID: add_trace_span_tables
Revises: f71305fb69b9
Create Date: 2026-01-13

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'add_trace_span_tables'
down_revision: Union[str, Sequence[str], None] = 'f71305fb69b9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# Pre-create enum types to reference in columns
trace_status_enum = postgresql.ENUM('success', 'error', 'running', name='trace_status', create_type=False)
span_kind_enum = postgresql.ENUM('INTERNAL', 'SERVER', 'CLIENT', 'PRODUCER', 'CONSUMER', name='span_kind', create_type=False)
span_status_code_enum = postgresql.ENUM('UNSET', 'OK', 'ERROR', name='span_status_code', create_type=False)


def upgrade() -> None:
    """Create traces and spans tables with enums and indexes."""

    # Create trace_status enum
    op.execute("""
        DO $$ BEGIN
            CREATE TYPE trace_status AS ENUM ('success', 'error', 'running');
        EXCEPTION
            WHEN duplicate_object THEN null;
        END $$;
    """)

    # Create span_kind enum (OTEL standard)
    op.execute("""
        DO $$ BEGIN
            CREATE TYPE span_kind AS ENUM ('INTERNAL', 'SERVER', 'CLIENT', 'PRODUCER', 'CONSUMER');
        EXCEPTION
            WHEN duplicate_object THEN null;
        END $$;
    """)

    # Create span_status_code enum (OTEL standard)
    op.execute("""
        DO $$ BEGIN
            CREATE TYPE span_status_code AS ENUM ('UNSET', 'OK', 'ERROR');
        EXCEPTION
            WHEN duplicate_object THEN null;
        END $$;
    """)

    # Create traces table
    op.create_table(
        'traces',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('trace_id', sa.String(64), nullable=False, unique=True),
        sa.Column('organization_id', sa.String(255), nullable=False),
        sa.Column('name', sa.String(512), nullable=False),
        sa.Column('service_name', sa.String(255), nullable=True),
        sa.Column('status', trace_status_enum, nullable=False, server_default='running'),
        sa.Column('execution_id', sa.String(255), nullable=True),
        sa.Column('execution_type', sa.String(50), nullable=True),
        sa.Column('user_id', sa.String(255), nullable=True),
        sa.Column('user_email', sa.String(255), nullable=True),
        sa.Column('started_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('NOW()')),
        sa.Column('ended_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('duration_ms', sa.BigInteger(), nullable=True),
        sa.Column('span_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('error_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('NOW()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True, server_default=sa.text('NOW()')),
    )

    # Create traces indexes
    op.create_index('ix_traces_trace_id', 'traces', ['trace_id'])
    op.create_index('ix_traces_org_id', 'traces', ['organization_id'])
    op.create_index('ix_traces_org_started', 'traces', ['organization_id', 'started_at'])
    op.create_index('ix_traces_org_status', 'traces', ['organization_id', 'status'])
    op.create_index('ix_traces_org_service', 'traces', ['organization_id', 'service_name'])
    op.create_index('ix_traces_org_user', 'traces', ['organization_id', 'user_id'])
    op.create_index('ix_traces_user_id', 'traces', ['user_id'])

    # Create partial index for execution_id
    op.execute("""
        CREATE INDEX IF NOT EXISTS ix_traces_execution
        ON traces(execution_id)
        WHERE execution_id IS NOT NULL
    """)

    # Create spans table
    op.create_table(
        'spans',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('trace_id', sa.String(64), sa.ForeignKey('traces.trace_id', ondelete='CASCADE'), nullable=False),
        sa.Column('span_id', sa.String(32), nullable=False),
        sa.Column('parent_span_id', sa.String(32), nullable=True),
        sa.Column('organization_id', sa.String(255), nullable=False),
        sa.Column('name', sa.String(512), nullable=False),
        sa.Column('kind', span_kind_enum, nullable=False, server_default='INTERNAL'),
        sa.Column('status_code', span_status_code_enum, nullable=False, server_default='UNSET'),
        sa.Column('status_message', sa.Text(), nullable=True),
        sa.Column('start_time_unix_nano', sa.BigInteger(), nullable=False),
        sa.Column('end_time_unix_nano', sa.BigInteger(), nullable=True),
        sa.Column('duration_ns', sa.BigInteger(), nullable=True),
        sa.Column('attributes', postgresql.JSONB(astext_type=sa.Text()), nullable=True, server_default='{}'),
        sa.Column('resource_attributes', postgresql.JSONB(astext_type=sa.Text()), nullable=True, server_default='{}'),
        sa.Column('events', postgresql.JSONB(astext_type=sa.Text()), nullable=True, server_default='[]'),
        sa.Column('links', postgresql.JSONB(astext_type=sa.Text()), nullable=True, server_default='[]'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('NOW()')),
    )

    # Create spans indexes
    op.create_index('ix_spans_trace_id', 'spans', ['trace_id'])
    op.create_index('ix_spans_span_id', 'spans', ['span_id'])
    op.create_index('ix_spans_parent_span_id', 'spans', ['parent_span_id'])
    op.create_index('ix_spans_org_id', 'spans', ['organization_id'])
    op.create_index('ix_spans_trace_parent', 'spans', ['trace_id', 'parent_span_id'])
    op.create_index('ix_spans_trace_start', 'spans', ['trace_id', 'start_time_unix_nano'])
    op.create_index('ix_spans_org_name', 'spans', ['organization_id', 'name'])
    op.create_index('ix_spans_org_start', 'spans', ['organization_id', 'start_time_unix_nano'])

    # Unique constraint on span_id within a trace
    op.create_index('ix_spans_trace_span_unique', 'spans', ['trace_id', 'span_id'], unique=True)

    # GIN indexes for JSONB columns
    op.execute("CREATE INDEX IF NOT EXISTS ix_spans_attributes_gin ON spans USING GIN (attributes)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_spans_resource_attrs_gin ON spans USING GIN (resource_attributes)")

    # Add table comments
    op.execute("COMMENT ON TABLE traces IS 'Aggregated OTEL traces for observability'")
    op.execute("COMMENT ON TABLE spans IS 'Individual OTEL spans within traces'")
    op.execute("COMMENT ON COLUMN traces.trace_id IS 'OpenTelemetry trace ID (32-char hex)'")
    op.execute("COMMENT ON COLUMN spans.span_id IS 'OpenTelemetry span ID (16-char hex)'")


def downgrade() -> None:
    """Drop traces and spans tables with enums."""

    # Drop tables (cascades to indexes)
    op.drop_table('spans')
    op.drop_table('traces')

    # Drop enums
    op.execute("DROP TYPE IF EXISTS trace_status")
    op.execute("DROP TYPE IF EXISTS span_kind")
    op.execute("DROP TYPE IF EXISTS span_status_code")
