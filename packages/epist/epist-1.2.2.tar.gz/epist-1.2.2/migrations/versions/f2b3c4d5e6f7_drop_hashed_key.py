"""drop_hashed_key

Revision ID: f2b3c4d5e6f7
Revises: e1a2b3c4d5e6
Create Date: 2025-11-28 18:00:00.000000

"""

from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "f2b3c4d5e6f7"
down_revision: str | None = "e1a2b3c4d5e6"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # Drop the hashed_key column if it exists
    op.execute("ALTER TABLE api_keys DROP COLUMN IF EXISTS hashed_key")


def downgrade() -> None:
    # Re-add hashed_key (nullable for now to avoid issues)
    op.execute("ALTER TABLE api_keys ADD COLUMN IF NOT EXISTS hashed_key VARCHAR")
