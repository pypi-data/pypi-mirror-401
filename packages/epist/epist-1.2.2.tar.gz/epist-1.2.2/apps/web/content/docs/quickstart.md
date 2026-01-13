---
title: Quickstart Guide
description: Get up and running with Epist.ai in under 5 minutes.
---

# Quickstart Guide

Welcome to Epist.ai! This guide will help you get started with the platform, from authentication to performing your first search.

## 📋 Prerequisites

Before you begin, ensure you have:
- An **API Key** from the [Dashboard](https://epist.ai/dashboard/settings).
- `curl` or a modern programming environment (Python/Node.js).

---

## 🚀 Step 1: Authentication

All API requests require an `X-API-Key` header.

```bash
export EPIST_API_KEY="sk_live_YOUR_KEY_HERE"
```

> [!IMPORTANT]
> Keep your API key secret. Never commit it to version control.

---

## 📤 Step 2: Upload Your First Audio

You can upload files (`.mp3`, `.wav`, `.m4a`, etc.) directly to our ingestion engine.

```bash
curl -X POST "https://api.epist.ai/api/v1/audio/upload" \
     -H "X-API-Key: $EPIST_API_KEY" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@/path/to/your/audio.mp3"
```

**Response:**
```json
{
  "id": "7f8e9a...",
  "status": "processing",
  "filename": "audio.mp3"
}
```

---

## 🔍 Step 3: Perform a Hybrid Search

Once processing is complete, you can search across your knowledge base using semantic and keyword matching.

```bash
curl -X POST "https://api.epist.ai/api/v1/search/" \
     -H "X-API-Key: $EPIST_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
       "query": "What are the core features?",
       "limit": 5
     }'
```

---

## 💬 Step 4: Use the Chat API (RAG)

Chat with your audio content using a GPT-style interface with automatic citations.

```bash
curl -X POST "https://api.epist.ai/api/v1/chat/completions" \
     -H "X-API-Key: $EPIST_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
       "messages": [{"role": "user", "content": "Summarize the latest meeting."}]
     }'
```

---

## 📦 Official SDKs

For a better developer experience, use our official client libraries:

| Platform | Package | Install Command |
| :--- | :--- | :--- |
| **JavaScript/TS** | `epist` | `npm install epist` |
| **Python** | `epist` | `pip install epist` |
| **CLI** | `epist-cli` | `pip install epist-cli` |

---

## 🧱 Local Development

If you are a contributor looking to run the platform locally:

```bash
# 1. Clone the repo
git clone https://github.com/Seifollahi/audio_rag_platform.git
cd audio_rag_platform

# 2. Install dependencies (requires 'uv')
uv sync

# 3. Run the API
uv run fastapi dev src/main.py
```

> [!TIP]
> Check the [Contributing Guide](https://github.com/Seifollahi/audio_rag_platform/blob/main/CONTRIBUTING.md) for detailed development standards.

## ⏭️ Next Steps

-   **Explore the [API Reference](api-reference)**: Dive deep into every endpoint.
-   **Setup [Integrations](integrations)**: Connect RSS feeds and podcasts.
-   **MCP Integration**: Use the [Model Context Protocol](mcp-architecture) to connect Claude to your data.
