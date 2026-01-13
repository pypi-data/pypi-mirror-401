import logging
import uuid

from .transcription import TranscriptionService

logger = logging.getLogger(__name__)


class IngestionService:
    def __init__(self, transcription_service: TranscriptionService):
        self.transcription_service = transcription_service

    async def ingest_url(self, url: str, title: str) -> str:
        """
        Ingests an audio file: Transcribes it and stores the result.
        Returns the Job ID.
        """
        job_id = str(uuid.uuid4())
        logger.info(f"Starting ingestion job {job_id} for {url}")

        # In a real async system, we would push this to a queue (ArQ/Celery)
        # For this MVP, we'll just log that we would do it.

        # Simulate triggering transcription
        # transcript = await self.transcription_service.transcribe_audio(url)
        # await self.save_transcript(job_id, transcript)

        return job_id

    async def get_status(self, job_id: str) -> str:
        return "PROCESSING"
