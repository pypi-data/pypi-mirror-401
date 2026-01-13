from unittest.mock import patch

import pytest


@pytest.mark.asyncio
async def test_sync_feeds_endpoint_unauthorized(client):
    # Test without auth header
    response = await client.post("/api/v1/tasks/sync-feeds")
    assert response.status_code == 401
    assert "Missing Authorization header" in response.json()["detail"]


@pytest.mark.asyncio
async def test_sync_feeds_endpoint_invalid_token(client):
    # Test with invalid OIDC token (signature check fails)
    with patch("google.oauth2.id_token.verify_oauth2_token") as mock_verify:
        mock_verify.side_effect = ValueError("Invalid token")
        response = await client.post("/api/v1/tasks/sync-feeds", headers={"Authorization": "Bearer invalid_token"})
        assert response.status_code == 401
        assert "Invalid OIDC token" in response.json()["detail"]


@pytest.mark.asyncio
async def test_sync_feeds_endpoint_success(client):
    # Mock OIDC verification success
    with patch("google.oauth2.id_token.verify_oauth2_token") as mock_verify:
        mock_verify.return_value = {"iss": "https://accounts.google.com"}

        # Mock the service call
        with patch("services.connector.PodcastService.sync_all_feeds") as mock_sync:
            response = await client.post("/api/v1/tasks/sync-feeds", headers={"Authorization": "Bearer valid_token"})

            assert response.status_code == 200
            assert response.json()["status"] == "success"
            mock_sync.assert_called_once()
