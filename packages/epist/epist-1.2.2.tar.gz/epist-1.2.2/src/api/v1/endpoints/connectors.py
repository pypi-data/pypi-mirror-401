from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession

from api.deps import get_current_user_org_id
from db.session import get_session
from models.connector import PodcastFeed
from services.connector import PodcastService
from services.transcription import TranscriptionService

router = APIRouter()


# Dependency for Service
def get_connector_service():
    # In a real app we'd use DI container or properly initialized service
    # For now, we instantiate on fly or use a singleton
    # We need TranscriptionService too.. for now mock or simple init
    return PodcastService(transcription_service=TranscriptionService())


@router.post("/feeds", response_model=PodcastFeed)
async def add_feed(
    url: str,
    name: str,
    refresh_interval_minutes: int | None = None,
    org_id: UUID = Depends(get_current_user_org_id),
    session: AsyncSession = Depends(get_session),
    service: PodcastService = Depends(get_connector_service),
):
    try:
        return await service.add_feed(session, url, org_id, name, refresh_interval_minutes=refresh_interval_minutes)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/feeds", response_model=list[PodcastFeed])
async def list_feeds(org_id: UUID = Depends(get_current_user_org_id), session: AsyncSession = Depends(get_session)):
    from sqlmodel import select

    feeds = await session.exec(select(PodcastFeed).where(PodcastFeed.organization_id == org_id))
    return feeds.all()


@router.post("/feeds/{feed_id}/sync")
async def sync_feed(
    feed_id: UUID,
    session: AsyncSession = Depends(get_session),
    service: PodcastService = Depends(get_connector_service),
):
    await service.sync_feed(session, feed_id)
    return {"status": "sync_started"}
