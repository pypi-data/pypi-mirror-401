from unittest.mock import patch

import pytest
from httpx import AsyncClient
from sqlmodel.ext.asyncio.session import AsyncSession

from models.audio import AudioResource


@pytest.fixture
def mock_storage_service():
    with patch("api.v1.endpoints.audio.storage_service") as mock:
        yield mock


@pytest.fixture
def mock_queue_service():
    with patch("services.queue.QueueService") as mock:
        yield mock


@pytest.mark.asyncio
async def test_upload_audio_success(
    client: AsyncClient, session: AsyncSession, mock_storage_service, mock_queue_service
):
    # Mock GCS upload
    mock_storage_service.upload_file.return_value = "gs://epist-audio-raw/uploads/test.mp3"

    # Create a dummy audio file
    files = {"file": ("test.mp3", b"fake audio content", "audio/mpeg")}

    from src.core.config import settings

    response = await client.post("/api/v1/audio/upload", files=files, headers={"X-API-Key": settings.API_KEY})

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "test.mp3"
    assert data["source_url"] == "gs://epist-audio-raw/uploads/test.mp3"
    assert data["status"] == "pending"

    # Verify DB record
    from uuid import UUID

    db_record = await session.get(AudioResource, UUID(data["id"]))
    assert db_record is not None
    assert db_record.title == "test.mp3"


@pytest.mark.asyncio
async def test_upload_audio_invalid_type(client: AsyncClient):
    # Upload a text file instead of audio
    files = {"file": ("test.txt", b"text content", "text/plain")}

    from src.core.config import settings

    response = await client.post("/api/v1/audio/upload", files=files, headers={"X-API-Key": settings.API_KEY})

    assert response.status_code == 400
    assert "Invalid content type" in response.json()["detail"]
