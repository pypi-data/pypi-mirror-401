import pytest
from httpx import AsyncClient
from sqlmodel.ext.asyncio.session import AsyncSession
from src.core.config import settings


@pytest.mark.asyncio
async def test_api_key_lifecycle(client: AsyncClient, session: AsyncSession):
    # Create a dummy user for Dev Key access
    from models.auth import Organization, User

    org = Organization(name="Test Org")
    session.add(org)
    await session.commit()
    await session.refresh(org)

    print("DEBUG: Running test_api_key_lifecycle with auth_flow_test@example.com")
    user = User(
        email="auth_flow_test@example.com", full_name="Test User", organization_id=org.id, firebase_uid="test_uid_flow"
    )
    session.add(user)
    await session.commit()

    # 1. Create API Key using Dev Key
    response = await client.post(
        "/api/v1/auth/api-keys", params={"name": "Test Key"}, headers={"X-API-Key": settings.API_KEY}
    )
    assert response.status_code == 201
    data = response.json()
    new_key = data["key"]
    key_id = data["id"]
    assert new_key.startswith("sk_live_")

    # 2. Use new API Key to access protected endpoint
    response = await client.get("/api/v1/stats", headers={"X-API-Key": new_key})
    assert response.status_code == 200

    # 3. Revoke API Key
    response = await client.delete(f"/api/v1/auth/api-keys/{key_id}", headers={"X-API-Key": settings.API_KEY})
    assert response.status_code == 204

    # 4. Try to use revoked key
    session.expire_all()
    response = await client.get("/api/v1/stats", headers={"X-API-Key": new_key})
    assert response.status_code == 401
