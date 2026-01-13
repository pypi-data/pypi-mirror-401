from src.core.rag.base import ChunkingConfig, RetrievalConfig
from src.core.rag.chunking.semantic import SemanticChunkingStrategy
from src.core.rag.retrieval.hybrid import HybridRetrievalStrategy


class RAGPipeline:
    def __init__(self, chunking_config: ChunkingConfig, retrieval_config: RetrievalConfig):
        self.chunking_config = chunking_config
        self.retrieval_config = retrieval_config

        # Factory Logic for Chunking
        if chunking_config.strategy_name == "semantic":
            self.chunker = SemanticChunkingStrategy(chunking_config)
        else:
            # Fallback to semantic for now, or implement Fixed/Recursive
            self.chunker = SemanticChunkingStrategy(chunking_config)

        # Factory Logic for Retrieval
        if retrieval_config.strategy_name == "hybrid":
            self.retriever = HybridRetrievalStrategy(retrieval_config)
        else:
            # Fallback
            self.retriever = HybridRetrievalStrategy(retrieval_config)

    def ingest(self, text: str, collection_name: str = "default"):
        """Chunk and Index text."""
        docs = self.chunker.chunk(text)
        if docs:
            self.retriever.index(docs, collection_name)
        return len(docs)

    def query(self, query: str, top_k: int = 5):
        """Search the index."""
        return self.retriever.retrieve(query, top_k)


def get_pipeline_for_tier(tier: str) -> RAGPipeline:
    """Factory to get the standard pipeline for a customer tier."""
    if tier.lower() == "free":
        # Standard: Semantic Chunking (P80) + Hybrid (50/50), No Rerank
        # Fast, Good enough.
        c_conf = ChunkingConfig(strategy_name="semantic", threshold_amount=80.0)
        r_conf = RetrievalConfig(strategy_name="hybrid", hybrid_weights=[0.5, 0.5], rerank=False)
        return RAGPipeline(c_conf, r_conf)

    elif tier.lower() == "pro":
        # Pro: Semantic (P80) + Hybrid (50/50) + Rerank (CrossEncoder)
        # Higher latency, better precision.
        c_conf = ChunkingConfig(strategy_name="semantic", threshold_amount=80.0)
        r_conf = RetrievalConfig(strategy_name="hybrid", hybrid_weights=[0.5, 0.5], rerank=True)
        return RAGPipeline(c_conf, r_conf)

    elif tier.lower() == "enterprise":
        # Enterprise: Custom? HyDE? For now, same as Pro but maybe aggressive chunking P90?
        # Let's say HyDE placeholder if we had it, or just Pro with Tuning options.
        # Let's use Pro config but enabled for high precision.
        c_conf = ChunkingConfig(strategy_name="semantic", threshold_amount=90.0)  # More granular
        r_conf = RetrievalConfig(strategy_name="hybrid", hybrid_weights=[0.4, 0.6], rerank=True)
        return RAGPipeline(c_conf, r_conf)

    else:
        raise ValueError(f"Unknown tier: {tier}")
