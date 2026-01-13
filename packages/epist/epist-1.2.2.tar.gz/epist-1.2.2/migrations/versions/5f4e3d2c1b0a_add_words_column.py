"""add words column to transcript_segments

Revision ID: 5f4e3d2c1b0a
Revises: 46f41c459437
Create Date: 2025-12-02 02:45:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "5f4e3d2c1b0a"
down_revision: str | None = "f2b3c4d5e6f7"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # Add words column to transcript_segments table
    op.add_column("transcript_segments", sa.Column("words", sa.JSON(), nullable=True))


def downgrade() -> None:
    # Remove words column from transcript_segments table
    op.drop_column("transcript_segments", "words")
