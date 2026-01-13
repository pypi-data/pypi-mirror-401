"""add user_id to tables

Revision ID: 1234567890ab
Revises: f2b3c4d5e6f7
Create Date: 2025-12-03 00:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "1234567890ab"
down_revision: str | None = "7c8d9e0f1a2b"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # Add user_id to audio_resources
    op.add_column("audio_resources", sa.Column("user_id", sa.Uuid(), nullable=True))
    op.create_foreign_key(None, "audio_resources", "users", ["user_id"], ["id"])

    # Add user_id to trace_events
    op.add_column("trace_events", sa.Column("user_id", sa.Uuid(), nullable=True))
    op.create_foreign_key(None, "trace_events", "users", ["user_id"], ["id"])

    # Add user_id to request_logs
    op.add_column("request_logs", sa.Column("user_id", sa.Uuid(), nullable=True))
    op.create_foreign_key(None, "request_logs", "users", ["user_id"], ["id"])


def downgrade() -> None:
    op.drop_constraint(None, "request_logs", type_="foreignkey")
    op.drop_column("request_logs", "user_id")

    op.drop_constraint(None, "trace_events", type_="foreignkey")
    op.drop_column("trace_events", "user_id")

    op.drop_constraint(None, "audio_resources", type_="foreignkey")
    op.drop_column("audio_resources", "user_id")
