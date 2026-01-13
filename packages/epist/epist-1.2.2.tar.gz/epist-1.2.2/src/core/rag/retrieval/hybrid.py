from functools import lru_cache

from langchain_community.retrievers import BM25Retriever
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from sentence_transformers import CrossEncoder
from src.core.rag.base import RetrievalConfig, RetrievalStrategy


@lru_cache(maxsize=1)
def get_reranker():
    """Load the CrossEncoder model (Singleton)."""
    return CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")


def reciprocal_rank_fusion(doc_lists: list[list[Document]], weights: list[float], k: int = 60) -> list[Document]:
    """
    Combine multiple document lists using Reciprocal Rank Fusion (RRF).

    Args:
        doc_lists: List of document lists from different retrievers
        weights: Weights for each retriever (should sum to 1.0)
        k: Constant for RRF formula (default 60)

    Returns:
        Combined and ranked list of documents
    """
    doc_scores: dict[str, float] = {}
    doc_map: dict[str, Document] = {}

    for doc_list, weight in zip(doc_lists, weights, strict=False):
        for rank, doc in enumerate(doc_list):
            # Use page_content as unique identifier
            doc_id = doc.page_content
            if doc_id not in doc_map:
                doc_map[doc_id] = doc
                doc_scores[doc_id] = 0.0
            # RRF formula: weight / (k + rank)
            doc_scores[doc_id] += weight / (k + rank + 1)

    # Sort by score descending
    sorted_docs = sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)
    return [doc_map[doc_id] for doc_id, _ in sorted_docs]


class HybridRetrievalStrategy(RetrievalStrategy):
    def __init__(self, config: RetrievalConfig):
        self.config = config
        self.embeddings = OpenAIEmbeddings()
        self.vectorstore: Chroma | None = None
        self.bm25_retriever: BM25Retriever | None = None

    def index(self, documents: list[Document], collection_name: str):
        # Create Vector Store
        self.vectorstore = Chroma.from_documents(documents, self.embeddings, collection_name=collection_name)

        # Create Sparse Retriever
        self.bm25_retriever = BM25Retriever.from_documents(documents)
        self.bm25_retriever.k = self.config.top_k

        if not self.vectorstore:
            raise ValueError("Vectorstore initialization failed")

    def retrieve(self, query: str, top_k: int = 5) -> list[Document]:
        if not self.vectorstore or not self.bm25_retriever:
            raise ValueError("Index not built. Call index() first.")

        # Get candidates from both retrievers
        bm25_docs = self.bm25_retriever.invoke(query)
        vector_docs = self.vectorstore.as_retriever(search_kwargs={"k": self.config.top_k}).invoke(query)

        # Combine using Reciprocal Rank Fusion
        candidates = reciprocal_rank_fusion([bm25_docs, vector_docs], self.config.hybrid_weights)

        if self.config.rerank:
            model = get_reranker()
            pairs = [[query, d.page_content] for d in candidates[: top_k * 2]]  # Get more for reranking
            scores = model.predict(pairs)
            scored = sorted(zip(candidates[: top_k * 2], scores, strict=False), key=lambda x: x[1], reverse=True)
            return [d for d, s in scored[:top_k]]

        return candidates[:top_k]
