# Changelog

All notable changes to the Epist.ai platform will be documented in this file.

## [1.2.2] - 2026-01-10
### Added
- **Webhook Reliability**: Support for ad-hoc `webhook_url` in transcription requests. Webhooks now fire consistently on both success and failure.
- **Task Deduplication**: The platform now detects duplicate transcription requests for the same URL, returning existing results immediately but still triggering any new webhooks.
- **SDK & API Alignment**: Updated `AudioStatus` response model to include `transcript`, `summary`, and `entities` fields, resolving TypeScript type mismatches.

### Fixed
- **Frontend Consistency**: Standardized audio status labels in the dashboard to align with backend and SDK definitions.
- **Cached Result Webhooks**: Fixed a bug where transcription results retrieved from cache would bypass webhook notifications.

## [1.2.1] - 2026-01-05
### Added
- Granular RSS Ingestion Controls: `max_episodes`, `start_date`, and keyword filtering (`include_keywords`, `exclude_keywords`).
- SDK support for ingestion filters in both Python and JavaScript.

## [1.2.0] - 2026-01-05

### Added
- **RSS Ingestion**: New generic platform feature to ingest entire podcast feeds via RSS.
- **Enhanced Podcast Metadata**: Automated extraction of author, description, and cover images from RSS feeds.
- **Platform Ingestion API**: New endpoint `POST /api/v1/ingest/rss` for programmatic feed ingestion.

## [1.1.0] - 2025-12-27

### Added
- **Stability & Observability**: Integrated **Sentry** across the entire stack (FastAPI & Next.js) for error tracking and performance monitoring.
- **Production Scheduler**: Migrated to **Cloud Scheduler** for periodic feed synchronization, preventing concurrency issues in scaled environments.
- **Tiered Feed Refresh**: Implemented granular control over podcast sync intervals based on organization tier (Free vs Pro).
- **API Hardening**: Added `TrustedHostMiddleware`, `GZipMiddleware`, and comprehensive security headers (CSP, HSTS) for production safety.
- **Database Safety**: Protected production database from automated startup initialization, relying strictly on migrations.
- **Developer Portal**: New dashboard section `/dashboard/developers` with SDK guides and Widget Builder.
- **JavaScript SDK**: Standardized `epist` for Node.js and Browser support with robust error handling.
- **Python SDK**: Refined `epist` for consistent API interaction.
- **Embeddable Widget**: Standalone build for the Audio Search Widget, allowing simple HTML embedding.
- **Epist CLI**: New command-line tool (`epist`) for ingestion, search, and status checks.
- **MCP Server Package**: Modularized `epist-mcp-server` into a standalone Python package for easier distribution.

### Changed
- Refactored `sdks` directory structure to clearly separate `js` (SDK), `widget` (React Component), and `python` (SDK).
- Updated internal documentation to reflect the new Developer Ecosystem.
- Improved database datetime handling for cross-platform compatibility.

## [0.2.0] - 2025-12-16
### Added
- **Epist Connect (MCP)**: Official Model Context Protocol server published to [PyPI](https://pypi.org/project/epist-mcp-server/). Connects Claude Desktop to your audio knowledge base.
- **Billing Robustness**: Idempotent webhook handling and signature verification for Stripe.
- **Reliability**: Global Error Boundaries, 404 Pages, and PII Log Redaction.

## [0.1.0] - 2025-12-08
### Initial Release
- Core Audio RAG Platform.
- Audio Ingestion & Transcription via Fireworks AI.
- Semantic Search using Vector Embeddings.
- Basic Frontend Dashboard.
