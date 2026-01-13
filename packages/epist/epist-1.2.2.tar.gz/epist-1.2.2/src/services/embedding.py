import logging

from openai import AsyncOpenAI

from core.config import settings

logger = logging.getLogger(__name__)


class EmbeddingService:
    def __init__(self):
        self.client = AsyncOpenAI(
            api_key=settings.OPENAI_API_KEY,
        )
        self.model = "text-embedding-3-small"
        self._cache = {}

    async def generate_embedding(self, text: str) -> list[float]:
        """
        Generate vector embedding for a given text with in-memory caching.
        """
        embeddings = await self.generate_embeddings([text])
        return embeddings[0]

    async def generate_embeddings(self, texts: list[str]) -> list[list[float]]:
        """
        Generate vector embeddings for a list of texts with in-memory caching.
        """
        if not texts:
            return []

        # Clean and filter unique texts for API call
        cleaned_texts = [t.replace("\n", " ") for t in texts]
        results: list[list[float] | None] = [None] * len(cleaned_texts)
        to_fetch = []

        for i, text in enumerate(cleaned_texts):
            if text in self._cache:
                results[i] = self._cache[text]
            elif text not in to_fetch:
                to_fetch.append(text)
                
        if to_fetch:
            try:
                # OpenAI supports batching by passing a list to 'input'
                response = await self.client.embeddings.create(input=to_fetch, model=self.model)
                
                # Create a map for the new embeddings
                new_embeddings = {
                    text: data.embedding 
                    for text, data in zip(to_fetch, response.data, strict=True)
                }
                
                # Update cache
                self._cache.update(new_embeddings)

                # Fill in the results for all indices
                for i, text in enumerate(cleaned_texts):
                    if results[i] is None:
                        results[i] = new_embeddings[text]

            except Exception as e:
                logger.error(f"Failed to generate batched embeddings: {e}")
                raise e

        # Ensure all elements are filled (should be guaranteed by logic above)
        final_results: list[list[float]] = []
        for res in results:
            if res is None:
                # Should logically never happen if loop logic is correct
                # But for type safety and resilience:
                logger.error("Embedding result unexpectedly None, returning empty vector")
                final_results.append([0.0] * 1536)
            else:
                final_results.append(res)

        return final_results
