import logging
from uuid import UUID

import stripe
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from core.config import settings
from models.auth import Organization

logger = logging.getLogger(__name__)

stripe.api_key = settings.STRIPE_SECRET_KEY


class StripeService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_checkout_session(
        self, org_id: str, plan_id: str | None = None, success_url: str | None = None, cancel_url: str | None = None
    ) -> str:
        """
        Create a Stripe Checkout Session for subscription upgrade.
        """
        stmt = select(Organization).where(Organization.id == org_id)
        result = await self.db.exec(stmt)
        org = result.first()
        if not org:
            raise HTTPException(status_code=404, detail="Organization not found")

        try:
            # If org already has a customer ID, use it
            customer_kwargs = {}
            if org.stripe_customer_id:
                customer_kwargs["customer"] = org.stripe_customer_id

            # Default success/cancel URLs if not provided
            base_url = settings.FRONTEND_URL
            if not success_url:
                success_url = f"{base_url}/dashboard/profile?session_id={{CHECKOUT_SESSION_ID}}"
            if not cancel_url:
                cancel_url = f"{base_url}/dashboard/profile"

            # Resolve Price ID
            # Frontend sends "pro" or "free". We mapped "pro" to actual Stripe Price ID via Env Var.
            # Resolve Price ID
            # Frontend sends "pro" or "starter"
            price_id = None
            if plan_id == "pro":
                price_id = settings.STRIPE_PRICE_ID_PRO
            elif plan_id == "starter":
                price_id = settings.STRIPE_PRICE_ID_STARTER

            if not price_id:
                raise HTTPException(status_code=400, detail="Invalid Price ID configuration")

            session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=[
                    {
                        "price": price_id,
                        "quantity": 1,
                    },
                ],
                mode="subscription",
                success_url=success_url,
                cancel_url=cancel_url,
                client_reference_id=str(org.id),
                subscription_data={"metadata": {"org_id": str(org.id)}},
                **customer_kwargs,
            )
            if not session.url:
                raise HTTPException(status_code=500, detail="Stripe session URL not generated")
            return session.url
        except Exception as e:
            logger.error(f"Stripe Checkout Error: {e}", exc_info=True)
            raise HTTPException(status_code=500, detail="Failed to create checkout session")

    async def create_portal_session(self, org_id: str, return_url: str | None = None) -> str:
        """
        Create a billing portal session for managing subscription.
        """
        stmt = select(Organization).where(Organization.id == org_id)
        result = await self.db.exec(stmt)
        org = result.first()
        if not org or not org.stripe_customer_id:
            raise HTTPException(status_code=400, detail="Organization has no billing capability")

        base_url = settings.FRONTEND_URL
        if not return_url:
            return_url = f"{base_url}/dashboard/profile"

        try:
            session = stripe.billing_portal.Session.create(
                customer=org.stripe_customer_id,
                return_url=return_url,
            )
            return session.url
        except Exception as e:
            logger.error(f"Stripe Portal Error: {e}", exc_info=True)
            raise HTTPException(status_code=500, detail="Failed to create portal session")

    async def handle_webhook(self, event: dict):
        """
        Handle Stripe webhook events.
        """
        event_type = event["type"]
        data = event["data"]["object"]

        # Idempotency Check
        # We need the Org ID to check idempotency.
        # Events like checkout.session.completed have client_reference_id (Org ID).
        # Subscription events have customer ID -> resolve to Org -> check last_webhook_id.

        event_id = event["id"]

        if event_type == "checkout.session.completed":
            await self._handle_checkout_completed(data, event_id)
        elif event_type == "customer.subscription.updated":
            await self._handle_subscription_updated(data, event_id)
        elif event_type == "customer.subscription.deleted":
            await self._handle_subscription_deleted(data, event_id)
        elif event_type == "invoice.payment_succeeded":
            await self._handle_invoice_payment_succeeded(data, event_id)

        # Add handling for successful payment / generic invoice payment succeeded if needed

    async def _handle_checkout_completed(self, session: dict, event_id: str):
        client_reference_id = session.get("client_reference_id")
        customer_id = session.get("customer")
        subscription_id = session.get("subscription")

        if client_reference_id:
            try:
                org_uuid = UUID(client_reference_id)
            except ValueError:
                logger.error(f"Invalid client_reference_id: {client_reference_id}")
                return

            stmt = select(Organization).where(Organization.id == org_uuid)
            result = await self.db.exec(stmt)
            org = result.first()
            if org:
                # Idempotency
                if org.last_webhook_id == event_id:
                    logger.info(f"Skipping duplicate webhook {event_id} for org {org.id}")
                    return

                org.stripe_customer_id = customer_id
                org.stripe_subscription_id = subscription_id
                org.subscription_status = "active"
                org.tier = "pro"
                org.last_webhook_id = event_id
                self.db.add(org)
                await self.db.commit()
                logger.info(f"Organization {org.id} subscribed. Customer: {customer_id}")

    async def _handle_subscription_updated(self, subscription: dict, event_id: str):
        customer_id = subscription.get("customer")
        status = subscription.get("status")
        current_period_end = subscription.get("current_period_end")
        items = subscription.get("items", {}).get("data", [])

        stmt = select(Organization).where(Organization.stripe_customer_id == customer_id)
        result = await self.db.exec(stmt)
        org = result.first()
        if org:
            if org.last_webhook_id == event_id:
                logger.info(f"Skipping duplicate webhook {event_id} for org {org.id}")
                return

            org.subscription_status = status
            # Convert timestamp to datetime if needed, or if DB stores it as such
            from datetime import datetime

            if current_period_end:
                org.current_period_end = datetime.fromtimestamp(current_period_end)

            # Downgrade logic if not active
            if status in ["canceled", "unpaid", "past_due"]:
                # Optional: Grace period handling? For now, strict downgrade.
                pass
                # We might want to keep 'pro' until end of period, but 'status' reflects Stripe state.
                # The 'tier' check logic should inspect 'status' + 'current_period_end' ideally.

            # Determine Tier from Price ID
            if status in ["active", "trialing"]:
                current_price_id = items[0]["price"]["id"] if items else None
                if current_price_id == settings.STRIPE_PRICE_ID_PRO:
                    org.tier = "pro"
                elif current_price_id == settings.STRIPE_PRICE_ID_STARTER:
                    org.tier = "starter"
                else:
                    logger.warning(f"Unknown price ID {current_price_id} for org {org.id}. Defaulting to 'free'.")
                    org.tier = "free"
            else:
                org.tier = "free"

            org.last_webhook_id = event_id  # Add this line
            self.db.add(org)
            await self.db.commit()
            logger.info(f"Updated subscription for org {org.id}: {status}")

    async def _handle_subscription_deleted(self, subscription: dict, event_id: str):
        customer_id = subscription.get("customer")
        stmt = select(Organization).where(Organization.stripe_customer_id == customer_id)
        result = await self.db.exec(stmt)
        org = result.first()
        if org:
            if org.last_webhook_id == event_id:
                logger.info(f"Skipping duplicate webhook {event_id} for org {org.id}")  # Add this line
                return

            org.subscription_status = "canceled"
            org.tier = "free"
            org.stripe_subscription_id = None
            org.last_webhook_id = event_id  # Add this line
            self.db.add(org)
            await self.db.commit()
            logger.info(f"Subscription canceled for org {org.id}")

    async def _handle_invoice_payment_succeeded(self, invoice: dict, event_id: str):
        customer_id = invoice.get("customer")
        billing_reason = invoice.get("billing_reason")

        # Only reset on subscription cycle (renewal)
        if billing_reason == "subscription_cycle":
            stmt = select(Organization).where(Organization.stripe_customer_id == customer_id)
            result = await self.db.exec(stmt)
            org = result.first()

            if org:
                if org.last_webhook_id == event_id:
                    logger.info(f"Skipping duplicate webhook {event_id} for org {org.id}")
                    return

                # Reset Usage
                from services.usage_service import UsageService

                usage_service = UsageService(self.db)
                await usage_service.reset_usage(org.id)

                org.last_webhook_id = event_id
                self.db.add(org)
                await self.db.commit()
                logger.info(f"Usage reset for org {org.id} due to subscription cycle")
