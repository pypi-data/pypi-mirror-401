"""add_key_hash_and_updated_at

Revision ID: e1a2b3c4d5e6
Revises: 46f41c459437
Create Date: 2025-11-27 21:20:00.000000

"""

from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "e1a2b3c4d5e6"
down_revision: str | None = "bad3402454db"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # Add updated_at to organizations
    op.execute("ALTER TABLE organizations ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP WITHOUT TIME ZONE")
    op.execute("UPDATE organizations SET updated_at = created_at WHERE updated_at IS NULL")
    op.alter_column("organizations", "updated_at", nullable=False)

    # Add updated_at to users
    op.execute("ALTER TABLE users ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP WITHOUT TIME ZONE")
    op.execute("UPDATE users SET updated_at = created_at WHERE updated_at IS NULL")
    op.alter_column("users", "updated_at", nullable=False)

    # Add updated_at and key_hash to api_keys
    op.execute("ALTER TABLE api_keys ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP WITHOUT TIME ZONE")
    op.execute("UPDATE api_keys SET updated_at = created_at WHERE updated_at IS NULL")
    op.alter_column("api_keys", "updated_at", nullable=False)

    op.execute("ALTER TABLE api_keys ADD COLUMN IF NOT EXISTS key_hash VARCHAR")
    # Check if index exists before creating
    op.execute("CREATE INDEX IF NOT EXISTS ix_api_keys_key_hash ON api_keys (key_hash)")


def downgrade() -> None:
    op.drop_index(op.f("ix_api_keys_key_hash"), table_name="api_keys")
    op.drop_column("api_keys", "key_hash")
    op.drop_column("api_keys", "updated_at")
    op.drop_column("users", "updated_at")
    op.drop_column("organizations", "updated_at")
