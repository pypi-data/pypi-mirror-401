# Experiment 01: Baseline Performance 📊

**Date:** 2025-12-04
**Status:** ✅ Complete

## 1. Hypothesis
We established a baseline for the current "Audio RAG" system to understand its performance before applying advanced optimizations (chunking, re-ranking, etc.).
**Hypothesis:** The current system (simple chunking + vector search) will perform well on simple, distinct queries but may struggle with synthesis or nuance.

## 2. Methodology
-   **Dataset:** "Golden Dataset" (5 QA pairs) derived from JFK's Inaugural Address (`jfk.wav`).
-   **Audio Source:** Real audio file (352KB WAV), transcribed via Fireworks (Whisper V3).
-   **Evaluation Framework:** RAGAS (Retrieval Augmented Generation Assessment) v0.4.0.
-   **Model:** GPT-4o (for evaluation).
-   **Environment:** Staging Cloud Environment (`epist-api-staging...`).

## 3. Results

| Metric | Score | Description |
| :--- | :--- | :--- |
| **Context Recall** | **1.0000** | The retrieval system found *all* relevant information. |
| **Context Precision** | **1.0000** | The retrieved chunks were *highly* relevant (little noise). |
| **Faithfulness** | **0.8000** | The answers were mostly grounded in the context, with slight hallucinations or external knowledge usage. |
| **Answer Relevancy** | **0.7146** | The answers directly addressed the user's question, though there is room for improvement in conciseness or style. |

## 4. Analysis
-   **Retrieval is Perfect (for this sample):** A score of 1.0 for both Precision and Recall indicates that for this specific, short speech, the simple chunking strategy worked perfectly. The distinct vocabulary of the JFK speech likely helped.
-   **Generation needs Tuning:** Faithfulness (0.80) and Relevancy (0.71) are good but not perfect. This suggests the "Answer Synthesis" step (the LLM prompt) could be optimized. It might be too verbose or slightly drifting from the strict context.

## 5. Conclusion & Next Steps
The baseline is strong (Retrieval: 1.0, Generation: ~0.75).
To stress-test the system, we need:
1.  **More Complex Data:** Longer audio files with multiple speakers.
2.  **Harder Questions:** Multi-hop reasoning questions.
3.  **Optimization:** Focus on improving *Answer Relevancy* by tuning the system prompt.

**Next Experiment:** Advanced Chunking (Semantic) to see if we can maintain this retrieval quality on larger, messier datasets.
