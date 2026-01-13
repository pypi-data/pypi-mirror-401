# Epist MCP Server

The official [Model Context Protocol (MCP)](https://modelcontextprotocol.io) server for Epist.ai. This allows you to connect AI assistants like **Claude Desktop** directly to your Audio Knowledge Base.

## 📦 Installation

```bash
pip install epist-mcp-server
```

## ⚙️ Configuration

Add the following to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "epist": {
      "command": "epist-mcp",
      "env": {
        "EPIST_API_KEY": "sk_live_YOUR_KEY_HERE"
      }
    }
  }
}
```

## 🛠️ Available Tools

- `search_audio`: Semantically search your transcription knowledge base.
- `ingest_url`: Submit a public audio URL for background transcription and indexing.
- `get_task_status`: Check the progress of current transcription jobs.

## 📚 Resources

The server exposes transcripts as MCP resources:
- `transcript://{audio_id}`: Read the full text and segments of a specific transcript.

## 📖 Further Reading

- [Epist Documentation](https://epist.ai/docs)
- [Official MCP Specification](https://modelcontextprotocol.io/introduction)
