from datetime import datetime
from uuid import uuid4

from sqlmodel import ARRAY, Column, Field, SQLModel, String


class WebhookEndpoint(SQLModel, table=True):
    __tablename__ = "webhook_endpoints"

    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    organization_id: str = Field(index=True, nullable=False)
    url: str = Field(nullable=False)
    secret: str = Field(nullable=False, description="Signing secret for verifying payloads")
    events: list[str] = Field(sa_column=Column(ARRAY(String)), description="List of events to subscribe to")
    description: str | None = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = Field(default=True)
