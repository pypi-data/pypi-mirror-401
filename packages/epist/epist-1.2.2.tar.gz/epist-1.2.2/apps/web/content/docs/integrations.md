---
title: Integrations Guide
description: Connect Epist.ai to your automation stack.
---

# Integrations Guide

This guide explains how to connect Epist.ai to automation platforms like n8n, Zapier, Make, and Pipedream.

## Prerequisites

To integrate Epist.ai with external tools, you need:
- An **Epist Account**.
- A valid **API Key** from the [Dashboard](https://epist.ai/dashboard/settings).

---

## 1. Authentication

Epist.ai uses API Key authentication via the request header.

> [!IMPORTANT]
> **Header Name:** `X-API-Key`
> **Value:** `YOUR_API_KEY`

### Example (cURL)
```bash
curl -X 'GET' 'https://api.epist.ai/api/v1/stats/' \
  -H 'X-API-Key: sk_live_...'
```

---

## 2. n8n Integration

Since Epist is OpenAPI compliant, you can integrate it into n8n using the HTTP Request node.

### Using HTTP Request Node
1.  Create an **HTTP Request** node.
2.  **Authentication**: Select "Generic Credential Type" -> "Header Auth".
3.  **Name**: `X-API-Key`
4.  **Value**: `[YOUR_API_KEY]`
5.  **URL**: `https://api.epist.ai/api/v1/audio/transcribe_url`
6.  **Method**: `POST`

---

## 3. Zapier Integration

You can connect to Epist using Zapier's "Webhooks by Zapier".

### Using Webhooks by Zapier
1.  Choose **Webhooks by Zapier** app.
2.  Event: **Custom Request**.
3.  **Method**: `POST`
4.  **URL**: `https://api.epist.ai/api/v1/search/`
5.  **Headers**:
    *   `X-API-Key`: `[YOUR_API_KEY]`
    *   `Content-Type`: `application/json`

---

## 4. OpenAPI Specification

For platforms that support importing OpenAPI specs:

**Spec URL:** `https://api.epist.ai/api/v1/openapi.json`
