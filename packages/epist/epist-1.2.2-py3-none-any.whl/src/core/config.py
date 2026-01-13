from typing import Any

from pydantic import PostgresDsn, ValidationInfo, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "Epist.ai"
    API_V1_STR: str = "/api/v1"

    # Database
    DB_USER: str = "epist_user"
    DB_PASSWORD: str | None = None
    DB_HOST: str | None = None
    DB_NAME: str = "epist"
    DATABASE_URL: str | None = None
    DB_POOL_SIZE: int = 5
    DB_MAX_OVERFLOW: int = 10

    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def assemble_db_connection(cls, v: str | None, info: ValidationInfo) -> Any:
        if isinstance(v, str):
            return v

        # If DATABASE_URL is not provided, try to build it
        values = info.data
        if values.get("DB_PASSWORD") and values.get("DB_HOST"):
            db_host = str(values.get("DB_HOST"))
            if db_host.startswith("/"):
                # Handle Cloud SQL Unix socket
                # asyncpg requires the host to be the directory containing the socket
                # and the host part of the URL to be empty or point to that directory.
                # We construct the URL manually to ensure correct format for asyncpg + sockets.
                from urllib.parse import quote_plus

                password = quote_plus(str(values.get("DB_PASSWORD")))
                user = quote_plus(str(values.get("DB_USER")))
                db_name = values.get("DB_NAME")
                return f"postgresql+asyncpg://{user}:{password}@/{db_name}?host={db_host}"
            else:
                return str(
                    PostgresDsn.build(
                        scheme="postgresql+asyncpg",
                        username=values.get("DB_USER"),
                        password=values.get("DB_PASSWORD"),
                        host=db_host,
                        path=values.get("DB_NAME"),
                    )
                )

        # Fallback for local dev if nothing is set
        return "postgresql+asyncpg://postgres:postgres@localhost:5432/epist"

    # Security
    SECRET_KEY: str
    MASTER_API_KEY: str | None = None
    API_KEY: str

    @field_validator("API_KEY", mode="before")
    @classmethod
    def set_api_key(cls, v: str, info: ValidationInfo) -> str:
        # If MASTER_API_KEY is provided, it overrides API_KEY
        master_key = info.data.get("MASTER_API_KEY")
        if master_key:
            return master_key
        return v

    # Infrastructure
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "INFO"
    SENTRY_DSN: str | None = None
    GCS_BUCKET_NAME: str = "epist-audio-raw"
    SENTRY_WEBHOOK_SECRET: str | None = None
    GITHUB_TOKEN: str | None = None
    GITHUB_REPO: str = "mo-seifollahi/audio_rag_platform"

    @field_validator("GCS_BUCKET_NAME", mode="before")
    @classmethod
    def set_gcs_bucket_name(cls, v: str, info: ValidationInfo) -> str:
        if v and v != "epist-audio-raw":
            return v

        env = info.data.get("ENVIRONMENT", "development")
        if env == "staging":
            return "epist-content-staging-audiointelligence-3cb34"
        elif env == "prod":
            return "epist-content-prod-audiointelligence-3cb34"
        return "epist-audio-raw"

    CLOUD_TASKS_QUEUE_PATH: str = "projects/audiointelligence-3cb34/locations/us-central1/queues/transcription-queue-v3"
    SERVICE_ACCOUNT_EMAIL: str = "920152096400-compute@developer.gserviceaccount.com"
    API_BASE_URL: str = "http://localhost:8000"

    @field_validator("API_BASE_URL", mode="before")
    @classmethod
    def set_api_base_url(cls, v: str, info: ValidationInfo) -> str:
        if v and v != "http://localhost:8000":
            return v

        env = info.data.get("ENVIRONMENT", "development")
        if env == "staging":
            return "https://epist-api-staging-920152096400.us-central1.run.app"
        elif env == "prod":
            return "https://epist-api-prod-920152096400.us-central1.run.app"
        return "http://localhost:8000"

    FRONTEND_URL: str = "http://localhost:3000"

    @field_validator("FRONTEND_URL", mode="before")
    @classmethod
    def set_frontend_url(cls, v: str, info: ValidationInfo) -> str:
        if v and v != "http://localhost:3000":
            return v

        env = info.data.get("ENVIRONMENT", "development")
        if env == "staging":
            return "https://epist-staging.web.app"
        elif env == "prod":
            return "https://epist.web.app"
        return "http://localhost:3000"

    # AI Providers
    OPENAI_API_KEY: str = ""
    FIREWORKS_API_KEY: str = ""
    FIREWORKS_PROXY_URL: str | None = None  # Format: http://user:pass@host:port
    HF_TOKEN: str | None = None

    # Search Configuration
    DEFAULT_RRF_K: int = 60
    DEFAULT_RERANK_MODEL: str = "cross-encoder/ms-marco-TinyBERT-L-2-v2"
    RERANK_PROVIDER: str = "api"  # "local" or "api"
    FIREWORKS_RERANK_MODEL: str = "fireworks/qwen3-reranker-8b"

    # Stripe
    STRIPE_SECRET_KEY: str = ""
    STRIPE_PUBLISHABLE_KEY: str = ""
    STRIPE_WEBHOOK_SECRET: str = ""
    STRIPE_PRICE_ID_PRO: str = ""
    STRIPE_PRICE_ID_STARTER: str = ""

    # CORS
    BACKEND_CORS_ORIGINS: list[str] = [
        "http://localhost:3000",
        "https://epist.ai",
        "https://www.epist.ai",
        "https://epist.web.app",
        "https://audiointelligence-3cb34.web.app",
        "https://epist-ai-staging.web.app",
        "https://epist-staging.web.app",
    ]

    # Regex for Firebase apps
    CORS_ORIGIN_REGEX: str = r"https://.*\.web\.app"

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True, extra="ignore")


try:
    settings = Settings()
except Exception as e:
    import sys

    sys.stderr.write(f"CRITICAL: Failed to load configuration: {e}\n")
    # We might want to re-raise or exit, but printing to stderr is crucial for Cloud Run logs
    raise e
