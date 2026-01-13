"""add_last_webhook_id

Revision ID: e7312b38f742
Revises: c8291a27e366
Create Date: 2025-12-18 06:40:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = 'e7312b38f742'
down_revision: Union[str, None] = 'c8291a27e366'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('organizations', sa.Column('last_webhook_id', sqlmodel.sql.sqltypes.AutoString(), nullable=True))


def downgrade() -> None:
    op.drop_column('organizations', 'last_webhook_id')
