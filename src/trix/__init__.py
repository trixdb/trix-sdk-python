"""
Trix Python SDK - Official Python client for Trix API.

Trix is a memory and knowledge management API that provides:
- Memory storage and retrieval
- Relationship management between memories
- Clustering and organization
- Graph traversal and analysis
- Semantic search
- Webhooks for event notifications
- Agent session management

Example:
    >>> from trix import Trix
    >>> client = Trix(api_key="your_api_key")
    >>> memory = client.memories.create(content="Important information")
    >>> print(memory.id)

Async Example:
    >>> from trix import AsyncTrix
    >>> async with AsyncTrix(api_key="your_api_key") as client:
    ...     memory = await client.memories.create(content="Important information")
    ...     print(memory.id)
"""

# Version constants - must be defined before importing submodules to avoid circular imports.
# The version is single-sourced from the installed distribution metadata, which setuptools
# populates from ``[project] version`` in pyproject.toml — the one authoritative source.
from importlib.metadata import PackageNotFoundError, version as _dist_version

try:
    __version__ = _dist_version("trixdb")
except PackageNotFoundError:  # pragma: no cover - running from a source tree without install
    __version__ = "0.0.0+unknown"
__api_version__ = "v1"
MIN_API_VERSION = "v1"
MAX_API_VERSION = "v1"

# ruff: noqa: E402
from .client import (
    AsyncTrix,
    ErrorInterceptor,
    PoolConfig,
    RequestContext,
    RequestInterceptor,
    ResponseContext,
    ResponseInterceptor,
    Trix,
)
from .protocols import AsyncClientProtocol, ClientProtocol, SyncClientProtocol
from .utils.pagination import AsyncPaginator, SyncPaginator
from .utils.retry import RetryConfig
from .utils.security import (
    validate_id,
    validate_base_url,
    validate_webhook_url,
    redact_sensitive_data,
    get_env_credential,
    mask_credential,
)
from .utils.logging import (
    LogConfig,
    LogFormat,
    LogLevel,
    get_logger,
    setup_logging,
    request_context,
)
from .utils.metrics import (
    InMemoryCollector,
    MetricsCollector,
    RequestMetrics,
    get_metrics_collector,
    set_metrics_collector,
    timed_request,
)
from .utils.telemetry import (
    TelemetryConfig,
    SpanStatusCode,
    SpanKind,
    RequestSpan,
    configure_telemetry,
    get_telemetry_config,
    is_telemetry_enabled,
    create_request_span,
    traced,
    with_tracing,
    with_tracing_async,
)
from .exceptions import (
    APIError,
    APIVersionMismatchError,
    AuthenticationError,
    ConflictError,
    ConnectionError,
    NotFoundError,
    PermissionError,
    RateLimitError,
    ServerError,
    TimeoutError,
    TrixError,
    ValidationError,
)
from ._type_exports import *  # noqa: F401, F403
from ._type_exports import TYPE_NAMES

__all__ = [
    # Clients
    "Trix",
    "AsyncTrix",
    # Protocols
    "SyncClientProtocol",
    "AsyncClientProtocol",
    "ClientProtocol",
    # Utilities
    "RetryConfig",
    "PoolConfig",
    "SyncPaginator",
    "AsyncPaginator",
    # Interceptors
    "RequestContext",
    "ResponseContext",
    "RequestInterceptor",
    "ResponseInterceptor",
    "ErrorInterceptor",
    # Security utilities
    "validate_id",
    "validate_base_url",
    "validate_webhook_url",
    "redact_sensitive_data",
    "get_env_credential",
    "mask_credential",
    # Logging utilities
    "LogConfig",
    "LogFormat",
    "LogLevel",
    "get_logger",
    "setup_logging",
    "request_context",
    # Metrics utilities
    "InMemoryCollector",
    "MetricsCollector",
    "RequestMetrics",
    "get_metrics_collector",
    "set_metrics_collector",
    "timed_request",
    # Telemetry utilities (OpenTelemetry integration)
    "TelemetryConfig",
    "SpanStatusCode",
    "SpanKind",
    "RequestSpan",
    "configure_telemetry",
    "get_telemetry_config",
    "is_telemetry_enabled",
    "create_request_span",
    "traced",
    "with_tracing",
    "with_tracing_async",
    # Exceptions
    "TrixError",
    "APIError",
    "APIVersionMismatchError",
    "AuthenticationError",
    "ConflictError",
    "PermissionError",
    "NotFoundError",
    "ValidationError",
    "RateLimitError",
    "ServerError",
    "ConnectionError",
    "TimeoutError",
    # Types (from _type_exports)
    *TYPE_NAMES,
]
