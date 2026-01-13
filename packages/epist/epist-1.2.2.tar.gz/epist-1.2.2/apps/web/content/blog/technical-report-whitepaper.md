---
title: "Technical Report: High-Precision RAG for Audio"
date: "2025-12-06"
description: "An in-depth look at Epist.ai's Tiered Retrieval Architecture, featuring Hybrid Search and Cross-Encoder Reranking."
author: "Epist.ai Engineering"
tags: ["Engineering", "Architecture", "RAG", "Whitepaper"]
coverImage: "https://images.unsplash.com/photo-1550751827-4bd374c3f58b?q=80&w=2670&auto=format&fit=crop"
readTime: "8 min read"
---

Audio content presents unique challenges for Retrieval-Augmented Generation (RAG). Unlike text, audio transcripts lack structural markers (headers, paragraphs) and contain high noise complexity (speaker interruptions, disfluencies). This report details the architecture of **Epist.ai**, a platform designed to solve these challenges through a tiered retrieval strategy utilizing **Semantic Chunking** and **Hybrid Retrieval with Reranking**.

## 1. System Architecture

Epist.ai operates on a modular "RAG Kernel" designed for flexibility and scale.

### 1.1 Ingestion Pipeline
*   **Transcription**: Powered by Fireworks AI (Whisper V3 Turbo), capable of <10s latency for 1hr audio.
*   **Chunking**: `SemanticChunkingStrategy` utilizes embedding distance (Cosine Similarity) between sentences to detect topic shifts.
    *   *Configuration*: Threshold = 95th Percentile (P95).
    *   *Benefit*: Preserves semantic integrity of spoken ideas.

### 1.2 Retrieval Pipeline
We implement a **Tiered Architecture** to balance cost vs. precision.

#### Standard Tier (Speed Optimized)
*   **Method**: Hybrid Search (Vector + Keyword)
*   **Vector Store**: `pgvector` (HNSW Index)
*   **Keyword Search**: BM25 (via `rank-bm25` in-memory or database text search)
*   **Fusion**: Reciprocal Rank Fusion (RRF) with balanced weights (Alpha=0.5).
*   **Latency**: ~50-100ms.

#### Pro Tier (Precision Optimized)
*   **Method**: Hybrid Search + Cross-Encoder Reranking
*   **First Pass**: Retrieves dynamic candidate pool (Top-25) via Hybrid Search.
*   **Second Pass (Reranking)**: Uses `cross-encoder/ms-marco-MiniLM-L-6-v2` to score relevance between Query and Candidate Document.
*   **Benefit**: The Cross-Encoder attends to full query-document interaction, capturing nuance that bi-encoders (vectors) miss.
*   **Latency**: ~300-500ms (Async implementation).

## 2. Experimental Results

We evaluated our pipeline on the "JFK Inaugural" golden dataset.

| Metric | Standard (Hybrid) | Pro (Reranked) | Delta |
| :--- | :--- | :--- | :--- |
| **Recall @ 5** | 0.88 | **0.96** | +9% |
| **Precision @ 3** | 0.75 | **0.92** | +22% |
| **Context Relevancy** | 0.95 | **0.98** | +3% |

*Data based on internal Epist Labs benchmarks.*

### Analysis
The **Pro Tier** significantly improves Precision @ 3. In practice, this means the LLM receives fewer irrelevant chunks, reducing "distraction" and hallucination risk. The Semantic Chunking foundation ensures that even when a chunk is retrieved, it contains a complete thought.

## 3. Deployment & Scalability

The system is deployed on **Google Cloud Run** using a containerized FastAPI backend.
*   **Storage**: Cloud SQL (PostgreSQL 15) for both relational data and Vector Store.
*   **Task Queue**: Cloud Tasks for asynchronous transcription and indexing.
*   **Frontend**: Next.js deployed on Firebase Hosting.

## 4. Conclusion

Epist.ai demonstrates that treating Audio RAG as a distinct discipline—requiring specialized chunking and retrieval strategies—yields significant performance gains over generic RAG pipelines. The introduction of the tiered architecture allows users to choose the right balance of speed and precision for their specific use case.

**[Explore the Pro Tier features in your dashboard](/dashboard).**
