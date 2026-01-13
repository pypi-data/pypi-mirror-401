import pytest
from httpx import AsyncClient
from sqlmodel import Session

from models.webhook import WebhookEndpoint


@pytest.mark.asyncio
async def test_create_webhook(client: AsyncClient, normal_user_token_headers: dict, session: Session):
    response = await client.post(
        "/api/v1/integrations/",
        headers=normal_user_token_headers,
        json={"url": "https://example.com/webhook", "events": ["transcription.completed"]},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["url"] == "https://example.com/webhook"
    assert "secret" in data
    assert data["secret"].startswith("whsec_")

    # Verify in DB
    assert session.get(WebhookEndpoint, data["id"]) is not None


@pytest.mark.asyncio
async def test_list_webhooks(client: AsyncClient, normal_user_token_headers: dict, session: Session):
    # Create one first
    response_create = await client.post(
        "/api/v1/integrations/",
        headers=normal_user_token_headers,
        json={"url": "https://example.com/webhook2", "events": ["transcription.failed"]},
    )
    assert response_create.status_code == 200

    # List
    response = await client.get("/api/v1/integrations/", headers=normal_user_token_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1

    # Ensure secret is NOT in list
    for webhook in data:
        assert "secret" not in webhook


@pytest.mark.asyncio
async def test_delete_webhook(client: AsyncClient, normal_user_token_headers: dict, session: Session):
    # Create
    response_create = await client.post(
        "/api/v1/integrations/",
        headers=normal_user_token_headers,
        json={"url": "https://example.com/webhook3", "events": ["all"]},
    )
    webhook_id = response_create.json()["id"]

    # Delete
    response = await client.delete(f"/api/v1/integrations/{webhook_id}", headers=normal_user_token_headers)
    assert response.status_code == 200

    # Verify gone
    response_list = await client.get("/api/v1/integrations/", headers=normal_user_token_headers)
    ids = [w["id"] for w in response_list.json()]
    assert webhook_id not in ids
