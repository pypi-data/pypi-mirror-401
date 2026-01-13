# Epist JavaScript SDK

The official JavaScript/TypeScript client library for the [Epist.ai](https://epist.ai) Audio RAG Platform.

## 📦 Installation

```bash
npm install epist
# or
yarn add epist
```

## 🚀 Quick Start

```typescript
import { Epist } from 'epist';

const client = new Epist({
  apiKey: process.env.EPIST_API_KEY,
});

// 1. Upload and Transcribe
const audio = await client.uploadFile(file);
console.log(`Processing: ${audio.id}`);

// 2. Ingest entire RSS Feed (Beta)
const feed = await client.ingestRss("https://podcast.rss/feed.xml");
console.log(`Feed synced: ${feed.name}`);

// 2. Semantic Search
const results = await client.search('What were the key takeaways?');
results.forEach(res => {
  console.log(`[${res.timestamp}] ${res.text}`);
});

// 3. RAG Chat
const chat = await client.chat.completions.create({
  messages: [{ role: 'user', content: 'Summarize the audio' }],
});
console.log(chat.choices[0].message.content);
```

## 📖 Documentation

For full API documentation and guides, visit [epist.ai/docs](https://epist.ai/docs).

## 🛡️ License

MIT
