from datetime import datetime
from uuid import UUID, uuid4

from pgvector.sqlalchemy import Vector
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import JSON, TSVECTOR
from sqlmodel import Field, Relationship, SQLModel


class TranscriptSegmentBase(SQLModel):
    start: float
    end: float
    text: str
    speaker: str | None = None
    confidence: float | None = None

    # Context overlap: text from previous/next chunks for better retrieval
    overlap_context_before: str | None = Field(default=None, max_length=500)
    overlap_context_after: str | None = Field(default=None, max_length=500)

    # Word-level timestamps (JSON array)
    words: list[dict] | None = Field(default=None, sa_column=Column("words", JSON))

    # Vector Embedding (1536 dimensions for text-embedding-3-small)
    embedding: list[float] | None = Field(default=None, sa_column=Column(Vector(1536)))

    # Full-Text Search Vector
    content_vector: str | None = Field(default=None, sa_column=Column(TSVECTOR))


class TranscriptSegment(TranscriptSegmentBase, table=True):
    __tablename__ = "transcript_segments"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    transcript_id: UUID = Field(foreign_key="transcripts.id", ondelete="CASCADE")

    transcript: "Transcript" = Relationship(back_populates="segments")


class TranscriptBase(SQLModel):
    audio_resource_id: UUID = Field(foreign_key="audio_resources.id", ondelete="CASCADE")
    language: str | None = None
    model: str | None = None
    text: str  # Full text


class Transcript(TranscriptBase, table=True):
    __tablename__ = "transcripts"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    segments: list[TranscriptSegment] = Relationship(back_populates="transcript")


class TranscriptSegmentRead(TranscriptSegmentBase):
    id: UUID
    transcript_id: UUID


class TranscriptReadWithSegments(TranscriptBase):
    id: UUID
    created_at: datetime
    segments: list[TranscriptSegmentRead]
