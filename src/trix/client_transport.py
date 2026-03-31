"""Synchronous HTTP transport methods for Trix client.

Extracted from client_sync.py to keep files within line limits.
Used as a mixin by the Trix class.
"""

import logging
import time
from typing import Any, BinaryIO, Dict, Iterator, Optional, Tuple, Union

import httpx

from .client_base import (
    RequestContext,
    ResponseContext,
    _safe_log_params,
    check_api_version,
    handle_response,
)
from .exceptions import APIError, ConnectionError, RateLimitError, ServerError, TimeoutError
from .utils.retry import RetryConfig

logger = logging.getLogger(__name__)


class SyncTransportMixin:
    """Mixin providing synchronous HTTP transport methods.

    Requires the host class to provide:
    - _client: httpx.Client
    - _timeout: float
    - _retry_config: RetryConfig
    - _get_headers() -> Dict[str, str]
    - _run_request_interceptors(ctx) -> RequestContext
    - _run_response_interceptors(ctx) -> ResponseContext
    - _run_error_interceptors(error, request) -> Exception
    """

    MAX_RESPONSE_SIZE = 50 * 1024 * 1024  # 50MB

    def _request(
        self,
        method: str,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        timeout: Optional[float] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Any:
        """Make HTTP request to Trix API with retry logic."""
        last_exception: Optional[Exception] = None
        config = self._retry_config
        request_timeout = timeout if timeout is not None else self._timeout

        merged_headers = self._get_headers()
        if headers:
            merged_headers.update(headers)
        request_context = RequestContext(
            method=method, path=path, params=params, json=json, headers=merged_headers
        )
        request_context = self._run_request_interceptors(request_context)

        for attempt in range(config.max_retries + 1):
            try:
                response = self._execute_request(request_context, request_timeout)
                return self._process_response(response, request_context)
            except (RateLimitError, ServerError) as e:
                last_exception = self._handle_retry(e, attempt, config, request_context)
                if last_exception is not None:
                    raise last_exception
            except httpx.TimeoutException as e:
                raise self._handle_httpx_error(e, request_context, "timeout")
            except httpx.NetworkError as e:
                raise self._handle_httpx_error(e, request_context, "network")
            except httpx.HTTPError as e:
                raise self._handle_httpx_error(e, request_context, "http")

        if last_exception:
            raise last_exception
        raise RuntimeError("Retry logic failed unexpectedly")

    def _execute_request(self, ctx: RequestContext, timeout: float) -> httpx.Response:
        """Execute the HTTP request."""
        logger.debug(f"Request: {ctx.method} {ctx.path} params={_safe_log_params(ctx.params)}")
        return self._client.request(
            method=ctx.method,
            url=ctx.path,
            params=ctx.params,
            json=ctx.json,
            headers=ctx.headers,
            timeout=timeout,
        )

    def _process_response(self, response: httpx.Response, ctx: RequestContext) -> Any:
        """Process and validate the HTTP response."""
        safe_headers = {
            k: v if k.lower() != "authorization" else "[REDACTED]"
            for k, v in response.headers.items()
        }
        elapsed = response.elapsed.total_seconds()
        logger.debug(f"Response: {response.status_code} ({elapsed:.3f}s) headers={safe_headers}")

        content_length = response.headers.get("content-length")
        if content_length and int(content_length) > self.MAX_RESPONSE_SIZE:
            raise ValueError(
                f"Response too large: {content_length} bytes (max {self.MAX_RESPONSE_SIZE})"
            )

        check_api_version(response)
        handle_response(response)

        response_data: Any = {} if response.status_code == 204 else response.json()
        response_context = ResponseContext(
            request=ctx,
            status_code=response.status_code,
            headers=dict(response.headers),
            data=response_data,
        )
        response_context = self._run_response_interceptors(response_context)
        return response_context.data

    def _handle_retry(
        self, error: Exception, attempt: int, config: RetryConfig, ctx: RequestContext
    ) -> Optional[Exception]:
        """Handle retry logic. Returns exception if should raise."""
        if attempt >= config.max_retries:
            return self._run_error_interceptors(error, ctx)

        retry_after = getattr(error, "retry_after", None)
        delay = config.calculate_delay(attempt, retry_after)
        logger.warning(
            f"Attempt {attempt + 1}/{config.max_retries + 1} failed: {error}. "
            f"Retrying in {delay:.2f}s..."
        )
        time.sleep(delay)
        return None

    def _handle_httpx_error(
        self, error: Exception, ctx: RequestContext, error_type: str
    ) -> Exception:
        """Convert httpx errors to Trix errors."""
        logger.debug(f"Request {error_type} error: {error}")
        if error_type == "timeout":
            exc: Exception = TimeoutError(f"Request timed out: {error}")
        elif error_type == "network":
            exc = ConnectionError(f"Network error: {error}")
        else:
            exc = APIError(f"HTTP error: {error}")
        return self._run_error_interceptors(exc, ctx)

    def _request_raw(
        self,
        method: str,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        timeout: Optional[float] = None,
    ) -> bytes:
        """Make HTTP request and return raw bytes."""
        request_timeout = timeout if timeout is not None else self._timeout
        try:
            logger.debug(f"Request (raw): {method} {path} params={_safe_log_params(params)}")
            response = self._client.request(
                method=method, url=path, params=params, timeout=request_timeout
            )
            logger.debug(f"Response (raw): {response.status_code}")
            check_api_version(response)
            handle_response(response)
            return response.content
        except httpx.TimeoutException as e:
            raise TimeoutError(f"Request timed out: {e}") from e
        except httpx.NetworkError as e:
            raise ConnectionError(f"Network error: {e}") from e
        except httpx.HTTPError as e:
            raise APIError(f"HTTP error: {e}") from e

    def _request_stream(
        self,
        method: str,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        chunk_size: int = 8192,
        timeout: Optional[float] = None,
    ) -> Iterator[bytes]:
        """Make HTTP request and stream the response."""
        request_timeout = timeout if timeout is not None else self._timeout
        try:
            logger.debug(f"Request (stream): {method} {path} params={_safe_log_params(params)}")
            with self._client.stream(
                method=method, url=path, params=params, timeout=request_timeout
            ) as response:
                logger.debug(f"Response (stream): {response.status_code}")
                check_api_version(response)
                handle_response(response)
                for chunk in response.iter_bytes(chunk_size=chunk_size):
                    yield chunk
        except httpx.TimeoutException as e:
            raise TimeoutError(f"Request timed out: {e}") from e
        except httpx.NetworkError as e:
            raise ConnectionError(f"Network error: {e}") from e
        except httpx.HTTPError as e:
            raise APIError(f"HTTP error: {e}") from e

    def _request_multipart(
        self,
        method: str,
        path: str,
        data: Optional[Dict[str, Any]] = None,
        files: Optional[Dict[str, Union[BinaryIO, Tuple[Any, ...]]]] = None,
        params: Optional[Dict[str, Any]] = None,
        timeout: Optional[float] = None,
    ) -> Any:
        """Make multipart/form-data HTTP request for file uploads."""
        request_timeout = timeout if timeout is not None else self._timeout
        try:
            logger.debug(f"Request (multipart): {method} {path}")
            headers = {k: v for k, v in self._get_headers().items() if k.lower() != "content-type"}
            response = self._client.request(
                method=method,
                url=path,
                data=data,
                files=files,
                params=params,
                headers=headers,
                timeout=request_timeout,
            )
            logger.debug(f"Response (multipart): {response.status_code}")
            check_api_version(response)
            handle_response(response)
            return {} if response.status_code == 204 else response.json()
        except httpx.TimeoutException as e:
            raise TimeoutError(f"Request timed out: {e}") from e
        except httpx.NetworkError as e:
            raise ConnectionError(f"Network error: {e}") from e
        except httpx.HTTPError as e:
            raise APIError(f"HTTP error: {e}") from e
