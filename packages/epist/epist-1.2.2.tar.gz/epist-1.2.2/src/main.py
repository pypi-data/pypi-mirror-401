import logging
import os
import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse, ORJSONResponse
from sqlmodel import SQLModel, text

from api.v1.endpoints import admin as admin_router
from api.v1.endpoints import audio as audio_router
from api.v1.endpoints import auth as auth_router
from api.v1.endpoints import billing as billing_router
from api.v1.endpoints import chat as chat_router
from api.v1.endpoints import connectors as connectors_router
from api.v1.endpoints import diagnostic as diagnostic_router
from api.v1.endpoints import ingestion as ingestion_router
from api.v1.endpoints import integrations as integrations_router
from api.v1.endpoints import logs as logs_router
from api.v1.endpoints import organization as organization_router
from api.v1.endpoints import search as search_router
from api.v1.endpoints import stats as stats_router
from api.v1.endpoints import tasks as tasks_router
from api.v1.endpoints import traces as traces_router
from api.v1.endpoints import webhooks as webhooks_router
from core.config import settings
from core.logging_utils import PIIFilter
from core.middleware import RequestLoggingMiddleware
from db.session import engine

# Disable gRPC for Google Cloud Storage to avoid fork/threading issues
os.environ["GOOGLE_CLOUD_DISABLE_GRPC"] = "true"

# Import models to register them with SQLModel

# Configure Logging
logging.basicConfig(
    level=settings.LOG_LEVEL,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logging.getLogger().addFilter(PIIFilter())
logger = logging.getLogger(__name__)

# Initialize Sentry
if settings.SENTRY_DSN:
    import sentry_sdk

    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        environment=settings.ENVIRONMENT,
        traces_sample_rate=0.1 if settings.ENVIRONMENT == "prod" else 1.0,
        release=f"epist-api@{settings.PROJECT_NAME}",  # Ideally get version from generic source
    )
    logger.info("Sentry initialized")


async def init_db():
    async with engine.begin() as conn:
        # Enable pgvector extension
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        # Create tables
        await conn.run_sync(SQLModel.metadata.create_all)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic (DB connection, etc.)
    print("Starting Epist.ai API...")

    try:
        if settings.ENVIRONMENT == "development":
            await init_db()
            logger.info("Database initialized successfully (Development Mode)")
        else:
            logger.info(f"Skipping init_db in {settings.ENVIRONMENT} mode. Relying on Alembic migrations.")
    except Exception as e:
        logger.warning(f"Database initialization failed (will retry on first request): {e}")
    yield
    # Shutdown logic
    print("Shutting down...")


# Trigger CI/CD Optimization Verification
# AI & Developer friendly metadata
app = FastAPI(
    title="Epist.ai API",
    description="""
    Production-ready Audio Intelligence REST API. 
    Transcribe audio from files or URLs, process with RAG, and search across your audio knowledge base.
    
    ### Core Capabilities:
    * **Transcription**: High-accuracy STT with speaker diarization.
    * **Audio RAG**: Hybrid search (semantic + lexical) over audio segments.
    * **Sharing**: Public transcript views with viral conversion loops.
    
    Built for developers and AI agents.
    """,
    version="1.1.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    default_response_class=ORJSONResponse,
    docs_url="/docs",
    redoc_url="/redoc",
    contact={
        "name": "Epist.ai Support",
        "url": "https://epist.ai",
        "email": "support@epist.ai",
    },
)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error", "path": str(request.url.path)},
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    logger.error(f"Validation error at {request.url.path}: {errors}")
    # Also print to stderr for Cloud Run logs visibility

    # Debug: Log body/form keys for validation errors
    try:
        content_type = request.headers.get("content-type", "")
        if "multipart/form-data" in content_type:
            form = await request.form()
            sys.stderr.write(f"DEBUG FORM KEYS: {list(form.keys())}\n")
        elif "application/json" in content_type:
            body = await request.json()
            if isinstance(body, dict):
                sys.stderr.write(f"DEBUG JSON KEYS: {list(body.keys())}\n")
    except Exception as e:
        sys.stderr.write(f"DEBUG BODY READ ERROR: {e}\n")

    return JSONResponse(
        status_code=422,
        content={"detail": errors, "path": str(request.url.path)},
    )


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "epist"}


@app.get("/health/connectivity")
async def connectivity_check():
    import socket

    results = {}
    hosts = [
        "google.com",
        "storage.googleapis.com",
        "api.fireworks.ai",
    ]
    for host in hosts:
        try:
            # We only return status, not IP, to avoid internal network disclosure
            socket.gethostbyname(host)
            results[host] = {"status": "ok"}
        except Exception:
            results[host] = {"status": "error"}

    return results


# Include Routers
app.include_router(audio_router.router, prefix="/api/v1/audio", tags=["Audio"])
app.include_router(diagnostic_router.router, prefix="/api/v1/diagnostic", tags=["Diagnostic"])
app.include_router(search_router.router, prefix="/api/v1/search", tags=["Search"])
app.include_router(stats_router.router, prefix="/api/v1/stats", tags=["Stats"])
app.include_router(tasks_router.router, prefix="/api/v1/tasks", tags=["Tasks"])
app.include_router(auth_router.router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(logs_router.router, prefix="/api/v1/logs", tags=["Logs"])
app.include_router(chat_router.router, prefix="/api/v1/chat", tags=["Chat"])
app.include_router(traces_router.router, prefix="/api/v1/traces", tags=["Traces"])
app.include_router(connectors_router.router, prefix="/api/v1/connectors", tags=["Connectors"])
app.include_router(webhooks_router.router, prefix="/api/v1/webhooks", tags=["Webhooks"])
app.include_router(billing_router.router, prefix="/api/v1/billing", tags=["Billing"])
app.include_router(organization_router.router, prefix="/api/v1/organizations", tags=["Organizations"])
app.include_router(admin_router.router, prefix="/api/v1/admin", tags=["Admin"])
app.include_router(ingestion_router.router, prefix="/api/v1/ingest", tags=["Ingestion"])
app.include_router(integrations_router.router, prefix="/api/v1/integrations", tags=["Integrations"])

# Middleware
app.add_middleware(RequestLoggingMiddleware)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
    allow_origin_regex=settings.CORS_ORIGIN_REGEX,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rate Limiting
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from core.limiter import limiter

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)  # type: ignore
app.add_middleware(SlowAPIMiddleware)


# Security Headers Middleware
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Content-Security-Policy"] = "default-src 'self'; frame-ancestors 'none';"
    return response


# Performance: GZip Compression
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Security: Trusted Hosts
# In Production/Staging, we restrict to our known domains
allowed_hosts = ["localhost", "127.0.0.1", "test", "*.epist.ai"]
if settings.ENVIRONMENT != "development":
    # Add Cloud Run specific host or domain if known
    # For now, allowing all subdomains of epist.ai and the staging URL
    allowed_hosts.append("epist-api-staging-920152096400.us-central1.run.app")
    allowed_hosts.append("epist-api-prod-920152096400.us-central1.run.app")

app.add_middleware(TrustedHostMiddleware, allowed_hosts=allowed_hosts)
