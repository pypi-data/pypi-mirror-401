# Epist MCP Server ('Epist Connect')

Connect [Claude Desktop](https://claude.ai/download) to your Epist.ai Audio Knowledge Base.

## Installation

### Option 1: Install from PyPI (Recommended)

```bash
pip install epist-mcp-server
```

### Option 2: Install from Source

```bash
cd packages/epist_mcp_server
pip install .
```

## Configuration

Add this to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "epist": {
      "command": "epist-mcp",
      "env": {
        "EPIST_API_KEY": "sk_live_...",
        "EPIST_API_URL": "https://api.epist.ai/api/v1"
      }
    }
  }
}
```

## Features

- **Ingest Audio**: "Ingest this podcast: https://..."
- **Search**: "Search my transcripts for..."
- **Read**: "Read transcript for ID 123"
