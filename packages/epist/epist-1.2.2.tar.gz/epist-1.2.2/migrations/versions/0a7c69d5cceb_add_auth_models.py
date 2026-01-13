"""Add auth models

Revision ID: 0a7c69d5cceb
Revises:
Create Date: 2025-11-27 05:50:30.702281+00:00

"""

from collections.abc import Sequence

import pgvector
import sqlalchemy as sa
import sqlmodel
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "0a7c69d5cceb"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    tables = inspector.get_table_names()

    if "audio_resources" not in tables:
        op.create_table(
            "audio_resources",
            sa.Column("meta_data", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
            sa.Column("id", sa.Uuid(), nullable=False),
            sa.Column("title", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
            sa.Column("source_url", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
            sa.Column("duration_seconds", sa.Float(), nullable=True),
            sa.Column("status", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
            sa.Column("created_at", sa.DateTime(), nullable=False),
            sa.Column("updated_at", sa.DateTime(), nullable=False),
            sa.PrimaryKeyConstraint("id"),
        )
        op.create_index(op.f("ix_audio_resources_source_url"), "audio_resources", ["source_url"], unique=False)
        op.create_index(op.f("ix_audio_resources_status"), "audio_resources", ["status"], unique=False)
        op.create_index(op.f("ix_audio_resources_title"), "audio_resources", ["title"], unique=False)

    if "transcripts" not in tables:
        op.create_table(
            "transcripts",
            sa.Column("id", sa.Uuid(), nullable=False),
            sa.Column("audio_resource_id", sa.Uuid(), nullable=False),
            sa.Column("text", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
            sa.Column("language", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
            sa.Column("model", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
            sa.Column("created_at", sa.DateTime(), nullable=False),
            sa.Column("updated_at", sa.DateTime(), nullable=False),
            sa.ForeignKeyConstraint(
                ["audio_resource_id"],
                ["audio_resources.id"],
            ),
            sa.PrimaryKeyConstraint("id"),
        )

    # Enable vector extension if not exists
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")

    if "transcript_segments" not in tables:
        op.create_table(
            "transcript_segments",
            sa.Column("embedding", pgvector.sqlalchemy.Vector(dim=1536), nullable=True),
            sa.Column("content_vector", postgresql.TSVECTOR(), nullable=True),
            sa.Column("id", sa.Uuid(), nullable=False),
            sa.Column("transcript_id", sa.Uuid(), nullable=False),
            sa.Column("start", sa.Float(), nullable=False),
            sa.Column("end", sa.Float(), nullable=False),
            sa.Column("text", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
            sa.Column("confidence", sa.Float(), nullable=True),
            sa.ForeignKeyConstraint(
                ["transcript_id"],
                ["transcripts.id"],
            ),
            sa.PrimaryKeyConstraint("id"),
        )
        # Create index for vector search
        op.create_index(
            "ix_transcript_segments_embedding",
            "transcript_segments",
            ["embedding"],
            unique=False,
            postgresql_using="ivfflat",
        )
        # Create index for full-text search
        op.create_index(
            "ix_transcript_segments_content_vector",
            "transcript_segments",
            ["content_vector"],
            unique=False,
            postgresql_using="gin",
        )

    if "organizations" not in tables:
        op.create_table(
            "organizations",
            sa.Column("id", sa.Uuid(), nullable=False),
            sa.Column("name", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
            sa.Column("created_at", sa.DateTime(), nullable=False),
            sa.Column("updated_at", sa.DateTime(), nullable=False),
            sa.PrimaryKeyConstraint("id"),
        )

    if "users" not in tables:
        op.create_table(
            "users",
            sa.Column("id", sa.Uuid(), nullable=False),
            sa.Column("email", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
            sa.Column("full_name", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
            sa.Column("organization_id", sa.Uuid(), nullable=True),
            sa.Column("is_active", sa.Boolean(), nullable=False),
            sa.Column("is_superuser", sa.Boolean(), nullable=False),
            sa.Column("created_at", sa.DateTime(), nullable=False),
            sa.Column("updated_at", sa.DateTime(), nullable=False),
            sa.ForeignKeyConstraint(
                ["organization_id"],
                ["organizations.id"],
            ),
            sa.PrimaryKeyConstraint("id"),
        )

    if "api_keys" not in tables:
        op.create_table(
            "api_keys",
            sa.Column("id", sa.Uuid(), nullable=False),
            sa.Column("name", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
            sa.Column("prefix", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
            sa.Column("hashed_key", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
            sa.Column("is_active", sa.Boolean(), nullable=False),
            sa.Column("user_id", sa.Uuid(), nullable=False),
            sa.Column("organization_id", sa.Uuid(), nullable=False),
            sa.Column("last_used_at", sa.DateTime(), nullable=True),
            sa.Column("created_at", sa.DateTime(), nullable=False),
            sa.Column("expires_at", sa.DateTime(), nullable=True),
            sa.ForeignKeyConstraint(
                ["organization_id"],
                ["organizations.id"],
            ),
            sa.ForeignKeyConstraint(
                ["user_id"],
                ["users.id"],
            ),
            sa.PrimaryKeyConstraint("id"),
        )
        op.create_index(op.f("ix_api_keys_hashed_key"), "api_keys", ["hashed_key"], unique=True)
        op.create_index(op.f("ix_api_keys_prefix"), "api_keys", ["prefix"], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("transcript_segments")
    op.drop_index(op.f("ix_apikey_key_hash"), table_name="apikey")
    op.drop_table("apikey")
    op.drop_index(op.f("ix_user_email"), table_name="user")
    op.drop_table("user")
    op.drop_table("transcripts")
    op.drop_table("organization")
    op.drop_index(op.f("ix_audio_resources_title"), table_name="audio_resources")
    op.drop_index(op.f("ix_audio_resources_status"), table_name="audio_resources")
    op.drop_index(op.f("ix_audio_resources_source_url"), table_name="audio_resources")
    op.drop_table("audio_resources")
    # ### end Alembic commands ###
