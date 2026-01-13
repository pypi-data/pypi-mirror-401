"""add usage tracking columns

Revision ID: 379f8e9d0c1e
Revises: 263aa63a981b
Create Date: 2025-12-30 18:30:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '379f8e9d0c1e'
down_revision: Union[str, None] = '263aa63a981b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Add columns to organizations
    op.add_column('organizations', sa.Column('billing_cycle_anchor', sa.DateTime(), nullable=True))
    op.add_column('organizations', sa.Column('monthly_audio_seconds', sa.Integer(), nullable=False, server_default='0'))
    op.add_column('organizations', sa.Column('usage_reset_at', sa.DateTime(), nullable=False, server_default=sa.func.now()))


def downgrade() -> None:
    op.drop_column('organizations', 'billing_cycle_anchor')
    op.drop_column('organizations', 'monthly_audio_seconds')
    op.drop_column('organizations', 'usage_reset_at')
