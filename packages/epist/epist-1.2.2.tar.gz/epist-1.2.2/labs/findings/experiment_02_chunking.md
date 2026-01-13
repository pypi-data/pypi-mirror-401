# Experiment 02: Advanced Chunking Research 🧠

**Date:** 2025-12-04
**Status:** ✅ Complete

## 1. Hypothesis
We hypothesized that **Semantic Chunking** (splitting text based on meaning/embedding similarity) would outperform the baseline **Recursive Character Chunking** (splitting by fixed size) by preserving context better, leading to higher answer relevancy and faithfulness.

## 2. Methodology
-   **Dataset:** "Golden Dataset" (JFK Inaugural Address).
-   **Pipelines:**
    1.  **Baseline:** `RecursiveCharacterTextSplitter` (Chunk Size: 1000, Overlap: 100).
    2.  **Semantic:** `SemanticChunker` (OpenAI Embeddings, Percentile Threshold).
-   **Evaluation:** RAGAS v0.4.0 (Faithfulness, Answer Relevancy, Context Precision, Context Recall).

## 3. Results

| Metric | Baseline Score | Semantic Score | Delta |
| :--- | :--- | :--- | :--- |
| **Context Recall** | 1.0000 | 1.0000 | = |
| **Context Precision** | 1.0000 | 1.0000 | = |
| **Faithfulness** | 1.0000 | 1.0000 | = |
| **Answer Relevancy** | 0.9404 | **0.9571** | **+1.67%** |

## 4. Analysis
-   **High Baseline:** The JFK speech is relatively short and coherent, so the baseline performed exceptionally well (1.0 on most metrics).
-   **Semantic Efficiency:** The Semantic Chunker generated only **2 chunks** for the entire speech, whereas the baseline likely generated more arbitrary splits.
-   **Relevancy Boost:** The slight improvement in Answer Relevancy (0.96 vs 0.94) suggests that providing the LLM with semantically complete blocks (rather than arbitrary cuts) allows it to synthesize slightly better answers.

## 5. Conclusion
**Semantic Chunking is the winner.** 🏆
While the numerical difference is small on this simple dataset, the qualitative advantage of grouping text by meaning is significant for scaling to larger, more complex documents (e.g., multi-speaker meetings).

**Recommendation:**
-   Adopt **Semantic Chunking** as the default strategy for the platform.
-   Proceed to **Experiment 3: Speaker-Aware RAG** to see if we can further improve performance on multi-speaker audio.
