from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.embedding import EmbeddingService


@pytest.mark.asyncio
async def test_generate_embeddings_batching():
    # Setup
    with patch("services.embedding.AsyncOpenAI") as mock_openai:
        mock_client = AsyncMock()
        mock_openai.return_value = mock_client
        
        # Mock OpenAI response
        def mock_embeddings_create(input, model):
            mock_response = MagicMock()
            data_list = []
            for i, text in enumerate(input):
                m = MagicMock()
                # Deterministic embedding for testing
                m.embedding = [float(i), float(i+1)]
                data_list.append(m)
            mock_response.data = data_list
            return mock_response

        mock_client.embeddings.create.side_effect = mock_embeddings_create
        
        service = EmbeddingService()
        texts = ["hello", "world"]
        
        # Run
        embeddings = await service.generate_embeddings(texts)
        
        # Verify call count and content
        # "hello" -> [0.0, 1.0], "world" -> [1.0, 2.0]
        assert len(embeddings) == 2
        assert embeddings[0] == [0.0, 1.0]
        assert embeddings[1] == [1.0, 2.0]
        assert mock_client.embeddings.create.call_count == 1
        
        # Verify caching & deduplication: call again with same texts + something new
        # "hello" (cached), "something new" (new)
        embeddings2 = await service.generate_embeddings(["hello", "something new"])
        assert len(embeddings2) == 2
        assert embeddings2[0] == [0.0, 1.0] # from cache
        assert embeddings2[1] == [0.0, 1.0] # fetched index 0 of new call
        assert mock_client.embeddings.create.call_count == 2
        
        # Verify only unique/new texts sent to API
        args, kwargs = mock_client.embeddings.create.call_args
        assert kwargs["input"] == ["something new"]
