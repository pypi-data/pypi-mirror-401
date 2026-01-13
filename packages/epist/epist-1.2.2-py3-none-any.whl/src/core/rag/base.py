from abc import ABC, abstractmethod
from typing import Literal

from langchain_core.documents import Document
from pydantic import BaseModel


class ChunkingConfig(BaseModel):
    strategy_name: str = "semantic"  # semantic, recursive, fixed
    chunk_size: int = 1000
    chunk_overlap: int = 200
    threshold_type: Literal["percentile", "standard_deviation", "interquartile", "gradient"] = "percentile"
    threshold_amount: float = 95.0  # for semantic


class RetrievalConfig(BaseModel):
    strategy_name: str = "hybrid"  # vector, hybrid, hyde
    top_k: int = 5
    hybrid_weights: list[float] = [0.5, 0.5]  # Dense, Sparse
    hyde_prompt: str | None = None
    rerank: bool = False


class ChunkingStrategy(ABC):
    @abstractmethod
    def chunk(self, text: str) -> list[Document]:
        """Split text into LangChain Documents."""
        pass


class RetrievalStrategy(ABC):
    @abstractmethod
    def index(self, documents: list[Document], collection_name: str):
        """Index documents."""
        pass

    @abstractmethod
    def retrieve(self, query: str, top_k: int = 5) -> list[Document]:
        """Retrieve relevant documents."""
        pass
