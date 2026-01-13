"""add_rss_ingestion_columns

Revision ID: 363c363d3907
Revises: 379f8e9d0c1e
Create Date: 2026-01-06 18:10:04.678279+00:00

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "363c363d3907"
down_revision: str | None = "379f8e9d0c1e"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # Use inspector to check for column existence before adding
    conn = op.get_bind()
    inspector = sa.inspect(conn)

    # 1. Podcast Feeds
    feed_columns = [c["name"] for c in inspector.get_columns("podcast_feeds")]
    if "description" not in feed_columns:
        op.add_column("podcast_feeds", sa.Column("description", sa.Text(), nullable=True))
    if "author" not in feed_columns:
        op.add_column("podcast_feeds", sa.Column("author", sa.String(), nullable=True))
    if "image_url" not in feed_columns:
        op.add_column("podcast_feeds", sa.Column("image_url", sa.String(), nullable=True))
    if "max_episodes" not in feed_columns:
        op.add_column("podcast_feeds", sa.Column("max_episodes", sa.Integer(), nullable=True))
    if "start_date" not in feed_columns:
        op.add_column("podcast_feeds", sa.Column("start_date", sa.DateTime(), nullable=True))
    if "include_keywords" not in feed_columns:
        op.add_column("podcast_feeds", sa.Column("include_keywords", sa.Text(), nullable=True))
    if "exclude_keywords" not in feed_columns:
        op.add_column("podcast_feeds", sa.Column("exclude_keywords", sa.Text(), nullable=True))

    # 2. Organizations (Double check for missing fields reported by user)
    org_columns = [c["name"] for c in inspector.get_columns("organizations")]
    if "stripe_customer_id" not in org_columns:
        op.add_column("organizations", sa.Column("stripe_customer_id", sa.String(), nullable=True))
        op.create_index(
            op.f("ix_organizations_stripe_customer_id"), "organizations", ["stripe_customer_id"], unique=False
        )
    if "stripe_subscription_id" not in org_columns:
        op.add_column("organizations", sa.Column("stripe_subscription_id", sa.String(), nullable=True))
    if "subscription_status" not in org_columns:
        op.add_column("organizations", sa.Column("subscription_status", sa.String(), nullable=True))


def downgrade() -> None:
    # Safely remove columns if they exist
    conn = op.get_bind()
    inspector = sa.inspect(conn)

    # 1. Organizations
    org_columns = [c["name"] for c in inspector.get_columns("organizations")]
    if "subscription_status" in org_columns:
        op.drop_column("organizations", "subscription_status")
    if "stripe_subscription_id" in org_columns:
        op.drop_column("organizations", "stripe_subscription_id")
    if "stripe_customer_id" in org_columns:
        op.drop_index(op.f("ix_organizations_stripe_customer_id"), table_name="organizations")
        op.drop_column("organizations", "stripe_customer_id")

    # 2. Podcast Feeds
    feed_columns = [c["name"] for c in inspector.get_columns("podcast_feeds")]
    if "exclude_keywords" in feed_columns:
        op.drop_column("podcast_feeds", "exclude_keywords")
    if "include_keywords" in feed_columns:
        op.drop_column("podcast_feeds", "include_keywords")
    if "start_date" in feed_columns:
        op.drop_column("podcast_feeds", "start_date")
    if "max_episodes" in feed_columns:
        op.drop_column("podcast_feeds", "max_episodes")
    if "image_url" in feed_columns:
        op.drop_column("podcast_feeds", "image_url")
    if "author" in feed_columns:
        op.drop_column("podcast_feeds", "author")
    if "description" in feed_columns:
        op.drop_column("podcast_feeds", "description")
