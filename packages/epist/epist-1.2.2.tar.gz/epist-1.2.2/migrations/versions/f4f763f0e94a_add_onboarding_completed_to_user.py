"""add onboarding_completed to user

Revision ID: f4f763f0e94a
Revises: 20b3f9ccf641
Create Date: 2025-12-22 04:39:52.382460+00:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = 'f4f763f0e94a'
down_revision: Union[str, None] = '20b3f9ccf641'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add onboarding_completed column with default False
    op.add_column('users', sa.Column('onboarding_completed', sa.Boolean(), nullable=False, server_default=sa.text('false')))


def downgrade() -> None:
    # Remove onboarding_completed column
    op.drop_column('users', 'onboarding_completed')
