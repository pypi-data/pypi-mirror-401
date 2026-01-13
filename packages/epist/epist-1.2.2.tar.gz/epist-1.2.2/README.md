# Epist.ai Audio RAG Platform

[![PyPI](https://img.shields.io/pypi/v/epist-mcp-server?color=blue&label=MCP%20Server)](https://pypi.org/project/epist-mcp-server/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

> [!TIP]
> **"Read" your audio.** Transform podcasts, meetings, and voice notes into a queryable Second Brain with RAG.

---

### 🔗 Quick Links
- [Documentation Site](https://epist.ai/docs)
- [Quick Start Guide](./docs/quickstart.md)
- [API Reference](./docs/api_reference.md)
- [MCP Guide](./README_MCP.md)
- [Contributing](./CONTRIBUTING.md)

---

## 🚀 **New: Model Context Protocol (MCP)**
Connect **Claude Desktop** directly to your knowledge base using our official MCP Server:
```bash
pip install epist-mcp-server
```
[Read the MCP Guide →](./README_MCP.md)

## Introduction

Epist.ai is a next-generation system that treats **audio as a first-class citizen**, enabling seamless ingestion, understanding, and retrieval of information from meetings, voice notes, and ambient conversations.

It provides a production-ready API for audio ingestion, transcription, and semantic search, built on modern RAG (Retrieval-Augmented Generation) principles.

## 🧠 Core Concepts

### The Audio RAG Pipeline
1.  **Ingestion**: Audio/Video files are streamed to GCS.
2.  **Transcription**: Fireworks AI (Whisper V3 Turbo) generates high-fidelity transcripts with speaker diarization.
3.  **Semantic Chunking**: Transcripts are intelligently split to preserve context.
4.  **Vectorization**: Text chunks are converted to embeddings using OpenAI's `text-embedding-3-small`.
5.  **Hybrid Retrieval**: Search combines BM25 keyword matching with Vector similarity for maximum precision.

### Platform vs. Tenant
-   **Platform (This Repo)**: The core engine providing the API, storage, and processing logic.
-   **Tenant (External)**: Applications like [podcast-rag-app](https://github.com/Seifollahi/podcast-rag-app) that consume the API to provide specific user experiences.

## Features

-   **Audio Upload**: Stream large audio files directly to Google Cloud Storage.
-   **RSS Ingestion**: Ingest entire podcast feeds automatically with metadata extraction.
-   **Automatic Transcription**: Background transcription with speaker diarization.
-   **Hybrid Search**: Combine semantic meaning (Vector) and exact keywords (Full-Text) using Reciprocal Rank Fusion (RRF).
-   **Multi-Modal Support**: Support for `.mp4`, `.mov`, `.mp3`, `.wav`.
-   **📊 Observability**: "Glass Box" tracing system to visualize every pipeline step.
-   **💬 Interactive Chat**: Chat with your audio content using citations that link directly to timestamps.
-   **MCP Integration**: Connect your audio knowledge base directly to Claude.

## Tech Stack

-   **Backend:** FastAPI (Python 3.11+)
-   **Database:** PostgreSQL 15 + `pgvector`
-   **ASR:** Fireworks AI (Whisper V3 Turbo)
-   **Embeddings:** OpenAI `text-embedding-3-small`
-   **RAG Framework:** LangChain
-   **Infrastructure:** GCP (Cloud Run, Cloud SQL, Cloud Storage, Cloud Tasks)
-   **Frontend:** Next.js 15 (React)

## Quick Start

This project uses `uv` for dependency management.

```bash
# Install dependencies
uv sync

# Run development server
uv run fastapi dev src/main.py
```

### Frontend Development

```bash
cd apps/web
npm install
npm run dev
```

## Project Structure

| Directory | Description |
| :--- | :--- |
| `src/` | **Core Backend API**: FastAPI application, services, and models. |
| `apps/web/` | **Main Dashboard**: Next.js 15 application for managing audio and search. |
| `packages/` | **Internal Packages**: Includes `epist_cli` and `epist_mcp_server`. |
| `sdks/` | **Client Libraries**: Official SDKs for JS/TS and Python. |
| `infra/` | **Infrastructure**: Terraform configurations for GCP deployment. |
| `docs/` | **Documentation**: Deep-dive guides and API references. |
| `labs/` | **Research**: Experimental notebooks and chunking evaluations. |

## Changelog

### v1.2.0 (Jan 05, 2026)
- **RSS Ingestion**: New generic platform feature to ingest entire podcast feeds.
- **Enhanced Metadata**: Automated extraction of author, description, and images.

### v1.1.0 (Dec 27, 2025)
- **Stability & Observability**: Integrated **Sentry** and migrated to **Cloud Scheduler**.
- **Security & Performance**: Added TrustedHost, GZip, and production security headers.
- **Tiered Sync**: Automated feed synchronization with tier-based refresh intervals.

### v0.1.0 (Dec 08, 2025)
- **Core Platform**: Initial release with Audio RAG and Vector Search.

## Contributing

We welcome contributions! Please see our [Contributing Guide](./CONTRIBUTING.md) for more information.

## License

This project is open source under the MIT License.

## Support

If you have questions or need assistance, please contact us at [admin@epist.ai](mailto:admin@epist.ai).

---

**Epist.ai** - Transforming audio into actionable knowledge.
