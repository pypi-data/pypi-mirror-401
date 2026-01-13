import logging
from uuid import UUID

import anyio
from openai import AsyncOpenAI
from sqlalchemy import text
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession

from core.config import settings
from db.session import engine
from models.audio import AudioResource
from models.transcript import Transcript, TranscriptSegment
from services.embedding import EmbeddingService
from services.storage import StorageService
from services.trace import trace_service

logger = logging.getLogger(__name__)


class TranscriptionService:
    def __init__(self):
        self.client = AsyncOpenAI(
            api_key=settings.FIREWORKS_API_KEY,
            base_url="https://audio-prod.api.fireworks.ai/v1",
            timeout=600.0,
        )
        self.model = "whisper-v3"


    async def process_audio(
        self,
        audio_id: UUID,
        audio_url: str,
        preset: str = "general",
        chunking_config: dict | None = None,
        trace_id: str | None = None,
    ):
        """
        Process audio file: Download -> Transcribe -> Store in DB.
        This is meant to be run as a BackgroundTask.
        """
        async with trace_service.span(
            name="Process Audio Task",
            component="TranscriptionService",
            trace_id=trace_id,
            inputs={"audio_id": str(audio_id), "audio_url": audio_url, "preset": preset},
        ) as span:
            await self._process_audio_impl(audio_id, audio_url, preset, chunking_config)

    async def _process_audio_impl(
        self,
        audio_id: UUID,
        audio_url: str,
        preset_name: str = "general",
        chunking_config_override: dict | None = None,
    ):
        """
        Internal implementation of process_audio logic.
        """
        logger.info(f"Starting transcription for audio {audio_id} with preset {preset_name}")

        # Resolve Configuration
        from core.rag.chunking.semantic import SemanticChunkingStrategy
        from core.rag.presets import get_preset

        preset = get_preset(preset_name)
        config = preset.chunking_config
        if chunking_config_override:
            # Simple override
            for k, v in chunking_config_override.items():
                if hasattr(config, k):
                    setattr(config, k, v)

        # We need to manually manage the session context here since it's a background task
        async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

        async with async_session() as session:
            # 1. Update status to processing
            audio = await session.get(AudioResource, audio_id)
            if not audio:
                logger.error(f"Audio {audio_id} not found")
                return

            audio.status = "processing"
            session.add(audio)
            await session.commit()

            try:
                # 2. Pre-Processing: Optimization - Check if already bridged
                cached_gcs_uri = audio.storage_gcs_uri
                if cached_gcs_uri:
                    logger.info(f"Using cached GCS URI from previous attempt: {cached_gcs_uri}")
                    audio_url = cached_gcs_uri
                elif audio_url.startswith(("http://", "https://")):
                    logger.info(f"Bridging external URL to GCS: {audio_url}")
                    try:
                        storage = StorageService()
                        blob_name = f"uploads/transcription_{audio_id}.mp3"
                        # Run blocking bridge in a separate thread to avoid freezing the event loop
                        gcs_uri = await anyio.to_thread.run_sync(storage.upload_from_url, audio_url, blob_name)

                        # Update the URL to the new GCS URI so the next block handles it
                        audio_url = gcs_uri
                        logger.info(f"Bridge successful. New Source: {audio_url}")

                        # Optimization: Persist GCS URI immediately to prevent re-download on retry
                        audio.storage_gcs_uri = gcs_uri
                        session.add(audio)
                        await session.commit()
                        logger.info(f"Persisted GCS URI to audio resource: {gcs_uri}")

                    except Exception as bridge_err:
                        logger.error(f"Failed to bridge external URL to GCS: {bridge_err}")
                        raise bridge_err

                # 3. Optimization: Use Signed URL for Transcription (Avoid Proxy Bandwidth)
                use_signed_url = False
                signed_url = None

                if audio_url.startswith("gs://"):
                    try:
                        storage = StorageService()
                        path_parts = audio_url.replace("gs://", "").split("/", 1)
                        bucket_name = path_parts[0]
                        blob_name = path_parts[1]

                        # Generate Signed URL (valid for 1 hour)
                        # Fixed: signed URL generation might be slow or block, run in thread
                        signed_url = await anyio.to_thread.run_sync(
                            storage.generate_signed_url, bucket_name, blob_name, 60
                        )
                        logger.info(f"Generated GCS Signed URL for transcription: {blob_name}")
                        use_signed_url = True
                    except Exception as verify_err:
                        # Log but don't fail, fallback to download
                        logger.warning(f"Failed to generate signed URL, falling back to download: {verify_err}")

                # Default response object placeholder
                response_obj = None

                # 4. Transcription Execution (URL or Fallback)

                if use_signed_url and signed_url:
                    try:
                        logger.info("Attempting transcription via Signed URL (JSON API)...")

                        # Build JSON request as required by Fireworks for URL transcription.
                        json_payload = {
                            "model": self.model,
                            "file": signed_url,
                            "response_format": "verbose_json",
                            "timestamp_granularities": ["segment", "word"],
                        }

                        # Use internal client with JSON payload for URL path
                        response = await self.client.post("/audio/transcriptions", body=json_payload, cast_to=object)

                        logger.info("URL-based transcription successful.")

                        # Adapter for response
                        class MockResponse:
                            def __init__(self, data):
                                if isinstance(data, dict):
                                    self.text = data.get("text", "")
                                    self.language = data.get("language", "en")
                                    self.duration = data.get("duration", 0.0)
                                    self.segments = [
                                        type("Segment", (), s) if isinstance(s, dict) else s
                                        for s in data.get("segments", [])
                                    ]
                                    for s in self.segments:
                                        # Ensure words are accessible as objects
                                        if hasattr(s, "words") and s.words and isinstance(s.words[0], dict):
                                            s.words = [type("Word", (), w) for w in s.words]
                                else:
                                    # Assume it's an object
                                    self.text = getattr(data, "text", "")
                                    self.language = getattr(data, "language", "en")
                                    self.duration = getattr(data, "duration", 0.0)
                                    self.segments = getattr(data, "segments", [])

                        if isinstance(response, dict):
                            response_obj = MockResponse(response)
                        else:
                            response_obj = response

                    except Exception as url_err:
                        logger.error(
                            f"URL-based transcription failed for {audio_id}: {url_err}. "
                            "Aborting fallback to save proxy traffic cost."
                        )
                        raise url_err

                if not response_obj:
                    # Satisfy mypy and handle unexpected execution flows without a fallback
                    error_msg = f"Transcription failed for {audio_id}: No valid response received from Direct Path."
                    logger.error(error_msg)
                    raise RuntimeError(error_msg)

                transcript_text = response_obj.text

                # Create Transcript Record
                transcript = Transcript(
                    audio_resource_id=audio_id,
                    text=transcript_text,
                    model=self.model,
                    language=response_obj.language,
                )
                session.add(transcript)
                await session.commit()
                await session.refresh(transcript)

                # Initialize Embedding Service and Segments list
                embedding_service = EmbeddingService()
                segments_to_create: list[dict] = []

                # Collect all words for alignment
                all_words = []
                if hasattr(response_obj, "segments"):
                    for seg in response_obj.segments:
                        if hasattr(seg, "words") and seg.words:
                            all_words.extend(seg.words)

                # --- CHUNKING LOGIC ---
                if config.strategy_name == "semantic" and all_words:
                    logger.info("Using Semantic Chunking Strategy")
                    strategy = SemanticChunkingStrategy(config)
                    docs = strategy.chunk(transcript_text)
                elif config.strategy_name == "recursive" and all_words:
                    logger.info("Using Recursive Chunking Strategy")
                    from core.rag.chunking.recursive import RecursiveChunkingStrategy

                    strategy = RecursiveChunkingStrategy(config)
                    docs = strategy.chunk(transcript_text)
                else:
                    docs = []

                if docs:

                    word_cursor = 0
                    total_words = len(all_words)

                    for i, doc in enumerate(docs):
                        content = doc.page_content.strip()
                        if not content:
                            continue

                        doc_words = content.split()
                        if not doc_words:
                            continue

                        start_time = 0.0
                        end_time = 0.0
                        chunk_words = []

                        if word_cursor >= total_words:
                            break

                        current_word_obj = all_words[word_cursor]
                        start_time = (
                            current_word_obj.get("start")
                            if isinstance(current_word_obj, dict)
                            else current_word_obj.start
                        ) or 0.0
                        accumulated_len = 0
                        target_len = len(content)

                        while word_cursor < total_words:
                            w = all_words[word_cursor]
                            w_text = (w.get("word") if isinstance(w, dict) else w.word) or ""
                            accumulated_len += len(w_text)
                            chunk_words.append(w)
                            word_cursor += 1
                            if accumulated_len >= target_len:
                                break

                        last_word = chunk_words[-1]
                        end_time = (last_word.get("end") if isinstance(last_word, dict) else last_word.end) or 0.0

                        segments_to_create.append(
                            {
                                "start": start_time,
                                "end": end_time,
                                "text": content,
                                "words": [
                                    {
                                        "word": w.get("word") if isinstance(w, dict) else w.word,
                                        "start": w.get("start") if isinstance(w, dict) else w.start,
                                        "end": w.get("end") if isinstance(w, dict) else w.end,
                                    }
                                    for w in chunk_words
                                ],
                                "overlap_context_before": None,
                                "overlap_context_after": None,
                            }
                        )

                else:
                    logger.info("Using Rule-Based / Fallback Chunking Strategy")
                    # Logic 1: Use word timestamps
                    if all_words:
                        MAX_CHUNK_SIZE = 1000
                        MIN_CHUNK_SIZE = 100
                        PAUSE_THRESHOLD = 1.5
                        OVERLAP_WORDS = 25

                        current_chunk_words = []
                        current_chunk_text_len = 0
                        previous_chunk_tail = None

                        for i, word_obj in enumerate(all_words):
                            # Robust access for dict or object
                            word_text = (
                                getattr(word_obj, "word", "")
                                if not isinstance(word_obj, dict)
                                else word_obj.get("word", "")
                            )
                            if not word_text:
                                word_text = ""

                            current_chunk_words.append(word_obj)
                            current_chunk_text_len += len(word_text)

                            pause_duration = 0.0
                            is_long_pause = False
                            if i < len(all_words) - 1:
                                current_end = (
                                    word_obj.get("end", 0)
                                    if isinstance(word_obj, dict)
                                    else getattr(word_obj, "end", 0)
                                )
                                next_word = all_words[i + 1]
                                next_start = (
                                    next_word.get("start", 0)
                                    if isinstance(next_word, dict)
                                    else getattr(next_word, "start", 0)
                                )
                                pause_duration = next_start - current_end
                                is_long_pause = pause_duration >= PAUSE_THRESHOLD

                            is_sentence_end = word_text.strip().endswith((".", "?", "!"))
                            is_max_size = current_chunk_text_len >= MAX_CHUNK_SIZE
                            is_min_size = current_chunk_text_len >= MIN_CHUNK_SIZE
                            is_last_word = i == len(all_words) - 1

                            should_split = (
                                is_max_size
                                or (is_min_size and is_long_pause)
                                or (is_min_size and is_sentence_end and pause_duration >= 0.5)
                                or is_last_word
                            )

                            if should_split:
                                start_time = (
                                    current_chunk_words[0].get("start")
                                    if isinstance(current_chunk_words[0], dict)
                                    else current_chunk_words[0].start
                                ) or 0.0
                                end_time = (
                                    current_chunk_words[-1].get("end")
                                    if isinstance(current_chunk_words[-1], dict)
                                    else current_chunk_words[-1].end
                                ) or 0.0

                                # reconstruct text
                                text_content = " ".join(
                                    [
                                        w.get("word", "") if isinstance(w, dict) else getattr(w, "word", "")
                                        for w in current_chunk_words
                                    ]
                                ).strip()

                                # Overlap logic
                                overlap_before = None
                                if previous_chunk_tail:
                                    overlap_before = " ".join(
                                        [
                                            w.get("word", "") if isinstance(w, dict) else getattr(w, "word", "")
                                            for w in previous_chunk_tail
                                        ]
                                    ).strip()

                                current_chunk_tail = (
                                    current_chunk_words[-OVERLAP_WORDS:]
                                    if len(current_chunk_words) > OVERLAP_WORDS
                                    else current_chunk_words
                                )

                                if text_content:
                                    seg_data = {
                                        "start": start_time,
                                        "end": end_time,
                                        "text": text_content,
                                        "words": [
                                            {
                                                "word": w.get("word") if isinstance(w, dict) else w.word,
                                                "start": w.get("start") if isinstance(w, dict) else w.start,
                                                "end": w.get("end") if isinstance(w, dict) else w.end,
                                            }
                                            for w in current_chunk_words
                                        ],
                                        "overlap_context_before": overlap_before,
                                        "overlap_context_after": None,
                                    }
                                    if segments_to_create:
                                        # update previous overlap
                                        chunk_head = (
                                            current_chunk_words[:OVERLAP_WORDS]
                                            if len(current_chunk_words) > OVERLAP_WORDS
                                            else current_chunk_words
                                        )
                                        segments_to_create[-1]["overlap_context_after"] = " ".join(
                                            [
                                                w.get("word", "") if isinstance(w, dict) else getattr(w, "word", "")
                                                for w in chunk_head
                                            ]
                                        ).strip()

                                    segments_to_create.append(seg_data)

                                previous_chunk_tail = current_chunk_tail
                                current_chunk_words = []
                                current_chunk_text_len = 0

                    elif hasattr(response_obj, "segments"):
                        # Fallback to segments
                        for seg in response_obj.segments:
                            # Robust
                            seg_text = seg.get("text") if isinstance(seg, dict) else getattr(seg, "text", "")
                            seg_start = seg.get("start") if isinstance(seg, dict) else seg.start
                            seg_end = seg.get("end") if isinstance(seg, dict) else seg.end

                            if seg_text and seg_text.strip():
                                segments_to_create.append(
                                    {"start": seg_start, "end": seg_end, "text": seg_text, "words": None}
                                )

                # --- END CHUNKING LOGIC ---

                # 3. Process and Store Segments
                logger.info(f"Created {len(segments_to_create)} chunks using {config.strategy_name} strategy")
                # 4. Generate Embeddings (BATCHED)
                logger.info(f"Generating embeddings for {len(segments_to_create)} segments...")
                segment_texts = [seg["text"] for seg in segments_to_create]
                try:
                    embeddings = await embedding_service.generate_embeddings(segment_texts)
                except Exception as e:
                    logger.error(f"Failed to generate batched embeddings: {e}")
                    # If batching fails, we might want to try individually or fail the task
                    raise e

                # 5. Save Segments to DB
                for i, seg_data in enumerate(segments_to_create):
                    segment = TranscriptSegment(
                        transcript_id=transcript.id,
                        start=seg_data["start"],
                        end=seg_data["end"],
                        text=seg_data["text"],
                        words=seg_data.get("words"),
                        embedding=embeddings[i],
                        overlap_context_before=seg_data.get("overlap_context_before"),
                        overlap_context_after=seg_data.get("overlap_context_after"),
                    )
                    session.add(segment)

                await session.commit()

                # Update tsvector
                await session.execute(
                    text(
                        "UPDATE transcript_segments SET content_vector = to_tsvector('english', text) WHERE transcript_id = :tid"
                    ).params(tid=str(transcript.id))
                )
                await session.commit()

                # Update Audio Status
                audio.status = "completed"
                session.add(audio)
                await session.commit()

                logger.info(f"Transcription completed for {audio_id}")

                # Trigger Webhook if configured
                if audio.webhook_url:
                    try:
                        from services.webhook_dispatcher import WebhookDispatcher
                        dispatcher = WebhookDispatcher(session)
                        # We don't have BackgroundTasks here easily, but we can await it or run in thread
                        # Since this is already a background task, we can just await it
                        await dispatcher.deliver_to_url(
                            url=audio.webhook_url,
                            event_type="audio.completed",
                            payload={
                                "id": str(audio.id),
                                "status": "completed",
                                "transcript": transcript_text,
                            }
                        )
                        logger.info(f"Webhook delivered for completed audio {audio_id}")
                    except Exception as wh_err:
                        logger.error(f"Failed to deliver completion webhook for {audio_id}: {wh_err}")

                # 5. Update Usage & Duration
                # Calculate duration from response or segments
                duration_seconds = 0.0
                if hasattr(response_obj, "duration"):
                    duration_seconds = response_obj.duration
                elif hasattr(response_obj, "segments") and response_obj.segments:
                    # Fallback to end of last segment
                    last_seg = response_obj.segments[-1]
                    duration_seconds = (last_seg.get("end") if isinstance(last_seg, dict) else last_seg.end) or 0.0

                audio.duration_seconds = duration_seconds
                session.add(audio)
                await session.commit()

                # Increment Usage for Organization
                try:
                    from services.usage_service import UsageService

                    # We need to fetch the User to get Org ID
                    stmt = text("SELECT organization_id FROM users WHERE id = :uid")
                    result = await session.execute(stmt, {"uid": audio.user_id})
                    org_id = result.scalar()

                    if org_id:
                        usage_service = UsageService(session)
                        await usage_service.increment_usage(org_id, int(duration_seconds))
                        await session.commit()
                        logger.info(f"Incremented usage for org {org_id} by {duration_seconds}s")
                except Exception as e:
                    logger.error(f"Failed to increment usage: {e}", exc_info=True)

            except Exception as e:
                # Trigger Webhook for failure if configured
                if hasattr(self, 'session_factory'): # This is tricky since we are inside a session block
                    pass
                
                # We need to be careful here. If we re-raise, the task might retry.
                # Usually we only want to fire 'failed' webhook on final failure.
                # However, for now let's fire it and rely on the client to handle retries or just use it as a 'current status' update.
                # Actually, better to only fire on final failure in the endpoint handler.
                # But TranscriptionService doesn't know about retry count.
                
                # Let's try to fire it here if possible, but keep the re-raise for Cloud Tasks.
                async_session_fail = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
                async with async_session_fail() as session_fail:
                    audio_fail = await session_fail.get(AudioResource, audio_id)
                    if audio_fail and audio_fail.webhook_url:
                         try:
                            from services.webhook_dispatcher import WebhookDispatcher
                            dispatcher = WebhookDispatcher(session_fail)
                            await dispatcher.deliver_to_url(
                                url=audio_fail.webhook_url,
                                event_type="audio.failed",
                                payload={
                                    "id": str(audio_id),
                                    "status": "failed",
                                    "error": str(e)
                                }
                            )
                         except Exception:
                             pass

                raise e
