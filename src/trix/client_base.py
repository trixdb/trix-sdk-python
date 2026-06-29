"""Base client types, utilities, and shared functionality.

This module contains shared types and utilities used by both sync and async clients.
"""

import logging
from dataclasses import dataclass, field
from typing import Any, Awaitable, Callable, Dict, Optional

import httpx

from . import MAX_API_VERSION, MIN_API_VERSION, __version__
from .exceptions import (
    APIError,
    APIVersionMismatchError,
    AuthenticationError,
    ConflictError,
    NotFoundError,
    PermissionError,
    RateLimitError,
    ServerError,
    ValidationError,
)
from .utils.security import redact_sensitive_data

API_VERSION_PREFIX = "/v1"


def versioned_path(path: str) -> str:
    """Prepend the ``/v1`` API-version prefix to a request path (idempotent).

    Resource files use leading-slash paths such as ``/goals``. With httpx a
    leading-slash request path *replaces* the base_url path, so any ``/v1`` a
    caller put in ``base_url`` is silently dropped and the request 404s against
    the versioned API. Prefixing here guarantees every request is versioned.

    Paths already starting with ``/v1`` (e.g. the GitHub resource) are returned
    unchanged to avoid producing ``/v1/v1``.
    """
    if path == API_VERSION_PREFIX or path.startswith(API_VERSION_PREFIX + "/"):
        return path
    if not path.startswith("/"):
        path = "/" + path
    return API_VERSION_PREFIX + path


def normalize_base_url(base_url: str) -> str:
    """Drop a trailing ``/v1`` (and slashes) from a base URL.

    The transport prepends ``/v1`` to every path and httpx *concatenates* the
    base-URL path with the request path (a leading-slash request path does not
    replace it). Stripping a caller-supplied ``/v1`` suffix here keeps exactly
    one ``/v1`` segment whether or not the base URL already included it.
    """
    trimmed = base_url.rstrip("/")
    if trimmed.endswith(API_VERSION_PREFIX):
        trimmed = trimmed[: -len(API_VERSION_PREFIX)]
    return trimmed


@dataclass
class RequestContext:
    """Context passed to request interceptors.

    Attributes:
        method: HTTP method (GET, POST, PUT, DELETE, etc.)
        path: API endpoint path
        headers: Request headers
        params: Query parameters
        json: JSON body for POST/PUT requests
    """

    method: str
    path: str
    headers: Dict[str, str] = field(default_factory=dict)
    params: Optional[Dict[str, Any]] = None
    json: Optional[Dict[str, Any]] = None


@dataclass
class ResponseContext:
    """Context passed to response interceptors.

    Attributes:
        request: The original request context
        status_code: HTTP response status code
        headers: Response headers
        data: Parsed response data
    """

    request: RequestContext
    status_code: int
    headers: Dict[str, str]
    data: Any


# Interceptor type aliases
RequestInterceptor = Callable[[RequestContext], Optional[RequestContext]]
ResponseInterceptor = Callable[[ResponseContext], Optional[ResponseContext]]
ErrorInterceptor = Callable[[Exception, RequestContext], Exception]

# Async interceptor type aliases
AsyncRequestInterceptor = Callable[[RequestContext], Awaitable[Optional[RequestContext]]]
AsyncResponseInterceptor = Callable[[ResponseContext], Awaitable[Optional[ResponseContext]]]
AsyncErrorInterceptor = Callable[[Exception, RequestContext], Awaitable[Exception]]


@dataclass
class PoolConfig:
    """Connection pool configuration.

    Args:
        max_connections: Maximum number of allowable connections in the pool.
            Default is 100.
        max_keepalive_connections: Maximum number of keep-alive connections.
            Default is 20.
        keepalive_expiry: Time in seconds for keep-alive connections to remain
            idle before being closed. Default is 5 seconds.
    """

    max_connections: int = 100
    max_keepalive_connections: int = 20
    keepalive_expiry: float = 5.0

    def to_httpx_limits(self) -> httpx.Limits:
        """Convert to httpx.Limits object."""
        return httpx.Limits(
            max_connections=self.max_connections,
            max_keepalive_connections=self.max_keepalive_connections,
            keepalive_expiry=self.keepalive_expiry,
        )


logger = logging.getLogger(__name__)


def _safe_log_params(params: Optional[Dict[str, Any]]) -> str:
    """Safely format params for logging, redacting sensitive data."""
    if params is None:
        return "None"
    return str(redact_sensitive_data(params))


def check_api_version(response: httpx.Response) -> None:
    """Check if the API version is compatible with this SDK.

    Args:
        response: HTTP response object

    Raises:
        APIVersionMismatchError: If API version is incompatible
    """
    api_version = response.headers.get("X-API-Version")
    if api_version:
        try:
            api_num = int(api_version.lstrip("v"))
            min_num = int(MIN_API_VERSION.lstrip("v"))
            max_num = int(MAX_API_VERSION.lstrip("v"))

            if api_num < min_num or api_num > max_num:
                raise APIVersionMismatchError(
                    f"API version {api_version} is not supported by this SDK. "
                    f"Supported versions: {MIN_API_VERSION} to {MAX_API_VERSION}. "
                    f"Please upgrade or downgrade the SDK.",
                    sdk_version=__version__,
                    api_version=api_version,
                    min_supported=MIN_API_VERSION,
                    max_supported=MAX_API_VERSION,
                )
        except ValueError:
            logger.warning(f"Could not parse API version: {api_version}")


def handle_response(response: httpx.Response) -> None:
    """Handle HTTP response and raise appropriate exceptions.

    Args:
        response: HTTP response object

    Raises:
        TrixError: On error responses
    """
    if response.is_success:
        return

    error_data: Optional[Dict[str, Any]] = None
    try:
        error_data = response.json()
        message = error_data.get("message", error_data.get("error", "Unknown error"))
    except Exception:
        message = response.text or f"HTTP {response.status_code}"

    if response.status_code == 401:
        raise AuthenticationError(message, response.status_code, error_data)
    elif response.status_code == 403:
        raise PermissionError(message, response.status_code, error_data)
    elif response.status_code == 404:
        raise NotFoundError(message, response.status_code, error_data)
    elif response.status_code == 422:
        raise ValidationError(message, response.status_code, error_data)
    elif response.status_code == 429:
        retry_after = response.headers.get("Retry-After")
        retry_after_value = None
        if retry_after:
            try:
                retry_after_value = min(int(retry_after), 60)  # Cap at 60 seconds
            except (ValueError, TypeError):
                retry_after_value = None
        raise RateLimitError(
            message,
            retry_after=retry_after_value,
            status_code=response.status_code,
            response=error_data,
        )
    elif response.status_code == 409:
        raise ConflictError(message, response.status_code, error_data)
    elif response.status_code >= 500:
        raise ServerError(message, response.status_code, error_data)
    else:
        raise APIError(message, response.status_code, error_data)
