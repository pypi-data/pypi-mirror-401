import logging
import uuid
from typing import Annotated

from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    File,
    Form,
    HTTPException,
    Request,
    UploadFile,
    status,
)
from fastapi.responses import StreamingResponse
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from api.deps import get_current_user, get_current_user_optional, get_session
from core.entitlements import EntitlementsService
from core.limiter import limiter
from models.audio import AudioResource, AudioResourceRead, AudioResourceUpdate, AudioUrlRequest
from models.auth import User
from models.transcript import Transcript, TranscriptReadWithSegments
from services.queue import QueueService
from services.storage import StorageService
from services.transcription import TranscriptionService

router = APIRouter()
storage_service = StorageService()
transcription_service = TranscriptionService()
logger = logging.getLogger(__name__)


@router.post(
    "/transcribe_url",
    response_model=AudioResourceRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[],
)
@limiter.limit("10/minute")
async def transcribe_url(
    request: Request,
    url_request: AudioUrlRequest,
    background_tasks: BackgroundTasks,
    session: Annotated[AsyncSession, Depends(get_session)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    """
    Transcribe audio from a URL.
    """
    # 1. Resolve URL (Handle 'url' or 'audio_url')
    audio_url = url_request.url or url_request.audio_url
    if not audio_url:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Either 'url' or 'audio_url' must be provided",
        )

    entitlements = EntitlementsService(session)
    await entitlements.check_transcription_limit(current_user.organization_id, new_duration_seconds=0)

    # 4b. Deduplication Check
    existing_stmt = select(AudioResource).where(
        AudioResource.source_url == audio_url,
        AudioResource.user_id == current_user.id
    )
    existing_result = await session.execute(existing_stmt)
    existing_audio = existing_result.scalar_one_or_none()

    if existing_audio:
        logger.info(f"Deduplication hit: Found existing audio process for {audio_url} (ID: {existing_audio.id})")
        
        # If a new webhook_url is provided, update it
        if url_request.webhook_url:
            existing_audio.webhook_url = str(url_request.webhook_url)
            session.add(existing_audio)
            await session.commit()
            
            # If already completed or failed, fire the webhook immediately in background
            if existing_audio.status in ["completed", "failed"]:
                from services.webhook_dispatcher import WebhookDispatcher
                dispatcher = WebhookDispatcher(session)
                # Determine event type based on status
                event_type = "audio.completed" if existing_audio.status == "completed" else "audio.failed"
                
                # Fetch transcript if completed
                payload = {"id": str(existing_audio.id), "status": existing_audio.status}
                if existing_audio.status == "completed":
                    from models.transcript import Transcript
                    t_stmt = select(Transcript).where(Transcript.audio_resource_id == existing_audio.id)
                    t_res = await session.execute(t_stmt)
                    transcript = t_res.scalar_one_or_none()
                    if transcript:
                        payload["transcript"] = transcript.text
                
                # We need BackgroundTasks here, but transcribe_url signature doesn't have it.
                # Adding it to the signature below.
                background_tasks.add_task(
                    dispatcher.deliver_to_url, 
                    url=str(url_request.webhook_url), 
                    event_type=event_type,
                    payload=payload
                )

        # Populate return data if completed
        if existing_audio.status == "completed":
            from models.transcript import Transcript
            t_stmt = select(Transcript).where(Transcript.audio_resource_id == existing_audio.id)
            t_res = await session.execute(t_stmt)
            transcript = t_res.scalar_one_or_none()
            if transcript:
                return AudioResourceRead(
                    **existing_audio.model_dump(),
                    transcript=transcript.text,
                    # Summary and Entities would be fetched here too if they existed
                )
        
        return existing_audio

    # 5. Create Database Record
    audio_resource = AudioResource(
        title=audio_url.split("/")[-1] or "Audio from URL",
        source_url=audio_url,
        status="pending",
        user_id=current_user.id,
        meta_data={
            "rag_enabled": url_request.rag_enabled,
            "language": url_request.language,
        },
        webhook_url=str(url_request.webhook_url) if url_request.webhook_url else None,
    )
    session.add(audio_resource)
    await session.commit()
    await session.refresh(audio_resource)

    # 6. Trigger Transcription (Cloud Tasks)

    queue_service = QueueService()
    try:
        logger.info(f"Enqueuing transcription for audio {audio_resource.id} from URL {audio_url}...")
        queue_service.enqueue_transcription(
            audio_id=audio_resource.id,
            audio_url=audio_url,
            preset=url_request.preset,
            chunking_config=url_request.chunking_config if isinstance(url_request.chunking_config, dict) else None,
        )
        logger.info("Transcription enqueued successfully.")
    except Exception as e:
        logger.error(f"Failed to enqueue transcription task: {e}", exc_info=True)
        audio_resource.status = "failed"
        audio_resource.error = str(e)
        session.add(audio_resource)
        await session.commit()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to trigger transcription process: {e!s}",
        )

    return audio_resource


@router.post(
    "/upload",
    response_model=AudioResourceRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[],
)
@limiter.limit("10/minute")
async def upload_audio(
    request: Request,
    background_tasks: BackgroundTasks,
    session: Annotated[AsyncSession, Depends(get_session)],
    current_user: Annotated[User, Depends(get_current_user)],
    file: Annotated[UploadFile, File(description="Audio file to upload")],
    preset: Annotated[str | None, Form()] = "general",
    chunking_config: Annotated[str | None, Form()] = None,
):
    """
    Upload an audio file to the platform.

    - **file**: The audio file (MP3, WAV, M4A, etc.)
    """
    # 0. Check Entitlements
    from core.entitlements import EntitlementsService

    entitlements = EntitlementsService(session)

    # Debug logging for SDK/client requests
    logger.info(f"Upload request from user {current_user.email}")
    logger.info(f"Content-Type: {request.headers.get('content-type')}")
    logger.info(f"Filename: {file.filename}")
    logger.info(f"Preset: {preset}")
    logger.info(f"Chunking Config (raw): {chunking_config}")
    await entitlements.check_transcription_limit(current_user.organization_id, new_duration_seconds=0)

    # 1. Validate Content Type
    if not file.content_type:
        raise HTTPException(status_code=400, detail="Content type is missing")

    if not (file.content_type.startswith("audio/") or file.content_type.startswith("video/")):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid content type: {file.content_type}. Must be an audio or video file.",
        )

    if not file.filename:
        raise HTTPException(status_code=400, detail="Filename is missing")

    # 2. Generate Unique Filename
    file_ext = file.filename.split(".")[-1] if "." in file.filename else "bin"
    file_id = uuid.uuid4()
    blob_name = f"uploads/{file_id}.{file_ext}"

    # 3. Upload to GCS
    try:
        logger.info(f"Uploading file {file.filename} to bucket {storage_service.bucket_name}...")
        gcs_uri = storage_service.upload_file(file.file, blob_name, file.content_type)
        logger.info(f"File uploaded successfully: {gcs_uri}")
    except Exception as e:
        logger.error(f"GCS Upload Failed for {file.filename}: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to upload file to storage: {e!s}",
        )

    # 4. Create Database Record
    audio_resource = AudioResource(
        id=file_id,
        title=file.filename,
        source_url=gcs_uri,
        status="pending",
        user_id=current_user.id,
        meta_data={
            "original_filename": file.filename,
            "content_type": file.content_type,
            "size": getattr(file, "size", 0),
        },
    )
    session.add(audio_resource)
    await session.commit()
    await session.refresh(audio_resource)

    # 5. Trigger Transcription (Cloud Tasks)
    import json


    queue_service = QueueService()

    # Parse chunking_config if provided as JSON string
    config_dict = None
    if chunking_config:
        try:
            config_dict = json.loads(chunking_config)
        except json.JSONDecodeError:
            # If it's not JSON, might be a raw string or we just accept it as None if it fails
            config_dict = None

    try:
        logger.info(f"Enqueuing transcription for audio {audio_resource.id}...")
        queue_service.enqueue_transcription(
            audio_id=audio_resource.id, audio_url=gcs_uri, preset=preset or "general", chunking_config=config_dict
        )
        logger.info("Transcription enqueued successfully.")
    except Exception as e:
        logger.error(f"Failed to enqueue transcription task: {e}", exc_info=True)
        audio_resource.status = "failed"
        audio_resource.error = str(e)
        session.add(audio_resource)
        await session.commit()
        # We don't necessarily want to fail the whole request if DB record is created,
        # but for now let's return a 500 to indicate the process didn't complete.
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to trigger transcription process: {e!s}",
        )

    return audio_resource


@router.get("", response_model=list[AudioResourceRead])
async def list_audio(
    session: Annotated[AsyncSession, Depends(get_session)],
    current_user: Annotated[User, Depends(get_current_user)],
    limit: int = 50,
    offset: int = 0,
):
    """
    List all audio resources for the current user.
    """
    statement = (
        select(AudioResource)
        .where(AudioResource.user_id == current_user.id)
        .order_by(AudioResource.created_at.desc())
        .limit(limit)
        .offset(offset)
    )
    result = await session.exec(statement)
    return result.all()


@router.get("/{audio_id}", response_model=AudioResourceRead)
async def get_audio(
    audio_id: uuid.UUID,
    session: Annotated[AsyncSession, Depends(get_session)],
    current_user: Annotated[User | None, Depends(get_current_user_optional)],
):
    """
    Get an audio resource by ID.
    """
    audio_resource = await session.get(AudioResource, audio_id)
    if not audio_resource:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Audio resource not found",
        )

    # Allow access if resource is public OR if current user is owner
    if not audio_resource.is_public:
        if not current_user or audio_resource.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to access this resource",
            )

    return audio_resource


@router.patch("/{audio_id}", response_model=AudioResourceRead)
async def update_audio(
    audio_id: uuid.UUID,
    update_request: AudioResourceUpdate,
    session: Annotated[AsyncSession, Depends(get_session)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    """
    Update an audio resource (title, is_public).
    """
    audio_resource = await session.get(AudioResource, audio_id)
    if not audio_resource:
        raise HTTPException(status_code=404, detail="Audio resource not found")

    if audio_resource.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this resource")

    update_data = update_request.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(audio_resource, key, value)

    session.add(audio_resource)
    await session.commit()
    await session.refresh(audio_resource)
    return audio_resource


@router.get("/{audio_id}/transcript", response_model=TranscriptReadWithSegments)
async def get_transcript(
    audio_id: uuid.UUID,
    session: Annotated[AsyncSession, Depends(get_session)],
    current_user: Annotated[User | None, Depends(get_current_user_optional)],
):
    """
    Get the transcript for an audio resource, including segments.
    """
    # 1. Check if audio exists
    audio_resource = await session.get(AudioResource, audio_id)
    if not audio_resource:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Audio resource not found",
        )

    # Allow access if resource is public OR if current user is owner
    if not audio_resource.is_public:
        if not current_user or audio_resource.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to access this resource",
            )

    # 2. Get Transcript
    # We need to join with segments to avoid N+1 queries, but for now lazy loading is fine with async session if configured
    # Actually, SQLModel relationships are lazy by default.
    # Let's query Transcript directly by audio_resource_id
    statement = select(Transcript).where(Transcript.audio_resource_id == audio_id)
    result = await session.exec(statement)
    transcript = result.first()

    if not transcript:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transcript not found for this audio",
        )

    # Ensure segments are loaded (though response_model should handle it if eager loading was set,
    # but with async we might need explicit loading or rely on the relationship being accessible)
    # Since we defined the relationship, FastAPI/Pydantic will try to access .segments.
    # With AsyncSession, accessing a relationship that isn't loaded will raise an error.
    # We should use select options to eager load.
    from sqlalchemy.orm import selectinload

    statement = (
        select(Transcript).where(Transcript.audio_resource_id == audio_id).options(selectinload(Transcript.segments))
    )
    result = await session.exec(statement)
    transcript = result.first()

    if not transcript:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transcript not found for this audio",
        )

    return transcript


@router.get("/{audio_id}/content")
async def get_audio_content(
    audio_id: uuid.UUID,
    session: Annotated[AsyncSession, Depends(get_session)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    """
    Stream the audio content for a given audio resource.
    """
    audio_resource = await session.get(AudioResource, audio_id)
    if not audio_resource:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Audio resource not found",
        )

    # Check ownership
    if audio_resource.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this resource",
        )

    source_url = audio_resource.source_url
    if not source_url:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Audio content not available",
        )

    if source_url.startswith("gs://"):
        # Parse bucket and blob
        path_parts = source_url.replace("gs://", "").split("/", 1)
        bucket_name = path_parts[0]
        blob_name = path_parts[1]

        try:
            stream, content_type = storage_service.get_file_stream(bucket_name, blob_name)
            return StreamingResponse(stream, media_type=content_type)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to stream audio: {e!s}",
            )
    elif source_url.startswith(("http://", "https://")):
        # Redirect to the URL
        from fastapi.responses import RedirectResponse

        return RedirectResponse(url=source_url)
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported audio source URL scheme",
        )


@router.delete("/{audio_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_audio(
    audio_id: uuid.UUID,
    session: Annotated[AsyncSession, Depends(get_session)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    """
    Permanently delete an audio resource (and its transcript, embeddings, and source file).
    """
    from services.audio_service import AudioService

    audio_service = AudioService(session)
    await audio_service.delete_audio_resource(audio_id, current_user.id)
