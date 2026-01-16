"""add_user_info_to_traces

Add user_name and user_avatar columns to traces table for
displaying user attribution in the observability UI.

Revision ID: add_user_info_to_traces
Revises: add_trace_span_tables
Create Date: 2026-01-13

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'add_user_info_to_traces'
down_revision: Union[str, Sequence[str], None] = 'add_trace_span_tables'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add user_name and user_avatar columns to traces table."""
    op.add_column('traces', sa.Column('user_name', sa.String(255), nullable=True))
    op.add_column('traces', sa.Column('user_avatar', sa.String(512), nullable=True))

    # Add comment for documentation
    op.execute("COMMENT ON COLUMN traces.user_name IS 'Display name of user who triggered the trace'")
    op.execute("COMMENT ON COLUMN traces.user_avatar IS 'URL to user avatar image'")


def downgrade() -> None:
    """Remove user_name and user_avatar columns from traces table."""
    op.drop_column('traces', 'user_avatar')
    op.drop_column('traces', 'user_name')
