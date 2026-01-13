# Contributing to Epist.ai

We love your input! We want to make contributing to Epist.ai as easy and transparent as possible, whether it's:

- Reporting a bug
- Discussing the current state of the code
- Submitting a fix
- Proposing a new feature
- Becoming a maintainer

## 🛠️ Development Setup

This project uses `uv` for lightning-fast dependency management.

1.  **Install `uv`**:
    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```

2.  **Clone & Install**:
    ```bash
    git clone https://github.com/Seifollahi/epist.git
    cd epist
    uv sync --all-extras --dev
    ```

3.  **Environment**:
    ```bash
    cp .env.example .env
    # Edit .env with your keys (OpenAI, Anthropic, Fireworks, etc.)
    ```

4.  **Run Development Server**:
    ```bash
    uv run fastapi dev src/main.py
    ```

## 📜 Coding Standards

We maintain high standards to ensure code quality and maintainability:

- **Linting**: We use `ruff` for linting and formatting.
  ```bash
  uv run ruff check .
  uv run ruff format .
  ```
- **Typing**: All new code should have type hints. Verify with `mypy`.
  ```bash
  uv run mypy .
  ```
- **Testing**: Write tests for new features. We use `pytest`.
  ```bash
  uv run pytest
  ```

## 🚀 Pull Request Process

1.  **Branching**: Create a feature branch from `main` (e.g., `feat/add-new-search-filter`).
2.  **Commits**: Use descriptive commit messages (Atomic commits preferred).
3.  **Checks**: Ensure all CI checks (linting, tests) pass locally before pushing.
4.  **Review**: Open a PR against `main`. Provide a clear description of the changes and link any related issues.
5.  **Merge**: Once approved and checks pass, a maintainer will merge your PR.

## ⚖️ License
By contributing, you agree that your contributions will be licensed under its MIT License.
