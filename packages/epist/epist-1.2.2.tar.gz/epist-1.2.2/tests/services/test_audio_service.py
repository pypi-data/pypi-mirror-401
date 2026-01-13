from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest
from fastapi import HTTPException

from models.audio import AudioResource
from services.audio_service import AudioService


@pytest.mark.asyncio
async def test_delete_audio_resource_success():
    # Setup
    mock_db = AsyncMock()
    user_id = uuid4()
    audio_id = uuid4()

    # Mock existing audio
    audio = AudioResource(id=audio_id, user_id=user_id, source_url="gs://bucket/blob.mp3", title="test.mp3")

    # Mock DB result
    mock_result = MagicMock()
    mock_result.first.return_value = audio
    mock_db.exec.return_value = mock_result

    # Init Service
    service = AudioService(mock_db)

    # Mock StorageService
    with patch.object(service.storage_service, "delete_file") as mock_storage_delete:
        await service.delete_audio_resource(audio_id, user_id)

        # Verify GCS Delete called
        mock_storage_delete.assert_called_once_with("bucket", "blob.mp3")

        # Verify DB Delete called
        mock_db.delete.assert_called_once_with(audio)
        mock_db.commit.assert_called_once()


@pytest.mark.asyncio
async def test_delete_audio_resource_not_found():
    mock_db = AsyncMock()
    mock_result = MagicMock()
    mock_result.first.return_value = None
    mock_db.exec.return_value = mock_result

    service = AudioService(mock_db)

    with pytest.raises(HTTPException) as exc:
        await service.delete_audio_resource(uuid4(), uuid4())

    assert exc.value.status_code == 404


@pytest.mark.asyncio
async def test_delete_audio_resource_forbidden():
    mock_db = AsyncMock()
    user_id = uuid4()
    other_user_id = uuid4()
    audio = AudioResource(id=uuid4(), user_id=other_user_id, source_url="gs://b/f")

    mock_result = MagicMock()
    mock_result.first.return_value = audio
    mock_db.exec.return_value = mock_result

    service = AudioService(mock_db)

    with pytest.raises(HTTPException) as exc:
        await service.delete_audio_resource(audio.id, user_id)

    assert exc.value.status_code == 403
