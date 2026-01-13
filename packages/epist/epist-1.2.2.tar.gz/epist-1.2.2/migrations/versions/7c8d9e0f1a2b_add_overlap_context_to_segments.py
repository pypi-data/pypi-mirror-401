"""add_overlap_context_to_segments

Revision ID: 7c8d9e0f1a2b
Revises: 6a7b8c9d0e1f
Create Date: 2025-12-02 21:05:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "7c8d9e0f1a2b"
down_revision: str | None = "6a7b8c9d0e1f"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # Add overlap context columns to transcript_segments
    op.add_column("transcript_segments", sa.Column("overlap_context_before", sa.String(length=500), nullable=True))
    op.add_column("transcript_segments", sa.Column("overlap_context_after", sa.String(length=500), nullable=True))


def downgrade() -> None:
    # Remove overlap context columns
    op.drop_column("transcript_segments", "overlap_context_after")
    op.drop_column("transcript_segments", "overlap_context_before")
