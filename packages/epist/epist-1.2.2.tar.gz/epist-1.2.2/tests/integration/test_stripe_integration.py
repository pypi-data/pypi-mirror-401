from unittest.mock import MagicMock, patch

import pytest
from sqlmodel import select

from models.auth import Organization, User
from services.stripe_service import StripeService

# Removed global TestClient import/instantiation


@pytest.mark.asyncio
async def test_stripe_subscription_flow(client, session, normal_user_token_headers, user: User):
    """
    Test the full subscription flow:
    1. Create Checkout Session (mocked)
    2. Simulate Webhook (Checkout Completed) -> Access Upgraded
    3. Check Entitlements (should allow Pro limits)
    4. Simulate Webhook (Subscription Deleted) -> Access Downgraded
    """
    # 0. Initial State: Free Tier
    # Ensure user/org is loaded
    await session.refresh(user, ["organization"])
    # If organization is None (failed refresh/load), fetch it manually
    if not user.organization:
        stmt = select(Organization).where(Organization.id == user.organization_id)
        res = await session.exec(stmt)
        user.organization = res.first()

    assert user.organization.tier == "free"

    # 1. Create Checkout Session
    with (
        patch("stripe.checkout.Session.create") as mock_checkout,
        patch("core.config.settings.STRIPE_PRICE_ID_PRO", "price_fake_pro"),
    ):
        mock_checkout.return_value = MagicMock(url="https://checkout.stripe.com/test")

        response = await client.post(
            "/api/v1/billing/checkout", headers=normal_user_token_headers, params={"plan_id": "pro"}
        )
        assert response.status_code == 200
        assert response.json()["url"] == "https://checkout.stripe.com/test"

    # 2. Simulate Webhook: checkout.session.completed
    # We call the service method directly to avoid signature complexity testing here.
    stripe_service = StripeService(session)

    mock_event = {
        "id": "evt_test_checkout_int",
        "type": "checkout.session.completed",
        "data": {
            "object": {
                "client_reference_id": str(user.organization_id),
                "customer": "cus_test123",
                "subscription": "sub_test123",
            }
        },
    }
    await stripe_service.handle_webhook(mock_event)

    from uuid import UUID

    org_id = UUID(str(user.organization_id))

    # Reload User/Org from DB
    session.expire_all()
    stmt = select(Organization).where(Organization.id == org_id)
    result = await session.exec(stmt)
    org = result.first()

    assert org.tier == "pro"
    assert org.stripe_customer_id == "cus_test123"
    assert org.stripe_subscription_id == "sub_test123"
    assert org.subscription_status == "active"

    # 3. Check Entitlements (Pro Limit)
    from core.entitlements import EntitlementsService

    entitlements = EntitlementsService(session)

    # Should not raise exception
    await entitlements.check_transcription_limit(org.id, new_duration_seconds=100)

    # 4. Simulate Webhook: customer.subscription.deleted
    mock_event_del = {
        "id": "evt_test_sub_del_int",
        "type": "customer.subscription.deleted",
        "data": {"object": {"customer": "cus_test123", "status": "canceled"}},
    }
    await stripe_service.handle_webhook(mock_event_del)

    session.expire_all()
    stmt = select(Organization).where(Organization.id == org_id)
    result = await session.exec(stmt)
    org = result.first()

    assert org.tier == "free"
    assert org.subscription_status == "canceled"
    assert org.stripe_subscription_id is None
