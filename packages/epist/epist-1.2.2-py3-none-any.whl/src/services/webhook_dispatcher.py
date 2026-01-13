import hashlib
import hmac
import json
import logging
from datetime import datetime
from typing import Any

import httpx
from fastapi import BackgroundTasks
from sqlmodel import Session, select

from core.config import settings
from models.webhook import WebhookEndpoint

logger = logging.getLogger(__name__)


class WebhookDispatcher:
    def __init__(self, session: Session):
        self.session = session

    async def dispatch_event(
        self, org_id: str, event_type: str, payload: dict[str, Any], background_tasks: BackgroundTasks
    ):
        """
        Finds all webhook subscriptions for the org and event_type,
        and schedules delivery.
        """
        statement = select(WebhookEndpoint).where(WebhookEndpoint.organization_id == org_id, WebhookEndpoint.is_active)
        results = self.session.exec(statement).all()

        # Filter in memory for array overlap (or use pgvector/pgarray operators if configured)
        # Assuming simple list check for now
        subscribers = [ep for ep in results if event_type in ep.events]

        if not subscribers:
            return

        event_id = f"evt_{datetime.now().timestamp()}"
        full_payload = {
            "id": event_id,
            "type": event_type,
            "created_at": datetime.utcnow().isoformat(),
            "data": payload,
        }

        for endpoint in subscribers:
            # In production, push to Cloud Tasks here for retry/backoff.
            # For now, use FastAPI BackgroundTasks for simplicity.
            background_tasks.add_task(
                self._deliver_payload, url=endpoint.url, secret=endpoint.secret, payload=full_payload
            )

    async def deliver_to_url(
        self, url: str, event_type: str, payload: dict[str, Any], secret: str | None = None
    ):
        """
        Delivers a one-off webhook to a specific URL.
        If secret is not provided, uses a default placeholder.
        """
        event_id = f"evt_adhoc_{datetime.now().timestamp()}"
        full_payload = {
            "id": event_id,
            "type": event_type,
            "created_at": datetime.utcnow().isoformat(),
            "data": payload,
        }
        # Use a default secret if none provided for ad-hoc webhooks
        # In a real system, this might be a per-user API key or a global signing secret
        signing_secret = secret or settings.SECRET_KEY
        await self._deliver_payload(url=url, secret=signing_secret, payload=full_payload)

    async def _deliver_payload(self, url: str, secret: str, payload: dict[str, Any]):
        """
        Delivers the webhook with a signature header.
        """
        body = json.dumps(payload, ensure_ascii=False)
        timestamp = str(int(datetime.now().timestamp()))

        # Create Signature: HMAC-SHA256(timestamp + "." + body, secret)
        to_sign = f"{timestamp}.{body}".encode()
        signature = hmac.new(secret.encode(), to_sign, hashlib.sha256).hexdigest()

        headers = {
            "Content-Type": "application/json",
            "Epist-Signature": f"t={timestamp},v1={signature}",
            "User-Agent": "Epist-Webhook/1.0",
        }

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.post(url, content=body, headers=headers)
                resp.raise_for_status()
                logger.info(f"Webhook delivered to {url} [status={resp.status_code}]")
        except Exception as e:
            logger.error(f"Webhook delivery failed to {url}: {e}")
            # Here is where we would rely on Cloud Tasks to retry
