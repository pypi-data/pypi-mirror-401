"""add storage_gcs_uri to audio_resource

Revision ID: 3a4b5c6d7e8f
Revises: 363c363d3907
Create Date: 2026-01-09 14:15:00.000000+00:00

"""
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "3a4b5c6d7e8f"
down_revision: str | None = "363c363d3907"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # Use inspector to check for column existence before adding
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    
    audio_columns = [c["name"] for c in inspector.get_columns("audio_resources")]
    if "storage_gcs_uri" not in audio_columns:
        op.add_column("audio_resources", sa.Column("storage_gcs_uri", sa.String(), nullable=True))
        op.create_index(
            op.f("ix_audio_resources_storage_gcs_uri"), "audio_resources", ["storage_gcs_uri"], unique=False
        )
    
    # Data Migration: Move storage_gcs_uri from meta_data to the new column
    # We use execute for this
    op.execute(
        """
        UPDATE audio_resources 
        SET storage_gcs_uri = meta_data->>'storage_gcs_uri'
        WHERE meta_data ? 'storage_gcs_uri' AND storage_gcs_uri IS NULL
        """
    )


def downgrade() -> None:
    # Downgrade: We don't necessarily need to move data back to meta_data as metadata update
    # and column update are separate, but it's good practice to keep the column if possible.
    # However, standard downgrade for add_column is drop_column.
    op.drop_index(op.f("ix_audio_resources_storage_gcs_uri"), table_name="audio_resources")
    op.drop_column("audio_resources", "storage_gcs_uri")
