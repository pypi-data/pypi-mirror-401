from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest
from sqlmodel.ext.asyncio.session import AsyncSession

from models.audio import AudioResource
from models.transcript import Transcript
from services.transcription import TranscriptionService


@pytest.fixture
def mock_openai_client():
    with patch("services.transcription.AsyncOpenAI") as mock:
        client_instance = AsyncMock()
        mock.return_value = client_instance
        yield client_instance


@pytest.fixture
def mock_storage_service():
    with patch("services.transcription.StorageService") as mock:
        yield mock


@pytest.fixture
def mock_embedding_service():
    with patch("services.transcription.EmbeddingService") as mock:
        service_instance = AsyncMock()
        mock.return_value = service_instance
        # Mock generate_embeddings to return list of lists
        service_instance.generate_embeddings.return_value = [[0.1] * 1536]
        yield service_instance


@pytest.mark.asyncio
async def test_process_audio_success(
    session: AsyncSession, mock_openai_client, mock_storage_service, mock_embedding_service
):
    # Setup
    audio_id = uuid4()
    audio = AudioResource(id=audio_id, title="test.mp3", source_url="gs://bucket/test.mp3", status="pending")
    session.add(audio)
    await session.commit()

    # Mock Fireworks Response
    mock_response = MagicMock()
    mock_response.text = "Hello world"
    mock_response.language = "en"
    from types import SimpleNamespace

    mock_response.segments = [SimpleNamespace(start=0.0, end=1.0, text="Hello world")]
    # Mock both the SDK method (fallback) and the raw post method (signed URL optimization)
    mock_openai_client.audio.transcriptions.create.return_value = mock_response
    mock_openai_client.post.return_value = mock_response

    # Mock GCS Signed URL generation
    mock_storage_service.return_value.generate_signed_url.return_value = "https://signed-url.com"

    # Run Service
    service = TranscriptionService()
    # Inject mocked client
    service.client = mock_openai_client

    # We need to patch the sessionmaker in the service to use our test session
    # Or better, we can just rely on the fact that the service creates a NEW session.
    # But for testing, we want it to use our in-memory DB.
    # The service uses `sessionmaker(engine, ...)`
    # We should patch `services.transcription.sessionmaker` to return a mock that yields our session.

    # Actually, simpler approach: The service uses `engine`.
    # Our `conftest.py` patches `create_async_engine`? No, it creates a fixture.
    # The service imports `engine` from `db.session`.
    # We should patch `services.transcription.engine` to be our test engine?
    # Or patch `services.transcription.sessionmaker`?

    # Let's patch sessionmaker to return an async context manager that yields our session
    async_cm = AsyncMock()
    async_cm.__aenter__.return_value = session
    async_cm.__aexit__.return_value = None

    mock_session_factory = MagicMock()
    mock_session_factory.return_value = async_cm

    with patch("services.transcription.async_sessionmaker", return_value=mock_session_factory):
        await service.process_audio(audio_id, "gs://bucket/test.mp3")

    # Verify
    await session.refresh(audio)
    assert audio.status == "completed"

    # Check Transcript
    from sqlmodel import select

    result = await session.exec(select(Transcript).where(Transcript.audio_resource_id == audio_id))
    transcript = result.first()
    assert transcript is not None
    assert transcript.text == "Hello world"
