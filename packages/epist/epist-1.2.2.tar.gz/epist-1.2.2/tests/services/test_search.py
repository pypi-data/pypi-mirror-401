from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest
from sqlmodel.ext.asyncio.session import AsyncSession

from models.transcript import TranscriptSegment
from services.search import SearchService


@pytest.fixture
def mock_embedding_service():
    with patch("services.search.EmbeddingService") as mock:
        service_instance = AsyncMock()
        mock.return_value = service_instance
        yield service_instance


@pytest.mark.asyncio
async def test_search_hybrid(session: AsyncSession, mock_embedding_service):
    from models.audio import AudioResource
    from models.transcript import Transcript

    # Setup Data
    # Create AudioResource
    audio = AudioResource(title="Test Audio", source_url="http://test.com/audio.mp3")
    session.add(audio)
    await session.commit()
    await session.refresh(audio)

    # Create Transcript
    transcript = Transcript(audio_resource_id=audio.id, text="Full transcript text")
    session.add(transcript)
    await session.commit()
    await session.refresh(transcript)

    seg1 = TranscriptSegment(
        id=uuid4(), transcript_id=transcript.id, start=0, end=1, text="Target concept", embedding=[0.1] * 1536
    )
    seg2 = TranscriptSegment(
        id=uuid4(), transcript_id=transcript.id, start=1, end=2, text="Random text", embedding=[0.9] * 1536
    )
    session.add(seg1)
    session.add(seg2)
    await session.commit()

    # Mock Embedding Generation
    mock_embedding_service.generate_embedding.return_value = [0.1] * 1536

    # Mock DB Execution for Vector and Keyword Search
    # Since we can't easily mock pgvector/tsvector in sqlite memory without extensions,
    # we will mock the session.exec return values.

    # We need to patch the sessionmaker in SearchService again
    async_cm = AsyncMock()
    async_cm.__aenter__.return_value = session
    async_cm.__aexit__.return_value = None

    mock_session_factory = MagicMock()
    mock_session_factory.return_value = async_cm

    # We also need to mock the session.exec calls inside the service
    # This is tricky because there are two calls.
    # Let's mock the `session.exec` method on our session object?
    # But `session` is a real AsyncSession (sqlite). It won't support vector ops.

    # Strategy: Mock the entire session context manager used in the service
    # and make it return a MockSession that returns our pre-defined lists.

    mock_session = AsyncMock()
    mock_session.exec.side_effect = [
        MagicMock(all=lambda: [seg1]),  # Vector result
        MagicMock(all=lambda: [seg1]),  # Keyword result
    ]

    async_cm_mock = AsyncMock()
    async_cm_mock.__aenter__.return_value = mock_session
    async_cm_mock.__aexit__.return_value = None

    mock_factory = MagicMock(return_value=async_cm_mock)

    with patch("services.search.async_sessionmaker", return_value=mock_factory):
        service = SearchService()
        service.embedding_service = mock_embedding_service

        results = await service.search("query")

        assert len(results) == 1
        assert results[0]["id"] == seg1.id
        assert "vector" in results[0]["methods"]
        assert "keyword" in results[0]["methods"]
