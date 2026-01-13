import asyncio
import logging
import time
import uuid
from contextlib import asynccontextmanager
from contextvars import ContextVar
from datetime import datetime
from typing import Any

from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession

from db.session import engine
from models.trace import TraceEvent

logger = logging.getLogger(__name__)

# Context Vars for Trace Context
_trace_id_ctx: ContextVar[str | None] = ContextVar("trace_id", default=None)
_parent_span_id_ctx: ContextVar[str | None] = ContextVar("parent_span_id", default=None)


class TraceService:
    def __init__(self):
        self._background_tasks = set()

    def _track_task(self, task: asyncio.Task[Any]):
        self._background_tasks.add(task)
        task.add_done_callback(self._background_tasks.discard)

    def _serialize(self, obj: Any, _depth: int = 0) -> Any:
        """
        Recursively serialize objects to be JSON-safe for DB storage.
        Handles Pydantic models, lists, dicts, and UUIDs.
        Redacts sensitive keys and truncates long strings.
        """
        if obj is None:
            return None

        # Max recursion depth to prevent infinite loops
        if _depth > 20:
            return "[MAX_DEPTH_REACHED]"

        # Handle UUIDs
        if isinstance(obj, uuid.UUID):
            return str(obj)

        # Handle Pydantic models (v1/v2 compatibility)
        if hasattr(obj, "model_dump"):
            return self._serialize(obj.model_dump(), _depth + 1)
        if hasattr(obj, "dict"):
            return self._serialize(obj.dict(), _depth + 1)

        # Handle lists/tuples
        if isinstance(obj, list | tuple):
            return [self._serialize(item, _depth + 1) for item in obj]

        # Handle dicts
        if isinstance(obj, dict):
            sensitive_keys = {
                "system_prompt",
                "prompt",
                "api_key",
                "token",
                "secret",
                "password",
                "key",
                "credential",
                "authorization",
            }
            res = {}
            # Special case for LLM messages: redact content if it's a system message
            is_system_message = str(obj.get("role", "")).lower() == "system"

            for k, v in obj.items():
                k_str = str(k).lower()
                if any(sk in k_str for sk in sensitive_keys):
                    res[str(k)] = "[REDACTED]"
                elif is_system_message and k_str == "content":
                    res[str(k)] = "[REDACTED_SYSTEM_PROMPT]"
                else:
                    res[str(k)] = self._serialize(v, _depth + 1)
            return res

        # Basic JSON serializable types
        if isinstance(obj, str | int | float | bool):
            # Truncate extremely long strings (likely internal context or large outputs)
            if isinstance(obj, str) and len(obj) > 10000:
                return f"{obj[:500]}... [TRUNCATED {len(obj)} chars]"
            return obj

        # Datetime
        if isinstance(obj, datetime):
            return obj.isoformat()

        # Fallback to string representation
        return str(obj)

    async def wait_for_tasks(self):
        """Wait for all background tasks to complete."""
        if self._background_tasks:
            await asyncio.gather(*self._background_tasks, return_exceptions=True)

    @property
    def current_trace_id(self) -> str | None:
        return _trace_id_ctx.get()

    @property
    def current_parent_span_id(self) -> str | None:
        return _parent_span_id_ctx.get()

    @asynccontextmanager
    async def span(
        self,
        name: str,
        component: str,
        trace_id: str | None = None,
        inputs: dict[str, Any] | None = None,
        metadata: dict[str, Any] | None = None,
        user_id: uuid.UUID | None = None,
    ):
        """
        Async context manager to record a trace span.
        """
        start_time = datetime.utcnow()
        start_ts = time.time()

        # Determine Trace ID
        current_trace = _trace_id_ctx.get()
        if trace_id:
            active_trace_id = trace_id
        elif current_trace:
            active_trace_id = current_trace
        else:
            active_trace_id = str(uuid.uuid4())

        # Determine Parent Span ID
        parent_span_id = _parent_span_id_ctx.get()

        # Generate new Span ID
        span_id = str(uuid.uuid4())

        # Set Context for children
        token_trace = _trace_id_ctx.set(active_trace_id)
        token_parent = _parent_span_id_ctx.set(span_id)

        span_data: dict[str, Any] = {"outputs": {}, "status": "success", "error_message": None}

        try:
            yield SpanContext(span_data)
        except Exception as e:
            span_data["status"] = "error"
            span_data["error_message"] = str(e)
            raise e
        finally:
            # Calculate duration
            end_time = datetime.utcnow()
            latency_ms = (time.time() - start_ts) * 1000

            # Reset Context
            _trace_id_ctx.reset(token_trace)
            _parent_span_id_ctx.reset(token_parent)

            # Persist Event
            # We use a fire-and-forget approach or background task ideally,
            # but for now we'll just save it.
            # Persist Event in background to avoid blocking the critical path
            try:
                # We use asyncio.create_task to fire and forget the DB write
                event = TraceEvent(
                    trace_id=active_trace_id,
                    span_id=span_id,
                    parent_span_id=parent_span_id,
                    event_type="span",
                    component=component,
                    name=name,
                    inputs=self._serialize(inputs) if inputs else {},
                    outputs=self._serialize(span_data["outputs"]) if span_data.get("outputs") else {},
                    meta=self._serialize(span_data.get("metadata", {})),
                    start_time=start_time,
                    end_time=end_time,
                    latency_ms=latency_ms,
                    status=span_data["status"],
                    error_message=span_data["error_message"],
                    user_id=user_id,
                )
                task = asyncio.create_task(self._save_event(event))
                self._track_task(task)
            except Exception as e:
                logger.error(f"Failed to schedule trace event save: {e}")

    async def _save_event(self, event: TraceEvent):
        # Create a new session for saving the log to avoid interfering with main transaction
        async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
        async with async_session() as session:
            session.add(event)
            await session.commit()


class SpanContext:
    def __init__(self, data: dict[str, Any]):
        self._data = data

    def set_output(self, output: Any):
        # Use recursive serialization
        self._data["outputs"] = trace_service._serialize(output)

    def set_metadata(self, key: str, value: Any):
        if "metadata" not in self._data:
            self._data["metadata"] = {}
        self._data["metadata"][key] = value


# Global instance
trace_service = TraceService()
