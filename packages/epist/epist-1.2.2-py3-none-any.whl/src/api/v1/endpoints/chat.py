import json
import logging

from fastapi import APIRouter, Depends, HTTPException, Request
from openai import AsyncOpenAI, AsyncStream
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession

from api.deps import get_current_user
from core.config import settings
from db.session import engine
from models.auth import Organization, User
from models.transcript import Transcript
from services.search import SearchService
from services.trace import trace_service

router = APIRouter()
logger = logging.getLogger(__name__)

# Initialize Services
search_service = SearchService()

# Initialize OpenAI Client
# Note: We use AsyncOpenAI for non-blocking calls
client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: list[ChatMessage]
    stream: bool = False
    model: str = "gpt-3.5-turbo"
    tier: str = "free"
    rrf_k: int | None = None
    rerank_model: str | None = None
    audio_resource_id: str | None = None  # Optional: focus context on a specific audio


class Citation(BaseModel):
    id: str
    text: str
    start: float
    end: float
    score: float


class ChatResponse(BaseModel):
    id: str
    object: str = "chat.completion"
    created: int
    model: str
    choices: list[dict]
    citations: list[Citation] | None = None
    trace_id: str | None = None


async def generate_standalone_query(messages: list[ChatMessage]) -> str:
    """
    Given a conversation history, generate a standalone query for retrieval.
    """
    if len(messages) <= 1:
        return messages[-1].content

    # Take last 5 messages for context
    context = "\n".join([f"{m.role}: {m.content}" for m in messages[-5:]])
    prompt = f"""Given the following conversation history and a follow-up message, rephrase the follow-up message to be a standalone question that can be used for searching a knowledge base.

Conversation History:
{context}

Standalone Question:"""

    try:
        completion = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            max_tokens=100,
        )
        return completion.choices[0].message.content or messages[-1].content
    except Exception as e:
        logger.error(f"Failed to generate standalone query: {e}")
        return messages[-1].content


@router.post("/completions")
async def chat_completions(
    request: ChatRequest, fastapi_request: Request, current_user: User = Depends(get_current_user)
):
    """
    Chat with your audio knowledge base.
    """
    # Use the request ID from middleware as the trace ID for consistency
    trace_id = getattr(fastapi_request.state, "request_id", None)

    async with trace_service.span(
        "Chat Request", component="ChatEndpoint", inputs=request.dict(), user_id=current_user.id, trace_id=trace_id
    ) as span:
        # Enforce Tiered Model Access for API Calls
        auth_method = getattr(fastapi_request.state, "auth_method", "session")

        async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
        async with async_session() as session:
            org = await session.get(Organization, current_user.organization_id)
            actual_tier = org.tier if org else "free"

        if auth_method == "api_key":
            if actual_tier == "free" and request.model != "gpt-3.5-turbo":
                logger.warning(
                    f"Free tier API user {current_user.id} attempted to use {request.model}. Downgrading to gpt-3.5-turbo."
                )
                request.model = "gpt-3.5-turbo"
            # Also sync request.tier with actual tier for API calls to prevent bypass of search mode
            request.tier = actual_tier

        try:
            # 1. Generate Standalone Query for Retrieval
            # This helps handle "tell me more" or "explain this" using context history
            async with trace_service.span(
                "Generate Standalone Query", component="ChatEndpoint", inputs={"messages": request.messages}
            ) as query_span:
                standalone_query = await generate_standalone_query(request.messages)
                query_span.set_output({"standalone_query": standalone_query})

            # 2. Retrieve Context (RAG)
            # Find transcript_id if audio_resource_id is provided
            transcript_id = None
            if request.audio_resource_id:
                async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
                async with async_session() as session:
                    stmt = select(Transcript).where(Transcript.audio_resource_id == request.audio_resource_id)
                    result = await session.execute(stmt)
                    transcript = result.scalars().first()
                    if transcript:
                        transcript_id = transcript.id

            async with trace_service.span(
                "Retrieve Context",
                component="ChatEndpoint",
                inputs={"query": standalone_query},
                user_id=current_user.id,
            ) as retrieval_span:
                # Increased limit to 10 for better coverage
                search_results = await search_service.search(
                    standalone_query,
                    limit=10,
                    tier=request.tier,
                    rrf_k=request.rrf_k,
                    rerank_model=request.rerank_model,
                    transcript_id=transcript_id,
                )
                retrieval_span.set_output(search_results)

            # Format Context - Deduplicate by text to avoid redundant context
            seen_text = set()
            unique_results = []
            for r in search_results:
                if r["text"] not in seen_text:
                    seen_text.add(r["text"])
                    unique_results.append(r)

            context_text = "\n\n".join(
                [
                    f"[Source {i + 1}] (Time: {int(r['start'])}s - {int(r['end'])}s): {r['text']}"
                    for i, r in enumerate(unique_results)
                ]
            )

            # 3. Construct System Prompt
            system_prompt = f"""You are an AI assistant for an audio knowledge base. 
Answer the user's question based on the provided context. Use the provided context to synthesize a helpful response.

When referencing information from the context, use inline citations in the format [Source N], where N corresponds to the source number in the context below. 

Crucially, do not group multiple citations like [Source 1, Source 2]. Instead, list them individually like [Source 1] [Source 2].

If the context contains multiple segments, combine them into a coherent answer.
If the context is about a specific episode or transcript, you can summarize and explain its topics based on the segments below.

If the answer is absolutely not in the context, say "I don't have enough information in the audio context to answer that."

Context:
{context_text}
"""

            # 4. Prepare Messages for LLM
            messages = [
                {"role": "system", "content": system_prompt},
                *[{"role": m.role, "content": m.content} for m in request.messages],
            ]

            # 5. Call LLM
            async with trace_service.span(
                "LLM Generation",
                component="ChatEndpoint",
                inputs={"model": request.model, "messages": messages},
                user_id=current_user.id,
            ) as llm_span:
                # Capture current trace_id for frontend linkage
                active_trace_id = trace_service.current_trace_id

                if request.stream:
                    # Streaming Response
                    async def stream_generator():
                        # Yield trace ID first for early UI linkage
                        yield f"data: {json.dumps({'trace_id': active_trace_id})}\n\n"

                        # Send citations at the beginning so the UI can use them for inline references immediately
                        citations = [
                            {
                                "id": str(r["id"]),
                                "text": r["text"],
                                "start": r["start"],
                                "end": r["end"],
                                "score": r["score"],
                            }
                            for r in search_results
                        ]
                        yield f"data: {json.dumps({'citations': citations})}\n\n"

                        stream = await client.chat.completions.create(
                            model=request.model, messages=messages, stream=True
                        )
                        full_content = ""
                        async for chunk in stream:
                            content = chunk.choices[0].delta.content
                            if content:
                                full_content += content
                                yield f"data: {json.dumps({'content': content})}\n\n"

                        yield "data: [DONE]\n\n"

                        # Record output in trace (collected content)
                        # Note: This runs after the generator finishes, so we might need a better way
                        # to capture streaming output in the span if we want it real-time,
                        # but for now capturing the full text at end is fine.
                        # However, since this is a generator, the span context will have exited.
                        # We need to manually save the output or structure this differently.
                        # For now, we won't capture full streaming output in the span to avoid complexity.

                    from fastapi.responses import StreamingResponse

                    return StreamingResponse(stream_generator(), media_type="text/event-stream")

                else:
                    # Standard Response
                    completion = await client.chat.completions.create(
                        model=request.model,
                        messages=messages,  # type: ignore
                        stream=False,  # type: ignore
                    )

                    assert not isinstance(completion, AsyncStream)

                    response_content = completion.choices[0].message.content
                    llm_span.set_output({"content": response_content})

                    citations = [
                        Citation(id=str(r["id"]), text=r["text"], start=r["start"], end=r["end"], score=r["score"])
                        for r in search_results
                    ]

                    response = {
                        "id": completion.id,
                        "object": "chat.completion",
                        "created": completion.created,
                        "model": completion.model,
                        "choices": [
                            {
                                "index": 0,
                                "message": {"role": "assistant", "content": response_content},
                                "finish_reason": "stop",
                            }
                        ],
                        "citations": citations,
                        "trace_id": active_trace_id,
                    }
                    span.set_output(response)
                    return response

        except Exception as e:
            logger.error(f"Chat Error: {e}")
            raise HTTPException(status_code=500, detail=str(e))
