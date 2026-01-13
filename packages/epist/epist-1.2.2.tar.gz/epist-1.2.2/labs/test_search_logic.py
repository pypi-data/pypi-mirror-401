import asyncio
import sys
import unittest
from unittest.mock import MagicMock, patch, AsyncMock

# Add src to path
import os
# Set dummy env vars for Settings validation
os.environ["SECRET_KEY"] = "dummy_secret_key"
os.environ["API_KEY"] = "dummy_api_key"
os.environ["OPENAI_API_KEY"] = "dummy_openai"
os.environ["FIREWORKS_API_KEY"] = "dummy_fw"
sys.path.append(os.path.join(os.getcwd(), "src"))

class TestSearchServiceLogic(unittest.TestCase):
    
    @patch('services.search.CrossEncoder')
    @patch('services.search.AsyncSession') # Mock DB session
    @patch('services.search.async_sessionmaker')
    @patch('services.search.EmbeddingService')
    def test_pro_tier_triggers_rerank(self, MockEmbed, MockMaker, MockSession, MockCrossEncoder):
        # Setup Mocks
        from services.search import SearchService, _HAS_SENTENCE_TRANSFORMERS
        
        # Ensure imports worked (mocking the global if needed, but assuming installed or mocked)
        # Actually we need to force _HAS_SENTENCE_TRANSFORMERS = True for this test
        import services.search
        services.search._HAS_SENTENCE_TRANSFORMERS = True
        
        # Mock embedding response
        mock_embed_svc = MockEmbed.return_value
        mock_embed_svc.generate_embedding = AsyncMock(return_value=[0.1, 0.2, 0.3])
        
        # Mock Session and Results
        mock_session = AsyncMock()
        MockMaker.return_value = MagicMock(return_value=mock_session)
        
        # Mock DB Results (TranscriptSegments)
        mock_seg1 = MagicMock(id="uuid1", text="Segment 1", start=0, end=1)
        mock_seg2 = MagicMock(id="uuid2", text="Segment 2", start=1, end=2)
        
        # Mock exec().all()
        # vector search returns 2
        # keyword search returns 2
        mock_result = MagicMock()
        mock_result.all.return_value = [mock_seg1, mock_seg2]
        mock_session.__aenter__.return_value.exec.return_value = mock_result
        
        # Mock Reranker
        mock_reranker = MockCrossEncoder.return_value
        mock_reranker.predict.return_value = [0.99, 0.50] # Seg1 better than Seg2
        
        # Init Service
        service = SearchService()
        
        # Run Search with PRO tier
        results = asyncio.run(service.search("query", limit=2, tier="pro"))
        
        # Verify Reranker was called
        MockCrossEncoder.assert_called() # Should init the model
        mock_reranker.predict.assert_called()
        
        # Verify Results
        # Should have method "rerank"
        self.assertTrue("rerank" in results[0]["methods"])
        print("✅ Pro Tier Reranking Logic Verified")

if __name__ == "__main__":
    unittest.main()
