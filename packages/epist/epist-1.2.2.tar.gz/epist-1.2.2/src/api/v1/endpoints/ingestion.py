import logging
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlmodel.ext.asyncio.session import AsyncSession

from api.deps import get_current_user, get_current_user_org_id
from core.entitlements import EntitlementsService
from db.session import get_session
from models.auth import User
from services.connector import PodcastService
from services.transcription import TranscriptionService

router = APIRouter()
logger = logging.getLogger(__name__)


class RssIngestionRequest(BaseModel):
    url: str
    name: str | None = None
    refresh_interval_minutes: int | None = None
    max_episodes: int | None = None
    start_date: str | None = None  # Accept ISO string
    include_keywords: str | None = None
    exclude_keywords: str | None = None


def get_podcast_service():
    return PodcastService(transcription_service=TranscriptionService())


@router.post("/rss", status_code=status.HTTP_201_CREATED)
async def ingest_rss(
    request: RssIngestionRequest,
    session: Annotated[AsyncSession, Depends(get_session)],
    current_user: Annotated[User, Depends(get_current_user)],
    org_id: Annotated[UUID, Depends(get_current_user_org_id)],
    service: PodcastService = Depends(get_podcast_service),
):
    """
    Ingest a podcast RSS feed.
    This will discover all episodes and trigger transcription for new ones.
    Requires 'rss_ingestion' entitlement.
    """
    # Check Entitlements
    entitlements = EntitlementsService(session)
    # Fetch org to check features
    from models.auth import Organization

    org = await session.get(Organization, org_id)
    if not org or not entitlements.check_access(org, "rss_ingestion"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Your tier does not support RSS ingestion.")

    try:
        logger.info(f"User {current_user.email} ingesting RSS: {request.url}")
        from datetime import datetime

        start_date_obj = None
        if request.start_date:
            try:
                start_date_obj = datetime.fromisoformat(request.start_date)
            except ValueError:
                raise HTTPException(status_code=400, detail="Invalid start_date format. Use ISO format.")

        feed = await service.add_feed(
            session=session,
            url=request.url,
            org_id=org_id,
            name=request.name or "New Podcast Feed",
            refresh_interval_minutes=request.refresh_interval_minutes,
            max_episodes=request.max_episodes,
            start_date=start_date_obj,
            include_keywords=request.include_keywords,
            exclude_keywords=request.exclude_keywords,
        )
        return {
            "id": str(feed.id),
            "name": feed.name,
            "status": "ingestion_started",
            "message": "Feed added and initial sync triggered.",
        }
    except ValueError as e:
        logger.warning(f"Validation failed for RSS ingestion: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(f"Failed to ingest RSS {request.url}: {e}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to process RSS feed.")
