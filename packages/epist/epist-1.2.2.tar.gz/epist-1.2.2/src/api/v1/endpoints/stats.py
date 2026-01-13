from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from db.session import get_session
from models.audio import AudioResource
from models.transcript import Transcript, TranscriptSegment

router = APIRouter()

from api.deps import get_api_key


@router.get("", dependencies=[Depends(get_api_key)])
async def get_stats(session: AsyncSession = Depends(get_session)):
    """
    Get system statistics: counts of audio files, transcripts, and segments.
    """
    audio_count = (await session.exec(select(func.count(AudioResource.id)))).one()
    transcript_count = (await session.exec(select(func.count(Transcript.id)))).one()
    segment_count = (await session.exec(select(func.count(TranscriptSegment.id)))).one()

    return {"audio_count": audio_count, "transcript_count": transcript_count, "segment_count": segment_count}
