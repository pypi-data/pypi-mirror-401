"""add_plan_executions_table

Creates the plan_executions table for tracking multi-task plan orchestration.
Also adds plan_execution_id foreign key to executions table.

Revision ID: add_plan_executions
Revises: 43abf98d6a01
Create Date: 2025-12-11 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'add_plan_executions'
down_revision: Union[str, Sequence[str], None] = '43abf98d6a01'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """
    Create plan_executions table and add foreign key to executions.
    """

    # Create plan_executions table
    op.create_table(
        'plan_executions',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('execution_id', sa.String(255), unique=True, nullable=False, index=True),
        sa.Column('organization_id', sa.String(255), nullable=False, index=True),
        sa.Column('agent_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('title', sa.Text(), nullable=False),
        sa.Column('summary', sa.Text(), nullable=True),
        sa.Column('total_tasks', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('completed_tasks', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('failed_tasks', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('status', sa.String(50), nullable=False, server_default='running', index=True),
        sa.Column('dag_state', postgresql.JSONB(astext_type=sa.Text()), nullable=True, server_default='{}'),
        sa.Column('total_tokens', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('total_execution_time_seconds', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('estimated_cost_usd', sa.Numeric(10, 4), nullable=True),
        sa.Column('actual_cost_usd', sa.Numeric(10, 4), nullable=True),
        sa.Column('plan_json', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('started_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('completed_at', sa.DateTime(timezone=True), nullable=True),
    )

    # Create indexes
    op.create_index(
        'idx_plan_executions_org_status',
        'plan_executions',
        ['organization_id', 'status']
    )
    op.create_index(
        'idx_plan_executions_created',
        'plan_executions',
        ['created_at']
    )

    # Add plan_execution_id to executions table
    op.add_column(
        'executions',
        sa.Column('plan_execution_id', postgresql.UUID(as_uuid=True), nullable=True)
    )

    # Create foreign key constraint
    op.create_foreign_key(
        'fk_executions_plan_execution',
        'executions',
        'plan_executions',
        ['plan_execution_id'],
        ['id'],
        ondelete='CASCADE'
    )

    # Create index on plan_execution_id
    op.create_index(
        'idx_executions_plan_execution_id',
        'executions',
        ['plan_execution_id']
    )

    print("✅ Created plan_executions table")
    print("✅ Added plan_execution_id to executions table")


def downgrade() -> None:
    """
    Remove plan_executions table and foreign key.
    """

    # Drop index
    op.drop_index('idx_executions_plan_execution_id', table_name='executions')

    # Drop foreign key
    op.drop_constraint('fk_executions_plan_execution', 'executions', type_='foreignkey')

    # Drop column from executions
    op.drop_column('executions', 'plan_execution_id')

    # Drop indexes
    op.drop_index('idx_plan_executions_created', table_name='plan_executions')
    op.drop_index('idx_plan_executions_org_status', table_name='plan_executions')

    # Drop table
    op.drop_table('plan_executions')

    print("✅ Removed plan_executions table and related changes")
