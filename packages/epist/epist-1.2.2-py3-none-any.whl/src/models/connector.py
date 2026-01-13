import uuid
from datetime import datetime

from sqlmodel import Field, Relationship, SQLModel

from models.auth import Organization


class PodcastFeed(SQLModel, table=True):
    __tablename__ = "podcast_feeds"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    url: str = Field(index=True)
    name: str
    organization_id: uuid.UUID = Field(foreign_key="organizations.id")
    description: str | None = None
    author: str | None = None
    image_url: str | None = None
    is_active: bool = Field(default=True)
    refresh_interval_minutes: int | None = Field(default=None)  # None = Manual
    last_synced_at: datetime | None = None
    max_episodes: int | None = None
    start_date: datetime | None = None
    include_keywords: str | None = None
    exclude_keywords: str | None = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship
    organization: Organization = Relationship()
