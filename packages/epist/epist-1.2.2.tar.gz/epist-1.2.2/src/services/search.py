import asyncio
import logging
import math
from functools import lru_cache
from uuid import UUID

import httpx
from sqlalchemy import text
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from core.config import settings
from db.session import engine
from models.transcript import TranscriptSegment
from services.embedding import EmbeddingService
from services.trace import trace_service

logger = logging.getLogger(__name__)

# Safe Import for Reranker (Pro Tier)
try:
    from sentence_transformers import CrossEncoder

    _HAS_SENTENCE_TRANSFORMERS = True
except ImportError:
    _HAS_SENTENCE_TRANSFORMERS = False
    logger.warning("sentence-transformers not installed. Reranking will be disabled.")


@lru_cache(maxsize=1)
def get_reranker(model_name: str | None = None):
    """Load the CrossEncoder model (Singleton) if available."""
    if not _HAS_SENTENCE_TRANSFORMERS:
        return None
    model = model_name or settings.DEFAULT_RERANK_MODEL
    logger.info(f"Loading CrossEncoder model {model} for Reranking...")
    return CrossEncoder(model, token=settings.HF_TOKEN)


class SearchResult:
    def __init__(self, segment_id: UUID, text: str, score: float, method: str):
        self.segment_id = segment_id
        self.text = text
        self.score = score
        self.method = method


class SearchService:
    def __init__(self):
        self.embedding_service = EmbeddingService()

    async def search(
        self,
        query: str,
        limit: int = 10,
        tier: str = "free",
        rrf_k: int | None = None,
        rerank_model: str | None = None,
        transcript_id: UUID | None = None,
    ) -> list[dict]:
        """
        Perform Hybrid Search (Vector + Keyword) with RRF Fusion.
        If tier="pro", applies Cross-Encoder Reranking.
        """

        def sigmoid(x: float) -> float:
            # Clip to avoid overflow/underflow if necessary, though exp is usually safe for reasonable logits
            return 1 / (1 + math.exp(-max(min(x, 20), -20)))

        # Determine effective parameters (Default vs. Override)
        effective_k = rrf_k if rrf_k is not None else settings.DEFAULT_RRF_K
        effective_rerank_model = rerank_model or settings.DEFAULT_RERANK_MODEL

        async with trace_service.span(
            "Hybrid Search",
            component="SearchService",
            inputs={
                "query": query,
                "limit": limit,
                "tier": tier,
                "rrf_k": effective_k,
                "rerank_model": effective_rerank_model,
                "transcript_id": str(transcript_id) if transcript_id else None,
            },
        ) as span:
            # 0. Check for Global Intent (Summary, Topics, etc.)
            is_global = any(word in query.lower() for word in ["summary", "summarize", "topics", "about", "overview"])

            async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

            if is_global and transcript_id:
                # For global queries with a specific transcript, we want a spread of segments
                async with trace_service.span("Global Distributed Search", component="SearchService") as global_span:
                    async with async_session() as session:
                        # Fetch segments spread across the transcript
                        stmt = select(TranscriptSegment).where(TranscriptSegment.transcript_id == transcript_id)
                        result_obj = await session.exec(stmt.order_by(TranscriptSegment.start))
                        all_segments = result_obj.all()

                        if len(all_segments) <= limit:
                            results = all_segments
                        else:
                            # Sample distributed segments
                            indices = [int(i * (len(all_segments) - 1) / (limit - 1)) for i in range(limit)]
                            results = [all_segments[i] for i in sorted(list(set(indices)))]

                        global_span.set_output({"count": len(results), "mode": "distributed"})
                        final_results = [
                            {
                                "id": s.id,
                                "text": s.text,
                                "start": s.start,
                                "end": s.end,
                                "score": 1.0,
                                "methods": ["global_dist"],
                            }
                            for s in results
                        ]
                        span.set_output(final_results)
                        return final_results

            # 1. Start Keyword Search and Embedding Generation in parallel
            async def run_keyword_search(q: str, limit: int):
                async with trace_service.span("Keyword Search", component="SearchService") as keyword_span:
                    async with async_session() as session:
                        stmt = select(TranscriptSegment).where(
                            text("content_vector @@ plainto_tsquery('english', :query)")
                        )
                        if transcript_id:
                            stmt = stmt.where(TranscriptSegment.transcript_id == transcript_id)

                        result_obj = await session.exec(stmt.params(query=q).limit(limit))
                        results = result_obj.all()
                        keyword_span.set_output({"count": len(results)})
                        return results

            async def run_embedding(q: str):
                async with trace_service.span(
                    "Generate Embedding", component="EmbeddingService", inputs={"text": q}
                ) as embed_span:
                    return await self.embedding_service.generate_embedding(q)

            # Parallel triggers
            search_limit = limit * 2 if tier == "pro" else limit

            # Use asyncio.gather to run tasks concurrently
            [query_embedding, keyword_results] = await asyncio.gather(
                run_embedding(query), run_keyword_search(query, search_limit)
            )

            async with async_session() as session:
                # 2. Vector Search (Cosine Similarity)
                async with trace_service.span("Vector Search", component="SearchService") as vector_span:
                    stmt = select(TranscriptSegment).order_by(
                        TranscriptSegment.embedding.cosine_distance(query_embedding)
                    )
                    if transcript_id:
                        stmt = stmt.where(TranscriptSegment.transcript_id == transcript_id)

                    vector_result_obj = await session.exec(stmt.limit(search_limit))
                    vector_results = vector_result_obj.all()
                    vector_span.set_output({"count": len(vector_results)})
                    logger.info(f"Vector search found {len(vector_results)} results")

                # 4. Reciprocal Rank Fusion (RRF)
                async with trace_service.span("RRF Fusion", component="SearchService") as rrf_span:
                    k = effective_k
                    scores = {}

                    # Process Vector Results
                    for rank, segment in enumerate(vector_results):
                        if segment.id not in scores:
                            scores[segment.id] = {"segment": segment, "score": 0.0, "methods": []}
                        scores[segment.id]["score"] += 1 / (k + rank + 1)
                        if "vector" not in scores[segment.id]["methods"]:
                            scores[segment.id]["methods"].append("vector")

                    # Process Keyword Results
                    for rank, segment in enumerate(keyword_results):
                        if segment.id not in scores:
                            scores[segment.id] = {"segment": segment, "score": 0.0, "methods": []}
                        scores[segment.id]["score"] += 1 / (k + rank + 1)
                        if "keyword" not in scores[segment.id]["methods"]:
                            scores[segment.id]["methods"].append("keyword")

                    # Sort by RRF Score DESC
                    sorted_results = sorted(scores.values(), key=lambda x: x["score"], reverse=True)

                    # Normalize RRF scores to [0, 1] range based on theoretical maximum
                    # Max possible score = (1/(k+1) * number of methods)
                    # We have 2 methods: Vector and Keyword
                    max_theoretical_rrf = 2 / (k + 1)
                    for item in sorted_results:
                        # Ensure we don't divide by zero (k is usually 60)
                        item["score"] = min(1.0, item["score"] / max_theoretical_rrf)

                    # Initial top candidates
                    candidates = sorted_results[:search_limit]  # Take top 20 for reranking

                # 5. Reranking (If Pro)
                if tier == "pro":
                    async with trace_service.span("Reranking", component="SearchService") as rerank_span:
                        rerank_span.set_metadata("provider", settings.RERANK_PROVIDER)

                        if settings.RERANK_PROVIDER == "api" and settings.FIREWORKS_API_KEY:
                            candidates = await self._rerank_fireworks(query, candidates)
                        elif _HAS_SENTENCE_TRANSFORMERS:
                            candidates = await self._rerank_local(query, candidates)

                        rerank_span.set_output({"count": len(candidates)})

                # Format Output (Final Limit)
                final_output = []
                for item in candidates[:limit]:
                    seg = item["segment"]
                    final_output.append(
                        {
                            "id": seg.id,
                            "text": seg.text,
                            "start": seg.start,
                            "end": seg.end,
                            "score": item["score"],
                            "methods": item["methods"],
                        }
                    )

                span.set_output(final_output)
                return final_output

    async def _rerank_local(self, query: str, candidates: list[dict]) -> list[dict]:
        """Perform local CPU-based reranking."""
        reranker = get_reranker()
        if not reranker:
            return candidates

        pairs = [[query, item["segment"].text] for item in candidates]
        if not pairs:
            return candidates

        # We need to run this in a threadpool to avoid blocking event loop
        rerank_scores = await asyncio.to_thread(reranker.predict, pairs)

        # Update scores using relative normalization
        raw_scores = [float(s) for s in rerank_scores]
        return self._apply_rerank_scores(candidates, raw_scores)

    async def _rerank_fireworks(self, query: str, candidates: list[dict]) -> list[dict]:
        """Perform API-based reranking via Fireworks AI."""
        if not candidates:
            return candidates

        url = "https://api.fireworks.ai/inference/v1/rerank"
        headers = {"Authorization": f"Bearer {settings.FIREWORKS_API_KEY}", "Content-Type": "application/json"}
        payload = {
            "model": settings.FIREWORKS_RERANK_MODEL,
            "query": query,
            "documents": [item["segment"].text for item in candidates],
            "top_n": len(candidates),
            "return_documents": False,
        }

        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.post(url, headers=headers, json=payload)
                response.raise_for_status()
                data = response.json()

                # Fireworks returns results in a list with 'index' and 'relevance_score'
                # We need to map them back to our candidates.
                # The 'results' are usually sorted by score already by the API.
                results = data.get("results", [])

                # Create a score map: index -> score
                score_map = {res["index"]: float(res["relevance_score"]) for res in results}

                # Reconstruct raw_scores in the original order of candidates
                raw_scores = [score_map.get(i, 0.0) for i in range(len(candidates))]

                return self._apply_rerank_scores(candidates, raw_scores)
        except Exception as e:
            logger.error(f"Fireworks reranking failed: {e}")
            # Fallback to local if API fails and we have the model
            if _HAS_SENTENCE_TRANSFORMERS:
                return await self._rerank_local(query, candidates)
            return candidates

    def _apply_rerank_scores(self, candidates: list[dict], raw_scores: list[float]) -> list[dict]:
        """Apply raw reranker scores to candidates with normalization."""
        if not raw_scores or len(raw_scores) != len(candidates):
            return candidates

        if len(raw_scores) > 1:
            max_l = max(raw_scores)
            min_l = min(raw_scores)
            range_l = max_l - min_l
            if range_l < 1e-6:
                for item in candidates:
                    item["score"] = 0.95
            else:
                for i, item in enumerate(candidates):
                    # Map top hitter to 98% and bottom one to 40% visually
                    norm = (raw_scores[i] - min_l) / range_l
                    item["score"] = 0.4 + (norm * 0.58)
        elif len(raw_scores) == 1:
            item = candidates[0]
            # Sigmoid for single result
            item["score"] = 1 / (1 + math.exp(-max(min(raw_scores[0], 20), -20)))

        for item in candidates:
            if "rerank" not in item["methods"]:
                item["methods"].append("rerank")

        # Sort by new score
        return sorted(candidates, key=lambda x: x["score"], reverse=True)
