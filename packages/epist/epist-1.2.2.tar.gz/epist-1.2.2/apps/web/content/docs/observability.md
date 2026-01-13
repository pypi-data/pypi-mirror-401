---
title: Observability & Tracing
description: Full transparency into your RAG pipeline.
---

# Observability & Tracing

The platform includes a built-in observability system (**"The Glass Box"**) that provides full transparency into the execution of your RAG pipelines.

## 📊 Overview

Instead of relies on unstructured logs, the system emits structured **Trace Events**. A "Trace" represents a single user interaction, containing multiple **Spans** for each step:
- **Retrieval**: Vector and Keyword search execution.
- **Reranking**: Scoring and re-ordering results.
- **Generation**: LLM prompt and completion details.

## 🔍 "Glass Box" Features

-   **Waterfall View**: Visualize the exact sequence and latency of every pipeline step.
-   **Trace Explorer**: Search and filter traces by component, status, or date in the [Dashboard](https://api.epist.ai/dashboard/traces).
-   **Debugging**: Inspect internal system prompts and raw retrieval results.

## 🛠️ Traces API

Access trace data programmatically for external analysis:

### List Traces
`GET /api/v1/traces`
- **Parameters**: `limit`, `offset`, `trace_id`, `component`.

### Get Trace Details
`GET /api/v1/traces/{trace_id}`
- **Returns**: Waterfall of all spans for that trace.

---

## 💻 Manual Instrumentation

If you're extending the platform, you can add custom tracing using the `trace_service`:

```python
from services.trace import trace_service

async def my_rag_logic(query):
    async with trace_service.span("My Step", component="CustomService") as span:
        # Business logic here
        result = await do_work(query)
        span.set_output(result)
        return result
```

> [!TIP]
> Tracing is enabled by default in production. In development, logs are also mirrored to the terminal for convenience.
## External Observability (Sentry)

For error tracking and performance monitoring, the platform integrates with **Sentry**.

### Configuration

### Features
- **Error Tracking**: Global exception handling in FastAPI.
- **Performance**: Transaction tracing for specific API endpoints.
- **Alerting**: Real-time notifications for production errors.
