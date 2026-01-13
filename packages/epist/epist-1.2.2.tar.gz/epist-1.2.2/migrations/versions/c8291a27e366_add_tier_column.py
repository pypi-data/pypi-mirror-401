"""add_tier_column

Revision ID: c8291a27e366
Revises: 4d38c93220eb
Create Date: 2025-12-17 06:10:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = 'c8291a27e366'
down_revision: Union[str, None] = '4d38c93220eb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('organizations', sa.Column('tier', sqlmodel.sql.sqltypes.AutoString(), nullable=False, server_default='free'))


def downgrade() -> None:
    op.drop_column('organizations', 'tier')
