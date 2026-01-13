# Epist R&D Lab 🧪

This directory contains scientific experiments, benchmarks, and research prototypes for the Epist Audio RAG platform.

## Purpose
-   **Scientific Rigor:** Verify improvements with data, not guesses.
-   **Isolation:** Experiments run here without affecting the production kernel.
-   **Reproducibility:** All benchmarks should be repeatable scripts.

## Setup
1.  Install dependencies:
    ```bash
    uv sync --extra lab
    ```
2.  Run the evaluation dashboard:
    ```bash
    python -m phoenix.server.main serve
    ```

## Experiments
-   `exp01_baseline`: Benchmarking the current production API.
-   `exp02_chunking`: Comparing Semantic vs. Fixed chunking.
