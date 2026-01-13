import time
import uuid
from collections.abc import Callable

from fastapi import Request, Response
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

from models.log import RequestLog


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp):
        super().__init__(app)
        super().__init__(app)

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        request_id = str(uuid.uuid4())
        start_time = time.time()

        # Store request_id in state for other parts of the app to use
        request.state.request_id = request_id

        response = await call_next(request)

        process_time = (time.time() - start_time) * 1000  # in ms

        # Extract details
        # Note: API Key extraction depends on how auth middleware sets it.
        # Assuming auth middleware might set request.state.api_key_id or we parse header if not set.
        api_key_id = getattr(request.state, "api_key_id", None)
        user_id = getattr(request.state, "user_id", None)

        # We run the logging in the background to not block the response
        # However, BaseHTTPMiddleware doesn't easily support background tasks *after* response is sent
        # without using BackgroundTasks which is attached to response.
        # For simplicity and reliability in this context, we'll await the log saving.
        # In high throughput, this should be offloaded to a queue (like Cloud Tasks or PubSub).

        if request.url.path.startswith(("/api/v1/logs", "/health", "/docs", "/openapi.json")):
            return response

        # Use a background task if possible, but for now ensure we catch errors
        try:
            await self.log_request(
                request_id=request_id,
                request=request,
                response=response,
                process_time=process_time,
                api_key_id=api_key_id,
                user_id=user_id,
            )
        except Exception as e:
            import sys

            # Write to stderr so it shows up in Cloud Run logs even if logger is broken
            sys.stderr.write(f"ERROR: Failed to log request: {e}\n")

        return response

    async def log_request(
        self,
        request_id: str,
        request: Request,
        response: Response,
        process_time: float,
        api_key_id: uuid.UUID | None,
        user_id: uuid.UUID | None,
    ):
        try:
            # Import engine here to ensure we get the patched version in tests
            from db.session import engine

            async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

            async with async_session() as session:
                log_entry = RequestLog(
                    request_id=request_id,
                    method=request.method,
                    path=request.url.path,
                    status_code=response.status_code,
                    latency_ms=process_time,
                    ip_address=request.client.host if request.client else None,
                    user_agent=request.headers.get("user-agent"),
                    api_key_id=api_key_id,
                    user_id=user_id,
                )
                session.add(log_entry)
                await session.commit()
        except Exception as e:
            # Fail silently or log to stderr so we don't crash the request
            print(f"Failed to save request log: {e}")
