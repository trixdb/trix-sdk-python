"""Transport-level retry tests (GitHub issue #8).

``RetryConfig.retryable_exceptions`` used to be silently ignored by the
transport, which hardcoded ``except (RateLimitError, ServerError)``. These
tests wire a real client to an ``httpx.MockTransport`` that counts attempts and
assert that a custom ``retryable_exceptions`` set actually governs whether the
transport retries -- both for errors it should now retry and ones it must not.
"""

import datetime

import httpx
import pytest

from trix import AsyncTrix, Trix
from trix.exceptions import ConnectionError as TrixConnectionError
from trix.exceptions import ServerError as TrixServerError
from trix.exceptions import TimeoutError as TrixTimeoutError
from trix.utils.retry import RetryConfig

# Fast, deterministic retries: zero delay, no jitter, two retries (3 attempts).
FAST = {"max_retries": 2, "initial_delay": 0.0, "jitter": False}


def _server_error(request: httpx.Request) -> httpx.Response:
    response = httpx.Response(500, json={"message": "boom"})
    response._elapsed = datetime.timedelta(0)
    return response


def _raise_connect(request: httpx.Request) -> httpx.Response:
    raise httpx.ConnectError("connection refused")


class _Counting:
    """Wrap a MockTransport handler and count how many times it is invoked."""

    def __init__(self, handler):
        self._handler = handler
        self.calls = 0

    def __call__(self, request: httpx.Request) -> httpx.Response:
        self.calls += 1
        return self._handler(request)


def _sync_client(handler, config: RetryConfig) -> Trix:
    client = Trix(api_key="test_key", base_url="https://api.test.com", retry_config=config)
    client._client.close()
    client._client = httpx.Client(base_url=client._base_url, transport=httpx.MockTransport(handler))
    return client


def _async_client(handler, config: RetryConfig) -> AsyncTrix:
    client = AsyncTrix(api_key="test_key", base_url="https://api.test.com", retry_config=config)
    client._client = httpx.AsyncClient(
        base_url=client._base_url, transport=httpx.MockTransport(handler)
    )
    return client


class TestSyncTransportHonorsConfig:
    def test_configured_connection_error_is_retried(self):
        """A network error IS retried when ConnectionError is configured retryable."""
        handler = _Counting(_raise_connect)
        config = RetryConfig(retryable_exceptions={TrixConnectionError, TrixTimeoutError}, **FAST)
        client = _sync_client(handler, config)
        try:
            with pytest.raises(TrixConnectionError):
                client._request("GET", "/ping")
        finally:
            client.close()
        assert handler.calls == 3  # 1 initial + 2 retries

    def test_default_config_does_not_retry_connection_error(self):
        """The default set {RateLimitError, ServerError} leaves timeouts un-retried."""
        handler = _Counting(_raise_connect)
        client = _sync_client(handler, RetryConfig(**FAST))
        try:
            with pytest.raises(TrixConnectionError):
                client._request("GET", "/ping")
        finally:
            client.close()
        assert handler.calls == 1  # no retry

    def test_unlisted_server_error_is_not_retried(self):
        """A 5xx is NOT retried when ServerError is excluded from the config."""
        handler = _Counting(_server_error)
        config = RetryConfig(retryable_exceptions={TrixTimeoutError}, **FAST)
        client = _sync_client(handler, config)
        try:
            with pytest.raises(TrixServerError):
                client._request("GET", "/ping")
        finally:
            client.close()
        assert handler.calls == 1  # ServerError not retryable here

    def test_default_config_still_retries_server_error(self):
        """Regression guard: default behavior (retry 5xx) is preserved."""
        handler = _Counting(_server_error)
        client = _sync_client(handler, RetryConfig(**FAST))
        try:
            with pytest.raises(TrixServerError):
                client._request("GET", "/ping")
        finally:
            client.close()
        assert handler.calls == 3  # retried to exhaustion


class TestAsyncTransportHonorsConfig:
    @pytest.mark.asyncio
    async def test_configured_connection_error_is_retried(self):
        handler = _Counting(_raise_connect)
        config = RetryConfig(retryable_exceptions={TrixConnectionError, TrixTimeoutError}, **FAST)
        client = _async_client(handler, config)
        try:
            with pytest.raises(TrixConnectionError):
                await client._request("GET", "/ping")
        finally:
            await client.close()
        assert handler.calls == 3

    @pytest.mark.asyncio
    async def test_unlisted_server_error_is_not_retried(self):
        handler = _Counting(_server_error)
        config = RetryConfig(retryable_exceptions={TrixTimeoutError}, **FAST)
        client = _async_client(handler, config)
        try:
            with pytest.raises(TrixServerError):
                await client._request("GET", "/ping")
        finally:
            await client.close()
        assert handler.calls == 1
