---
title: API Reference
description: Detailed documentation for the Epist.ai REST API.
---

# API Reference

The Epist.ai API is RESTful and uses standard HTTP methods and status codes.

> [!TIP]
> **Interactive Swagger UI**: Explore and test the API directly at [api.epist.ai/docs](https://api.epist.ai/docs).

## Authentication

All requests must include your API Key in the `X-API-Key` header.

```bash
curl -H "X-API-Key: your_api_key_here" https://api.epist.ai/api/v1/...
```

---

## 🎙️ Audio Ingestion

Endpoints for uploading and processing audio/video content.

### [POST] /v1/audio/upload
Upload a file directly. Supported formats: `.mp3`, `.wav`, `.m4a`, `.mp4`, `.mov`.

- **Content-Type**: `multipart/form-data`
- **Body**:
    - `file`: (Binary) The audio/video file.
- **Response** (202 Accepted):
    ```json
    {
      "id": "uuid",
      "status": "processing",
      "filename": "meeting.mp3"
    }
    ```

### [POST] /v1/audio/transcribe_url
Ingest content from a public URL.

- **Body**:
    ```json
    {
      "audio_url": "https://example.com/podcast.mp3",
      "rag_enabled": true
    }
    ```

---

## 🔍 Retrieval (RAG)

Connect your data to your applications using semantic search.

### [POST] /v1/search/
Perform a hybrid search (Vector + Keyword).

- **Body**:
    ```json
    {
      "query": "What did they say about Q4 projections?",
      "limit": 10,
      "rerank_model": "cross-encoder/ms-marco-MiniLM-L-6-v2"
    }
    ```
- **Response**: List of `SearchResponseItem` including text snippets, timestamps, and scores.

### [POST] /v1/chat/completions
OpenAI-compatible endpoint for RAG-powered chat.

- **Body**:
    ```json
    {
      "messages": [{"role": "user", "content": "Summary of the audio."}],
      "stream": false
    }
    ```
- **Response**: Standard Chat Completion object with a `citations` array.

---

## 🔗 Connectors & Feeds

Automate your knowledge ingestion.

### [POST] /v1/connectors/feeds
Add an RSS/Podcast feed for automated sync.

- **Parameters**: `url`, `name`, `refresh_interval_minutes`.
- **Response**: `PodcastFeed` object.

---

## 📊 Management & Logs

### [GET] /v1/stats/
Get system-wide usage statistics (total audio files, transcripts, etc.).

### [GET] /v1/logs/
Retrieve detailed request logs for debugging and observability.

### [GET] /v1/traces/
Access "Glass Box" traces to see exact retrieval and reranking steps.

---

## ⚠️ Error Handling

| Code | Meaning | Resolution |
| :--- | :--- | :--- |
| `200` | OK | Success. |
| `202` | Accepted | Upload successful, processing started. |
| `401` | Unauthorized | Check your `X-API-Key`. |
| `429` | Too Many Requests | Rate limit hit. Check your plan limits. |
| `500` | Server Error | Contact [support@epist.ai](mailto:support@epist.ai). |
