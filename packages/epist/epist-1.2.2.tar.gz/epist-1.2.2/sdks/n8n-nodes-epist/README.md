# n8n-nodes-epist

This is an n8n community node to interact with [Epist.ai](https://epist.ai), an Audio RAG (Retrieval-Augmented Generation) platform.

## Installation

Follow the [installation guide](https://docs.n8n.io/integrations/community-nodes/installation/) in the n8n documentation to install this node.

Package name on npm: `n8n-nodes-epist`

## Operations

### Audio
*   **Transcribe URL**: Send a public URL of an audio file to be transcribed and ingested into your RAG knowledge base.
*   **Upload**: Upload an audio file directly from n8n binary data.
*   **Get Status**: Check the status and retrieve results for a specific audio ID.
*   **Delete**: Permanently delete an audio resource and its associated data.

### Search
*   **Query**: Perform hybrid search (semantic + keyword) across your transcribed audio collections.

## Credentials

You will need an API Key from your Epist.ai dashboard.
1. Log in to [Epist.ai](https://epist.ai).
2. Go to Settings -> API Keys.
3. Generate a new key and paste it into the n8n credentials.
