from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest

from models.auth import Organization
from services.stripe_service import StripeService


@pytest.mark.asyncio
async def test_create_checkout_session():
    # Mock DB
    mock_db = AsyncMock()

    # Mock Org
    org_id = uuid4()
    org = Organization(id=org_id, name="Test Org", tier="free")

    # Setup mock result for select
    mock_result = MagicMock()
    mock_result.first.return_value = org
    mock_db.exec.return_value = mock_result

    service = StripeService(mock_db)

    with (
        patch("stripe.checkout.Session.create") as mock_stripe_create,
        patch("services.stripe_service.settings") as mock_settings,
    ):
        mock_settings.STRIPE_PRICE_ID_PRO = "price_pro_123"
        mock_settings.FRONTEND_URL = "http://localhost:3000"
        mock_stripe_create.return_value = MagicMock(url="http://checkout.url")

        url = await service.create_checkout_session(str(org_id), plan_id="pro")

        assert url == "http://checkout.url"
        mock_stripe_create.assert_called_once()
        # Verify call args
        args, kwargs = mock_stripe_create.call_args
        assert kwargs["client_reference_id"] == str(org_id)
        assert kwargs["line_items"][0]["price"] == "price_pro_123"


@pytest.mark.asyncio
async def test_handle_webhook_checkout_completed():
    mock_db = AsyncMock()
    org_id = uuid4()
    org = Organization(id=org_id, name="Test Org", tier="free")

    mock_result = MagicMock()
    mock_result.first.return_value = org
    mock_db.exec.return_value = mock_result

    service = StripeService(mock_db)

    event = {
        "id": "evt_test_checkout",
        "type": "checkout.session.completed",
        "data": {"object": {"client_reference_id": str(org_id), "customer": "cus_123", "subscription": "sub_123"}},
    }

    await service.handle_webhook(event)

    # Verify DB update
    assert org.stripe_customer_id == "cus_123"
    assert org.stripe_subscription_id == "sub_123"
    assert org.tier == "pro"
    assert org.subscription_status == "active"

    mock_db.add.assert_called_with(org)
    mock_db.commit.assert_called_once()


@pytest.mark.asyncio
async def test_handle_webhook_subscription_deleted():
    mock_db = AsyncMock()
    org = Organization(id=uuid4(), name="Test Org", tier="pro", stripe_customer_id="cus_123")

    mock_result = MagicMock()
    mock_result.first.return_value = org
    mock_db.exec.return_value = mock_result

    service = StripeService(mock_db)

    event = {
        "id": "evt_test_sub_del",
        "type": "customer.subscription.deleted",
        "data": {"object": {"customer": "cus_123", "status": "canceled"}},
    }

    await service.handle_webhook(event)

    assert org.tier == "free"
    assert org.subscription_status == "canceled"

    mock_db.add.assert_called_with(org)
    mock_db.commit.assert_called_once()
