from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest


@pytest.mark.asyncio
async def test_webhook_delivery_on_completion():
    # Mock models
    audio_id = uuid4()
    webhook_url = "https://example.com/webhook"
    
    mock_audio = MagicMock()
    mock_audio.id = audio_id
    mock_audio.webhook_url = webhook_url
    mock_audio.status = "processing"
    mock_audio.storage_gcs_uri = "gs://bucket/test.mp3"

    # Mock WebhookDispatcher
    with patch("services.webhook_dispatcher.WebhookDispatcher.deliver_to_url", new_callable=AsyncMock) as mock_deliver:
        # We need to mock the session inside TranscriptionService._process_audio_impl
        mock_session = AsyncMock()
        mock_session.get.return_value = mock_audio
        
        # Mock the async_sessionmaker context manager
        mock_session_cm = MagicMock()
        mock_session_cm.__aenter__.return_value = mock_session
        mock_session_factory = MagicMock(return_value=mock_session_cm)

        from services.transcription import TranscriptionService
        service = TranscriptionService()
        
        mock_response_data = {
            "text": "Translated text",
            "language": "en",
            "duration": 10.0,
            "segments": []
        }
        
        # Patch everything needed to avoid real DB and API calls
        with patch("services.transcription.async_sessionmaker", return_value=mock_session_factory):
            with patch.object(service.client, "post", new_callable=AsyncMock, return_value=mock_response_data):
                with patch("services.storage.StorageService.generate_signed_url", new_callable=AsyncMock, return_value="https://signed-url"):
                    with patch("services.embedding.EmbeddingService.generate_embeddings", new_callable=AsyncMock, return_value=[[0.1]*1536]):
                        # Run transcription
                        await service._process_audio_impl(audio_id, "gs://bucket/test.mp3")

        # Verify webhook was called
        mock_deliver.assert_called_once()
        args, kwargs = mock_deliver.call_args
        assert kwargs["url"] == webhook_url
        assert kwargs["event_type"] == "audio.completed"
        assert kwargs["payload"]["status"] == "completed"
        assert kwargs["payload"]["transcript"] == "Translated text"
        
        # Verify status update in DB
        assert mock_audio.status == "completed"
        assert mock_session.commit.called
