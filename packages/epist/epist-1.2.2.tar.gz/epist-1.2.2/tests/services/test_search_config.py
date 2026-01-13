from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from core.config import settings
from services.search import SearchService


@pytest.mark.asyncio
async def test_search_uses_defaults():
    """Verify that search uses default settings when no overrides are provided."""

    # Mock dependencies
    with (
        patch("services.search.EmbeddingService") as mock_embed_cls,
        patch("services.search.trace_service") as mock_trace,
        patch("services.search.async_sessionmaker") as mock_session_maker,
    ):
        # Setup mocks
        mock_instance = mock_embed_cls.return_value
        mock_instance.generate_embedding = AsyncMock(return_value=[0.1] * 1536)

        mock_trace.span.return_value.__aenter__.return_value = AsyncMock()

        # Proper Mocking for SQLModel session.exec
        mock_result = MagicMock()
        mock_result.all.return_value = []
        # sessionmaker() -> session_factory -> session_factory() -> context_manager -> session
        mock_session_maker.return_value.return_value.__aenter__.return_value.exec = AsyncMock(return_value=mock_result)

        service = SearchService()

        # Test Default
        with patch.object(settings, "DEFAULT_RRF_K", 60):
            # We intercept the span call to check inputs
            mock_span = mock_trace.span
            await service.search("query")

            # Check arguments passed to top-level span (first call)
            first_call_args = mock_span.call_args_list[0]
            # args, kwargs
            call_kwargs = first_call_args.kwargs
            assert call_kwargs["inputs"]["rrf_k"] == 60
            assert call_kwargs["inputs"]["rerank_model"] == settings.DEFAULT_RERANK_MODEL


@pytest.mark.asyncio
async def test_search_uses_overrides():
    """Verify that search uses provided overrides."""

    # Mock dependencies
    with (
        patch("services.search.EmbeddingService") as mock_embed_cls,
        patch("services.search.trace_service") as mock_trace,
        patch("services.search.async_sessionmaker") as mock_session_maker,
    ):
        # Setup mocks
        mock_instance = mock_embed_cls.return_value
        mock_instance.generate_embedding = AsyncMock(return_value=[0.1] * 1536)

        mock_trace.span.return_value.__aenter__.return_value = AsyncMock()

        mock_result = MagicMock()
        mock_result.all.return_value = []
        mock_session_maker.return_value.return_value.__aenter__.return_value.exec = AsyncMock(return_value=mock_result)

        service = SearchService()

        # Test Override
        await service.search("query", rrf_k=10, rerank_model="my-custom-model")

        # Check arguments passed to top-level span (first call)
        first_call_args = mock_trace.span.call_args_list[0]
        call_kwargs = first_call_args.kwargs
        assert call_kwargs["inputs"]["rrf_k"] == 10
        assert call_kwargs["inputs"]["rerank_model"] == "my-custom-model"
