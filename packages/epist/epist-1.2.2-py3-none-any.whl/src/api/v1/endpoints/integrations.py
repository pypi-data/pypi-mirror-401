from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, HttpUrl
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from api.deps import get_current_user, get_session
from models.auth import User
from models.webhook import WebhookEndpoint

router = APIRouter()


class WebhookCreate(BaseModel):
    url: HttpUrl
    events: list[str]
    description: str | None = None


class WebhookRead(BaseModel):
    id: str
    url: str
    events: list[str]
    description: str | None
    created_at: Any
    is_active: bool


class WebhookUpdate(BaseModel):
    url: HttpUrl | None = None
    events: list[str] | None = None
    is_active: bool | None = None


class WebhookCreateResponse(WebhookRead):
    secret: str


@router.post("/", response_model=WebhookCreateResponse)
async def create_webhook(
    webhook: WebhookCreate, current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)
):
    """Register a new webhook endpoint."""
    # Generate a random signing secret (in production, show this once)
    import secrets

    signing_secret = f"whsec_{secrets.token_hex(24)}"

    db_webhook = WebhookEndpoint(
        organization_id=str(current_user.organization_id),
        url=str(webhook.url),
        events=webhook.events,
        description=webhook.description,
        secret=signing_secret,
    )
    session.add(db_webhook)
    await session.commit()
    await session.refresh(db_webhook)
    return db_webhook


@router.get("/", response_model=list[WebhookRead])
async def list_webhooks(current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    """List all webhooks for the organization."""
    statement = select(WebhookEndpoint).where(WebhookEndpoint.organization_id == str(current_user.organization_id))
    result = await session.exec(statement)
    return result.all()


@router.delete("/{webhook_id}")
async def delete_webhook(
    webhook_id: str, current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)
):
    """Delete a webhook endpoint."""
    webhook = await session.get(WebhookEndpoint, webhook_id)
    if not webhook or webhook.organization_id != str(current_user.organization_id):
        raise HTTPException(status_code=404, detail="Webhook not found")

    await session.delete(webhook)
    await session.commit()
    return {"ok": True}
