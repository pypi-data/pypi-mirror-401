import hashlib
import hmac
import json
import logging

import httpx
import stripe
from fastapi import APIRouter, Depends, Header, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from db.session import get_session
from services.stripe_service import StripeService

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/stripe")
async def stripe_webhook(
    request: Request, stripe_signature: str = Header(None), db: AsyncSession = Depends(get_session)
):
    """
    Handle incoming Stripe webhook events.
    """
    payload = await request.body()
    sig_header = stripe_signature
    webhook_secret = settings.STRIPE_WEBHOOK_SECRET

    logger.info(f"Received Stripe Webhook. Signature: {sig_header[:20] if sig_header else 'None'}...")

    if not sig_header or not webhook_secret:
        raise HTTPException(status_code=400, detail="Missing signature or secret")

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, webhook_secret)
    except ValueError as e:
        # Invalid payload
        logger.error(f"Invalid payload: {e}")
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        logger.error(f"Invalid signature: {e}")
        raise HTTPException(status_code=400, detail="Invalid signature")

    stripe_service = StripeService(db)
    await stripe_service.handle_webhook(event)

    return {"status": "success"}


@router.post("/sentry")
async def sentry_webhook(request: Request, sentry_hook_signature: str = Header(None, alias="sentry-hook-signature")):
    """
    Handle incoming Sentry webhook alerts and trigger Antigravity auto-fix.
    """
    payload = await request.body()

    # 1. Verify Signature (if secret is configured)
    if settings.SENTRY_WEBHOOK_SECRET:
        if not sentry_hook_signature:
            raise HTTPException(status_code=401, detail="Missing signature")

        digest = hmac.new(settings.SENTRY_WEBHOOK_SECRET.encode(), payload, hashlib.sha256).hexdigest()

        if not hmac.compare_digest(digest, sentry_hook_signature):
            raise HTTPException(status_code=401, detail="Invalid signature")

    # 2. Extract Error Data
    try:
        event_data = json.loads(payload)
        # Sentry alerts have different structures based on type.
        # For 'issue', it's in event_data['data']['issue']
        issue = event_data.get("data", {}).get("issue", {})
        error_msg = issue.get("title", "Unknown Error")
        issue_id = issue.get("id", "unknown")

        # In a real integration, we might want to fetch the full traceback from Sentry API
        # if it's not in the webhook payload. For now, we pass the title and ID.
        logger.info(f"Sentry alert received: {error_msg} (ID: {issue_id})")
    except Exception as e:
        logger.error(f"Failed to parse Sentry payload: {e}")
        raise HTTPException(status_code=400, detail="Invalid payload")

    # 3. Trigger GitHub Workflow
    if not settings.GITHUB_TOKEN:
        logger.error("GITHUB_TOKEN not configured. Cannot trigger auto-fix.")
        return {"status": "received", "action": "none", "reason": "missing_github_token"}

    repo = settings.GITHUB_REPO
    url = f"https://api.github.com/repos/{repo}/dispatches"

    headers = {
        "Authorization": f"token {settings.GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "Epist-Sentry-Trigger",
    }

    dispatch_payload = {
        "event_type": "sentry-error-alert",
        "client_payload": {"error_message": error_msg, "issue_id": issue_id, "sentry_event": event_data},
    }

    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(url, json=dispatch_payload, headers=headers)
            resp.raise_for_status()
            logger.info(f"Successfully triggered GitHub workflow for issue {issue_id}")
    except Exception as e:
        logger.error(f"Failed to trigger GitHub workflow: {e}")
        return {"status": "error", "message": str(e)}

    return {"status": "success", "issue_id": issue_id}
