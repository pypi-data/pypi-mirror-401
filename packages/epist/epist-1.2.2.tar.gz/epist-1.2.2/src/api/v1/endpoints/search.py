from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession

from api.deps import get_current_user
from db.session import engine
from models.auth import Organization, User
from services.search import SearchService

router = APIRouter()
search_service = SearchService()


class SearchRequest(BaseModel):
    query: str
    limit: int = 10
    tier: str = "free"
    # Advanced Tuning
    rrf_k: int | None = None
    rerank_model: str | None = None


class SearchResponseItem(BaseModel):
    id: Any
    text: str
    start: float
    end: float
    score: float
    methods: list[str]


@router.post("", response_model=list[SearchResponseItem])
async def search(request: SearchRequest, fastapi_request: Request, current_user: User = Depends(get_current_user)):
    """
    Perform Hybrid Search (Vector + Keyword) on transcripts.
    """
    auth_method = getattr(fastapi_request.state, "auth_method", "session")

    # Enforce tier specifically for API calls to prevent bypass
    if auth_method == "api_key":
        async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
        async with async_session() as session:
            org = await session.get(Organization, current_user.organization_id)
            actual_tier = org.tier if org else "free"
            request.tier = actual_tier

    try:
        results = await search_service.search(
            request.query,
            request.limit,
            tier=request.tier,
            rrf_k=request.rrf_k,
            rerank_model=request.rerank_model,
        )
        return results
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Search failed: {e!s}",
        )
