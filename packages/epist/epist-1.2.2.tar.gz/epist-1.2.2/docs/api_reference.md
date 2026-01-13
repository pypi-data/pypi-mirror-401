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
      "rag_enabled": true,
      "webhook_url": "https://your-app.com/webhooks/epist"
    }
    ```
- **Response** (201 Created):
    ```json
    {
      "id": "uuid",
      "status": "pending",
      "title": "podcast.mp3",
      "transcript": null,
      "summary": null,
      "entities": null
    }
    ```
- **Note**: If the content has already been processed (cached), the status will be `completed` and the fields `transcript`, `summary`, and `entities` will be populated immediately. In both cases, a webhook will be sent to the provided `webhook_url` upon final resolution.

---

## ⚡ Ingestion (Beta)

Generic tools for high-volume content sourcing.

### [POST] /v1/ingest/rss
Ingest an entire podcast or blog RSS feed. 
Automatically extracts metadata and triggers transcription for all discovered media.

- **Body**:
    ```json
    {
      "url": "https://podcast.rss/feed.xml",
      "name": "My Favorite Podcast",
      "refresh_interval_minutes": 1440,
      "max_episodes": 10,
      "start_date": "2024-01-01T00:00:00",
      "include_keywords": "AI, agents",
      "exclude_keywords": "politics, news"
    }
    ```
- **Response** (201 Created):
    ```json
    {
      "id": "uuid",
      "name": "My Favorite Podcast",
      "status": "ingestion_started"
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
