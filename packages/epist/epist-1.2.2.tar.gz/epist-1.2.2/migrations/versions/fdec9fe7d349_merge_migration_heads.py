"""merge_migration_heads

Revision ID: fdec9fe7d349
Revises: 338d8acc11d4, 99ab8cd76ef1
Create Date: 2025-12-15 17:05:40.075549+00:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel
import pgvector


# revision identifiers, used by Alembic.
revision: str = 'fdec9fe7d349'
down_revision: Union[str, None] = ('338d8acc11d4', '99ab8cd76ef1')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass

