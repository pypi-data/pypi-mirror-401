from langchain_core.documents import Document
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai import OpenAIEmbeddings
from src.core.rag.base import ChunkingConfig, ChunkingStrategy


class SemanticChunkingStrategy(ChunkingStrategy):
    def __init__(self, config: ChunkingConfig):
        self.config = config
        # TODO: Allow passing embedding model from outside
        self.embeddings = OpenAIEmbeddings()
        self.splitter = SemanticChunker(
            self.embeddings,
            breakpoint_threshold_type=config.threshold_type,
            breakpoint_threshold_amount=config.threshold_amount,
        )

    def chunk(self, text: str) -> list[Document]:
        if not text:
            return []
        # SemanticChunker handles text -> docs
        return self.splitter.create_documents([text])
