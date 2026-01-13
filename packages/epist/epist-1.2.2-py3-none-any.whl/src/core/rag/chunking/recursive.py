from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.core.rag.base import ChunkingConfig, ChunkingStrategy


class RecursiveChunkingStrategy(ChunkingStrategy):
    def __init__(self, config: ChunkingConfig):
        self.config = config
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=config.chunk_size,
            chunk_overlap=config.chunk_overlap,
        )

    def chunk(self, text: str) -> list[Document]:
        if not text:
            return []
        # RecursiveCharacterTextSplitter handles text -> docs
        return self.splitter.create_documents([text])
