"""Shared test helpers: spec'd client mocks + MockTransport smoke clients.

Issue #12. Resource tests used to mock the client as a bare ``Mock()``, which
auto-fabricates *any* attribute — so a call to a client method that does not
exist (the ``self._client.get(...)`` bug behind ~144 broken GitHub methods)
silently "passed". These helpers close that gap:

* :func:`spec_client` / :func:`spec_async_client` return ``Mock(spec=Trix)`` /
  ``Mock(spec=AsyncTrix)`` so accessing an attribute the real client does not
  expose raises ``AttributeError`` inside the test instead of fabricating a
  child mock.
* :func:`capturing_sync_client` / :func:`capturing_async_client` wire a *real*
  client to an ``httpx.MockTransport`` that records requests, so a smoke test
  exercises the whole path (verb + ``/v1`` URL) and catches missing-method AND
  endpoint-drift bugs together.
"""

from __future__ import annotations

import datetime
from typing import Any, Callable
from unittest.mock import Mock

import httpx

from trix import AsyncTrix, Trix


def spec_client() -> Mock:
    """Sync client mock restricted to the real ``Trix`` attribute surface."""
    return Mock(spec=Trix)


def spec_async_client() -> Mock:
    """Async client mock restricted to the real ``AsyncTrix`` attribute surface."""
    return Mock(spec=AsyncTrix)


def _recording_handler(
    captured: list[httpx.Request], body: Any, status: int
) -> Callable[[httpx.Request], httpx.Response]:
    """Build a MockTransport handler that records requests and returns ``body``."""

    def handle(request: httpx.Request) -> httpx.Response:
        captured.append(request)
        response = httpx.Response(status, json=body)
        # MockTransport responses have no ``.elapsed``; debug logging reads it.
        response._elapsed = datetime.timedelta(seconds=0)
        return response

    return handle


def capturing_sync_client(body: Any = None, status: int = 200) -> tuple[Trix, list[httpx.Request]]:
    """Return a real ``Trix`` wired to a MockTransport plus the captured-request list."""
    captured: list[httpx.Request] = []
    client = Trix(api_key="test_key", base_url="https://api.test.com")
    client._client.close()
    client._client = httpx.Client(
        base_url=client._base_url,
        transport=httpx.MockTransport(_recording_handler(captured, body, status)),
    )
    return client, captured


def capturing_async_client(
    body: Any = None, status: int = 200
) -> tuple[AsyncTrix, list[httpx.Request]]:
    """Return a real ``AsyncTrix`` wired to a MockTransport plus the captured-request list."""
    captured: list[httpx.Request] = []
    client = AsyncTrix(api_key="test_key", base_url="https://api.test.com")
    client._client = httpx.AsyncClient(
        base_url=client._base_url,
        transport=httpx.MockTransport(_recording_handler(captured, body, status)),
    )
    return client, captured
