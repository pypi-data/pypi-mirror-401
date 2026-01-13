# src/services/audio_service.py
import logging
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from models.audio import AudioResource
from services.storage import StorageService

logger = logging.getLogger(__name__)


class AudioService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.storage_service = StorageService()

    async def delete_audio_resource(self, audio_id: UUID, user_id: UUID) -> None:
        """
        Permanently delete an audio resource:
        1. Remove from GCS (if source_url is gs://)
        2. Remove from DB (Transcripts/Segments cascade via DB FK)
        """
        # 1. Fetch Resource
        stmt = select(AudioResource).where(AudioResource.id == audio_id)
        result = await self.session.exec(stmt)
        audio = result.first()

        if not audio:
            raise HTTPException(status_code=404, detail="Audio resource not found")

        # 2. Check Ownership
        if audio.user_id != user_id:
            raise HTTPException(status_code=403, detail="Not authorized to delete this resource")

        # 3. Delete from Storage
        if audio.source_url and audio.source_url.startswith("gs://"):
            try:
                # Parse gs://bucket/blob_name
                path_parts = audio.source_url.replace("gs://", "").split("/", 1)
                if len(path_parts) == 2:
                    bucket_name = path_parts[0]
                    blob_name = path_parts[1]
                    self.storage_service.delete_file(bucket_name, blob_name)
                else:
                    logger.warning(f"Invalid GCS URL format for deletion: {audio.source_url}")
            except Exception as e:
                logger.error(f"Failed to delete blob for {audio_id}: {e}")
                # We continue to delete DB record even if storage fails (orphan blob is better than zombie app data)
                # Or should we fail? Better to cleanup metadata so user sees it gone.

        # 4. Delete from DB
        await self.session.delete(audio)
        await self.session.commit()

        logger.info(f"Deleted audio resource {audio_id} and associated data.")
