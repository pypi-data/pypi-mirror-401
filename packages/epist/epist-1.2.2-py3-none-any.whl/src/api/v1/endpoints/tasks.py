import uuid

from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import BaseModel
from sqlmodel.ext.asyncio.session import AsyncSession

from api.deps import get_session
from services.transcription import TranscriptionService

router = APIRouter()
transcription_service = TranscriptionService()


class ProcessAudioTask(BaseModel):
    audio_id: uuid.UUID
    audio_url: str
    preset: str = "general"
    chunking_config: dict | None = None


@router.post("/process-audio", status_code=status.HTTP_200_OK)
async def process_audio_task(
    task_payload: ProcessAudioTask,
    request: Request,
    session: AsyncSession = Depends(get_session),
):
    """
    Handler for Cloud Tasks to process audio.
    Verifies OIDC token to ensure request is authorized.
    """
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing Authorization header",
        )

    token = auth_header.split(" ")[1]

    try:
        # Verify the token
        # Note: We skip audience check for now or set it to the service URL if known.
        # Cloud Tasks sets audience to the handler URL by default.
        # For strict verification, we should check audience.
        from google.auth.transport import requests
        from google.oauth2 import id_token

        # We accept any audience for now to avoid hardcoding the URL,
        # but in production we should verify it matches our service URL.
        # Or we can just verify the signature and issuer.
        id_info = id_token.verify_oauth2_token(token, requests.Request())

        # Verify issuer
        if id_info["iss"] != "https://accounts.google.com":
            raise ValueError("Wrong issuer.")

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid OIDC token: {e!s}",
        )

    trace_header = request.headers.get("X-Cloud-Trace-Context")
    trace_id = trace_header.split("/")[0] if trace_header else None

    # Guardrail: Check retry count
    retry_count = int(request.headers.get("X-CloudTasks-TaskRetryCount", 0))
    max_retries = 20  # Increased from 3 to 20 to handle persistent 503s

    try:
        await transcription_service.process_audio(
            audio_id=task_payload.audio_id,
            audio_url=task_payload.audio_url,
            preset=task_payload.preset,
            chunking_config=task_payload.chunking_config,
            trace_id=trace_id,
        )
    except Exception as e:
        import logging
        import traceback

        logger = logging.getLogger("api.tasks")
        error_msg = str(e)

        # Double check for HTML in top-level handler
        if "<!DOCTYPE html>" in error_msg or "<html" in error_msg.lower():
            error_msg = "External Service Overloaded (HTML Response)"

        full_traceback = traceback.format_exc()
        logger.error(f"Error processing audio task (attempt {retry_count + 1}): {error_msg}\n{full_traceback}")

        # Record the error in the database for visibility
        from models.audio import AudioResource

        audio = await session.get(AudioResource, task_payload.audio_id)
        if audio:
            audio.error = f"{error_msg}\n\n{full_traceback}"
            audio.meta_data = {
                **(audio.meta_data or {}),
                "error": error_msg,
                "traceback": full_traceback,
            }
            if retry_count >= max_retries:
                logger.error(f"Max retries ({max_retries}) exceeded. Marking task as failed.")
                audio.status = "failed"
            session.add(audio)
            await session.commit()

        if retry_count >= max_retries:
            logger.error(f"Max retries ({max_retries}) exceeded. Marking task as failed.")
            if audio:
                audio.status = "failed"
                session.add(audio)
                await session.commit()
            return {"status": "failed", "reason": "Max retries exceeded"}

        # Sentry Fix: Check for known transient errors
        # If it's the specific "Transient Service Error" we raised, return 503 instead of raising.
        # This keeps Cloud Tasks retrying but prevents Sentry from alerting on an "Unhandled Exception".
        if "Transient Service Error" in error_msg or "External Service Overloaded" in error_msg:
            # log specifically for Cloud Tasks to see the reason
            logger.warning(f"Cloud Tasks Retry Triggered ({retry_count + 1}/{max_retries}): {error_msg}")
            from fastapi.responses import JSONResponse

            return JSONResponse(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                content={
                    "status": "retrying",
                    "reason": error_msg,
                    "attempt": retry_count + 1,
                },
            )

        # Re-raise for unknown errors or hard failures
        raise e

    return {"status": "success"}


@router.post("/sync-feeds", status_code=status.HTTP_200_OK)
async def sync_feeds_task(
    request: Request,
    session: AsyncSession = Depends(get_session),
):
    """
    Handler for Cloud Scheduler to sync podcast feeds.
    Verifies OIDC token to ensure request is authorized.
    """
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing Authorization header",
        )

    token = auth_header.split(" ")[1]

    try:
        from google.auth.transport import requests
        from google.oauth2 import id_token

        # Verify token - accepting any audience for now to simplify setup
        # In prod, restrict to specific audience
        id_info = id_token.verify_oauth2_token(token, requests.Request())

        if id_info["iss"] != "https://accounts.google.com":
            raise ValueError("Wrong issuer.")

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid OIDC token: {e!s}",
        )

    # Execute Sync
    from services.connector import PodcastService

    # Create ephemeral service
    # Note: PodcastService might need TranscriptionService
    service = PodcastService(transcription_service=transcription_service)

    try:
        await service.sync_all_feeds(session)
        return {"status": "success", "message": "Feed sync completed"}
    except Exception as e:
        import logging

        logger = logging.getLogger("api.tasks")
        logger.error(f"Feed sync failed: {e}", exc_info=True)
        # We assume 200 OK + error log is better for Scheduler than 500 which triggers retries indefinitely?
        # Actually Cloud Scheduler retries policies are configurable.
        # Let's return 500 so it shows as failed in Cloud Console.
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Feed sync failed: {e!s}")
