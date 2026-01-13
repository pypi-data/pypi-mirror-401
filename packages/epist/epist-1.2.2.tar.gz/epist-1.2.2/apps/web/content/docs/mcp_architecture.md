---
title: MCP Architecture
description: Connect Claude Desktop to your Audio Knowledge Base.
---

# MCP Architecture

The **Model Context Protocol (MCP)** server is the primary interface for AI assistants (like Claude) to interact with your Audio Knowledge Base.

## 🛠️ Available Tools

### 1. `search_audio`
Semantically search your transcription knowledge base.
- **Arguments**: `query` (string), `limit` (int).
- **Returns**: List of matching segments with timestamps and sources.

### 2. `ingest_url`
Submit a public audio URL for background transcription and indexing.
- **Arguments**: `url` (string).
- **Returns**: Confirmation and Task ID.

### 3. `get_task_status`
Monitor the progress of a transcription job.
- **Arguments**: `audio_id` (uuid).
- **Returns**: Current status (`queued`, `processing`, `completed`).

## 📚 Resources

The server exposes transcripts as MCP resources:
- `transcript://{audio_id}`: Access the full raw transcript of a processed audio file.

## 🛡️ Security & Auth

The MCP server uses standard `X-API-Key` authentication. For local use with Claude Desktop, the key is passed via environment variables in the config file.

> [!TIP]
> Always use a dedicated API key for your MCP integration to track usage independently in the dashboard.
