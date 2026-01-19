"""Main Trix client for sync and async operations.

This module provides backward-compatible exports from the refactored client modules.
For new code, you can import directly from the specific modules:
- trix.client_sync for Trix (sync client)
- trix.client_async for AsyncTrix
- trix.client_base for shared types (RequestContext, ResponseContext, PoolConfig)
"""

# Re-export from base module
from .client_base import (
    AsyncErrorInterceptor,
    AsyncRequestInterceptor,
    AsyncResponseInterceptor,
    ErrorInterceptor,
    PoolConfig,
    RequestContext,
    RequestInterceptor,
    ResponseContext,
    ResponseInterceptor,
)

# Re-export from sync client
from .client_sync import Trix

# Re-export from async client
from .client_async import AsyncTrix

__all__ = [
    # Client classes
    "Trix",
    "AsyncTrix",
    # Types
    "RequestContext",
    "ResponseContext",
    "PoolConfig",
    # Interceptors
    "RequestInterceptor",
    "ResponseInterceptor",
    "ErrorInterceptor",
    "AsyncRequestInterceptor",
    "AsyncResponseInterceptor",
    "AsyncErrorInterceptor",
]
