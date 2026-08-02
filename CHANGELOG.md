# Changelog

All notable changes to the Trix Python SDK will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Fixed
- **GitHub resources**: ~144 `client.github.*` methods (e.g. `get_issue_cycle_time`,
  `dead_code_ratio`, `generate_tests`) raised `AttributeError` at call time because they
  invoked `self._client.get/post/put/patch/delete`, which the client never implemented.
  Added these verb helpers to the sync (`Trix`) and async (`AsyncTrix`) clients and to the
  client protocols, so every GitHub method now issues its request and returns the typed
  model. ([#5](https://github.com/trix/trix-python-sdk/issues/5))
- **Multipart uploads**: file uploads (e.g. `client.files.upload`, image/audio memory
  uploads) were sent with `Content-Type: application/json` instead of
  `multipart/form-data`, so the server could not parse the body. `_get_headers()` baked
  `Content-Type` into the `httpx` client-level defaults, which overrode the per-request
  multipart boundary. `Content-Type` is now left unset on the client and derived per
  request by httpx from the `json=` / `files=` body. ([#6](https://github.com/trix/trix-python-sdk/issues/6))
- **Idempotent retries**: the client auto-retries 5xx / 429 responses on all methods, which
  could duplicate a write when a mutating request's first attempt reached the server but the
  response was lost. Mutating requests (POST/PUT/PATCH/DELETE) now send a single stable
  `Idempotency-Key` (generated once, before the retry loop, reused across attempts) so the
  backend dedupes retries. GET and other non-mutating methods send no key; a caller-supplied
  key is preserved. ([#7](https://github.com/trix/trix-python-sdk/issues/7))
- **Packaging**: the version was duplicated across five places (pyproject.toml,
  `trix.__version__`, package.json, .release-please-manifest.json, and the built dist) and
  they disagreed (0.1.1 vs 0.5.0 vs 0.6.0). The version is now single-sourced: pyproject.toml
  is authoritative and `trix.__version__` is read from the installed distribution metadata,
  so runtime and dist always match. package.json and .release-please-manifest.json are
  realigned to the authoritative version.
- **Typing**: added `src/trix/py.typed` and declared it as package data so the PEP 561 marker
  ships in the wheel; downstream type checkers now treat `trix` as typed. ([#9](https://github.com/trix/trix-python-sdk/issues/9))

## [1.0.0] - 2025-12-25

### Added

#### Core Features
- Initial release of Trix Python SDK
- Full support for Trix API v1
- Synchronous client (`Trix`) and asynchronous client (`AsyncTrix`)
- Context manager support for both sync and async clients
- Comprehensive type hints using Pydantic models

#### Resources
- **Memories**: Full CRUD operations, bulk operations, audio transcription
- **Relationships**: Create, update, delete, and reinforce relationships
- **Clusters**: Manage clusters, add/remove memories, cluster expansion
- **Spaces**: Workspace organization and management
- **Graph**: Graph traversal, context retrieval, shortest path finding
- **Search**: Semantic and keyword search, embedding generation
- **Webhooks**: Event notifications and webhook management
- **Agent**: Session management and memory consolidation
- **Feedback**: Search result feedback and relationship creation
- **Highlights**: Text highlighting and auto-extraction
- **Jobs**: Background job monitoring and management

#### Developer Experience
- Automatic retry with exponential backoff for rate limits
- Comprehensive error handling with custom exception types
- Pagination helpers with automatic iteration
- Type-safe request and response models
- Detailed logging support
- Full IDE autocomplete support

#### Documentation
- Comprehensive README with examples
- API documentation in docstrings
- Example scripts for common use cases
- Contributing guidelines

#### Testing
- Unit tests for core functionality
- Integration test structure
- GitHub Actions CI/CD pipeline
- Code coverage reporting

### Technical Details
- Minimum Python version: 3.9
- Built on httpx for HTTP requests
- Pydantic v2 for data validation
- Support for both API key and JWT authentication

[Unreleased]: https://github.com/trix/trix-python-sdk/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/trix/trix-python-sdk/releases/tag/v1.0.0
