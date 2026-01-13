"""add trace_events table

Revision ID: 6a7b8c9d0e1f
Revises: 5f4e3d2c1b0a
Create Date: 2025-12-01 20:30:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
import sqlmodel
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "6a7b8c9d0e1f"
down_revision: str | None = "5f4e3d2c1b0a"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    tables = inspector.get_table_names()

    if "trace_events" not in tables:
        op.create_table(
            "trace_events",
            sa.Column("id", sa.Uuid(), nullable=False),
            sa.Column("trace_id", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
            sa.Column("span_id", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
            sa.Column("parent_span_id", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
            sa.Column("event_type", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
            sa.Column("component", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
            sa.Column("name", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
            sa.Column("inputs", postgresql.JSON(astext_type=sa.Text()), nullable=True),
            sa.Column("outputs", postgresql.JSON(astext_type=sa.Text()), nullable=True),
            sa.Column("metadata", postgresql.JSON(astext_type=sa.Text()), nullable=True),
            sa.Column("start_time", sa.DateTime(), nullable=False),
            sa.Column("end_time", sa.DateTime(), nullable=False),
            sa.Column("latency_ms", sa.Float(), nullable=False),
            sa.Column("status", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
            sa.Column("error_message", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
            sa.Column("created_at", sa.DateTime(), nullable=False),
            sa.PrimaryKeyConstraint("id"),
        )
        op.create_index(op.f("ix_trace_events_trace_id"), "trace_events", ["trace_id"], unique=False)
        op.create_index(op.f("ix_trace_events_span_id"), "trace_events", ["span_id"], unique=False)
        op.create_index(op.f("ix_trace_events_parent_span_id"), "trace_events", ["parent_span_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_trace_events_parent_span_id"), table_name="trace_events")
    op.drop_index(op.f("ix_trace_events_span_id"), table_name="trace_events")
    op.drop_index(op.f("ix_trace_events_trace_id"), table_name="trace_events")
    op.drop_table("trace_events")
