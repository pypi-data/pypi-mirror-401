from datetime import datetime
from typing import Any
from uuid import UUID, uuid4

from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import JSON
from sqlmodel import Field, SQLModel


class TraceEvent(SQLModel, table=True):
    __tablename__ = "trace_events"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    trace_id: str = Field(index=True)
    span_id: str = Field(index=True)
    parent_span_id: str | None = Field(default=None, index=True)
    user_id: UUID | None = Field(default=None, foreign_key="users.id", nullable=True)

    event_type: str  # e.g., "retrieval", "llm_call", "tool_use"
    component: str  # e.g., "SearchService", "ChatEndpoint"
    name: str  # Human readable name e.g. "Vector Search"

    inputs: dict[str, Any] = Field(default={}, sa_column=Column(JSON))
    outputs: dict[str, Any] = Field(default={}, sa_column=Column(JSON))
    meta: dict = Field(default_factory=dict, sa_column=Column("metadata", JSON))

    start_time: datetime
    end_time: datetime
    latency_ms: float

    status: str = "success"  # success, error
    error_message: str | None = None

    created_at: datetime = Field(default_factory=datetime.utcnow)
