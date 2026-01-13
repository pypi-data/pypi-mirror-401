# Use the pre-built base image with heavy dependencies
FROM us-central1-docker.pkg.dev/audiointelligence-3cb34/epist-repo/api-base:latest as builder

WORKDIR /app

# Copy project files
COPY pyproject.toml README.md ./

# Install dependencies WITHOUT using lockfile to avoid CUDA packages
# This prevents the disk space issue from downloading 2.5GB of CUDA libraries
RUN --mount=type=cache,target=/root/.cache/uv \
    uv pip install \
    "torch>=2.2.0" \
    "torchaudio>=2.2.0" \
    "torchvision>=0.17.0" \
    --index-url https://download.pytorch.org/whl/cpu && \
    uv pip install -e ".[audio-rag]" --no-deps && \
    uv pip install \
    langchain langchain-core langchain-community langchain-openai langchain-experimental langchain-text-splitters \
    langgraph langgraph-checkpoint langsmith \
    chromadb pgvector sentence-transformers \
    fastapi uvicorn httpx pydantic pydantic-settings python-multipart \
    sqlalchemy sqlmodel asyncpg alembic greenlet tenacity \
    librosa audioread soundfile soxr numpy scipy pandas moviepy pydub \
    transformers datasets huggingface-hub tiktoken openai fireworks-ai rank-bm25 \
    firebase-admin authlib python-jose pyjwt cryptography \
    stripe sentry-sdk prometheus-client slowapi \
    google-cloud-storage google-cloud-tasks \
    mcp feedparser apscheduler \
    ragas arize-phoenix opentelemetry-api opentelemetry-sdk \
    python-dotenv pyyaml aiohttp httptools uvloop \
    --extra-index-url https://pypi.org/simple

# Runtime stage
FROM us-central1-docker.pkg.dev/audiointelligence-3cb34/epist-repo/api-base:latest

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/app/.venv/bin:$PATH" \
    PYTHONPATH="/app/src" \
    HF_HOME="/app/.cache" \
    PORT=8080

WORKDIR /app

# Copy virtual environment from builder (updates the base venv with new deps)
COPY --from=builder /app/.venv /app/.venv

# Copy application code
COPY src/ ./src/
COPY alembic.ini .
COPY migrations/ ./migrations/

# Copy scripts
COPY scripts/ ./scripts/
RUN chmod +x ./scripts/start.sh

# Pre-download Reranking model to bake it into the image
RUN python -c 'from sentence_transformers import CrossEncoder; CrossEncoder("cross-encoder/ms-marco-TinyBERT-L-2-v2")'

# Create a non-root user for security (Cloud Run best practice)
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Expose the port (Cloud Run expects 8080 by default)
EXPOSE 8080

# Start the application
CMD ["./scripts/start.sh"]
