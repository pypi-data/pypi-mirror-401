"""add error field to audio resource

Revision ID: c1f92da73359
Revises: e7312b38f742
Create Date: 2025-12-18 18:42:03.812809+00:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel
import pgvector


# revision identifiers, used by Alembic.
revision: str = 'c1f92da73359'
down_revision: Union[str, None] = 'e7312b38f742'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('audio_resources', sa.Column('error', sa.Text(), nullable=True))


def downgrade() -> None:
    op.drop_column('audio_resources', 'error')

