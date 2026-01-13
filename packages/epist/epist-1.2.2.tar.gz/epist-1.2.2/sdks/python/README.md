# Epist Python SDK

The official Python client library for the [Epist.ai](https://epist.ai) Audio RAG Platform.

## 📦 Installation

```bash
pip install epist
```

## 🚀 Quick Start

```python
from epist import Epist
import os

client = Epist(api_key=os.getenv("EPIST_API_KEY"))

# 1. Upload and Transcribe
audio = client.upload_file("meeting.mp3")
print(f"Extraction started: {audio['id']}")

# 2. Ingest entire RSS Feed (Beta)
feed = client.ingest_rss("https://podcast.rss/feed.xml")
print(f"Feed synced: {feed['name']}")

# 2. Hybrid Search
results = client.search("What did we decide on pricing?")
for res in results:
    print(f"[{res['timestamp']}] {res['text']}")

# 3. RAG Chat
chat = client.chat.completions.create(
    messages=[{"role": "user", "content": "Summarize this audio"}]
)
print(chat.choices[0].message.content)
```

## 📖 Documentation

For full API documentation and guides, visit [epist.ai/docs](https://epist.ai/docs).

## 🛡️ License

MIT
