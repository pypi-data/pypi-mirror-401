"""merge_heads

Revision ID: 4d38c93220eb
Revises: 7b8c9d0e1f2a, fdec9fe7d349
Create Date: 2025-12-17 05:09:36.871512+00:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel
import pgvector


# revision identifiers, used by Alembic.
revision: str = '4d38c93220eb'
down_revision: Union[str, None] = ('7b8c9d0e1f2a', 'fdec9fe7d349')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass

