# Changelog

All notable changes to the Trix Python SDK will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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
