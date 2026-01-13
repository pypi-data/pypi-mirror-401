from datetime import datetime
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


class RequestLogBase(SQLModel):
    request_id: str = Field(index=True)
    method: str
    path: str
    status_code: int
    latency_ms: float
    error_message: str | None = None
    created_at: datetime = Field(default_factory=datetime.utcnow)


class RequestLog(RequestLogBase, table=True):
    __tablename__ = "request_logs"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    ip_address: str | None = None
    user_agent: str | None = None
    api_key_id: UUID | None = Field(default=None, foreign_key="api_keys.id", nullable=True)
    user_id: UUID | None = Field(default=None, foreign_key="users.id", nullable=True)


class RequestLogRead(RequestLogBase):
    id: UUID
    user_id: UUID | None = None
