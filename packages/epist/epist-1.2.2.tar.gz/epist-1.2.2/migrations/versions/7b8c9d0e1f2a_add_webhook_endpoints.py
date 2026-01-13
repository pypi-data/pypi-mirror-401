"""Add webhook endpoints

Revision ID: 7b8c9d0e1f2a
Revises: 0a7c69d5cceb
Create Date: 2025-12-16 12:00:00.000000

"""
import sqlalchemy as sa
import sqlmodel
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "7b8c9d0e1f2a"
down_revision: str | None = "0a7c69d5cceb"
branch_labels: str | None = None
depends_on: str | None = None


def upgrade() -> None:
    op.create_table(
        "webhook_endpoints",
        sa.Column("id", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("organization_id", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("url", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("secret", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("events", sa.ARRAY(sa.String()), nullable=True),
        sa.Column("description", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_webhook_endpoints_organization_id"), "webhook_endpoints", ["organization_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_webhook_endpoints_organization_id"), table_name="webhook_endpoints")
    op.drop_table("webhook_endpoints")
