---
title: 'Getting Started with the Epist API: Audio Intelligence for your App'
date: '2025-12-20'
description: 'Learn how to integrate powerful audio intelligence into your applications using the Epist API. This tutorial covers file uploads, URL transcription, status polling, and semantic search.'
author: 'Epist Team'
tags: ['tutorial', 'api', 'python', 'nodejs', 'audio']
---

Welcome to the **Epist API**. This guide shows you how to integrate production-ready audio intelligence into your applications. You'll learn how to upload audio files, transcribe audio from URLs, and perform semantic search over your audio content using our scalable **Audio RAG** platform.

## Verified Capabilities

This guide covers the following core features, all fully verified on our platform:

1.  **File Upload**: High-speed uploads for local audio files (MP3, FLAC, WAV).
2.  **URL Transcription**: Production-grade transcription from public URLs.
3.  **Status Polling**: Real-time progress tracking for large-scale processing.
4.  **Audio RAG & Semantic Search**: Query your processed knowledge base with natural language.

---

## Prerequisites

Before you begin, ensure you have:

*   **Epist API Key**: You need a valid API key (e.g., `sk_live_...`).
*   **Python 3.10+** or **Node.js 18+**.

---

## 1. Python SDK Integration

The Python SDK is the recommended way to interact with Epist. It handles authentication, error handling, and file uploads automatically.

### Installation

Ensure you are using the latest version of the SDK.

```bash
pip install epist
```

### Complete Example

Create a file named `epist_demo.py`. This script demonstrates the full lifecycle: uploading a file, checking its status, and searching the results.

```python
import os
import time
from epist import Epist

# Initialize the client
# Ensure EPIST_API_KEY is set in your environment or passed explicitly
client = Epist(api_key="YOUR_API_KEY")

def main():
    # --- 1. Upload a Local File ---
    print("\n[1] Uploading 'interview.mp3'...")
    try:
        # Uploads are synchronous but processing is asynchronous
        upload_res = client.upload_file("interview.mp3")
        task_id = upload_res["id"]
        print(f"Upload successful. Task ID: {task_id}")
    except Exception as e:
        print(f"Upload failed: {e}")
        return

    # --- 2. Poll for Completion ---
    # We must wait for the audio to be processed before we can search it.
    print(f"\n[2] Polling status for task: {task_id}")
    while True:
        status_res = client.get_status(task_id)
        status = status_res.get("status")
        print(f"Status: {status}")
        
        if status == "completed":
            print("Processing complete!")
            break
        elif status == "failed":
            print(f"Task failed: {status_res.get('error')}")
            return
        
        time.sleep(2)

    # --- 3. Semantic Search ---
    # Now that the file is indexed, we can ask questions about it.
    query = "What was discussed about the roadmap?"
    print(f"\n[3] Searching knowledge base for: '{query}'")
    
    search_res = client.search(query=query, limit=3)
    
    for idx, item in enumerate(search_res, 1):
        print(f"\nResult {idx}:")
        print(f"Text: {item.get('text', '')[:150]}...")
        print(f"Score: {item.get('score')}")

if __name__ == "__main__":
    main()
```

---

## 2. Node.js Integration

For Node.js applications, use the `epist` package to interact with the API.

### Installation

```bash
npm install epist
```

### Complete Example

Create a file named `epist_demo.js`.

```javascript
const { Epist } = require('epist');

// Initialize the client
const client = new Epist({ 
    apiKey: "YOUR_API_KEY",
    // Default: https://api.epist.ai/api/v1
});

async function main() {
    // --- 1. Transcribe from URL ---
    const audioUrl = "https://storage.googleapis.com/cloud-samples-data/speech/brooklyn_bridge.flac";
    console.log(`\n[1] Transcribing URL: ${audioUrl}`);

    try {
        const urlRes = await client.transcribeUrl(audioUrl, true);
        const taskId = urlRes.id;
        console.log(`Task started. ID: ${taskId}`);

        // --- 2. Poll Status ---
        await pollStatus(client, taskId);

        // --- 3. Search ---
        const query = "How old is the bridge?";
        console.log(`\n[3] Searching for: '${query}'`);
        const searchRes = await client.search(query, 1);
        
        searchRes.forEach(result => {
             console.log(`\nAnswer: ${result.text}`);
        });

    } catch (error) {
        console.error("Error:", error.message);
    }
}

async function pollStatus(client, id) {
    while (true) {
        const res = await client.getStatus(id);
        const status = res.status;
        console.log(`Status: ${status}`);
        
        if (status === 'completed' || status === 'failed') break;
        await new Promise(r => setTimeout(r, 2000));
    }
}

main();
```

---

## Common Pitfalls & Best Practices

1.  **Valid Audio URLs**: When using `transcribe_url`, ensure the URL is publicly accessible and points to a valid media file. Invalid domains (like `NxDomain`) will result in a `failed` task status.
2.  **Status Polling**: Transcription is asynchronous. Always poll the `/audio/{id}` endpoint until the status is `completed` before attempting to retrieve transcripts or search.
3.  **File Upload Headers**: If using raw HTTP calls for uploads, let your HTTP library (like `requests` or `axios`) handle the `Content-Type` header processing. Manually setting `application/json` on a multipart upload will cause `422 Unprocessable Entity` errors.

## Need Help?

Check out our full SDK documentation or reach out to support if you encounter persistent issues. **Ready to integrate audio intelligence? [Get your API key and start building today](/dashboard).** Happy coding!
