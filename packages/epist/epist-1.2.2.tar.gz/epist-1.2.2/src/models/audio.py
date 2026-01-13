from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import UUID, uuid4

from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import Field, SQLModel


class AudioResourceBase(SQLModel):
    title: str | None = Field(default=None, index=True)
    source_url: str = Field(index=True)  # Raw audio URL
    duration_seconds: float | None = None
    status: str = Field(default="pending", index=True)  # pending, processing, completed, failed
    meta_data: dict[str, Any] | None = Field(default_factory=dict, sa_column=Column(JSONB))
    storage_gcs_uri: str | None = Field(default=None, index=True)
    is_public: bool = Field(default=False, index=True)
    webhook_url: str | None = Field(default=None)
    error: str | None = Field(default=None, index=False)


class AudioResource(AudioResourceBase, table=True):
    __tablename__ = "audio_resources"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    user_id: UUID | None = Field(default=None, foreign_key="users.id", nullable=True)

    # Relationships
    # Use string forward reference to avoid circular imports
    # We need to import Transcript only for type checking if needed, but SQLModel handles string refs well
    # However, for back_populates to work, the other model must exist.
    # We won't add the relationship here yet to avoid circular import issues until we are sure.
    # Actually, let's add it but use TYPE_CHECKING


class AudioResourceCreate(AudioResourceBase):
    pass


class AudioResourceUpdate(SQLModel):
    title: str | None = None
    is_public: bool | None = None


class AudioResourceRead(AudioResourceBase):
    id: UUID
    created_at: datetime
    transcript: str | None = None
    summary: str | None = None
    entities: list[dict] | None = None


class AudioUrlRequest(SQLModel):
    url: str | None = None
    audio_url: str | None = None
    rag_enabled: bool = True
    language: str = "en"
    preset: str = "general"
    chunking_config: dict | str | None = None
    webhook_url: str | None = None
