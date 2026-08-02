"""Streaming bot-run error-handling tests (GitHub issue #11).

`run_stream` used to iterate the response body without checking HTTP status, so
a failed run (401/403/404/5xx) surfaced as an empty stream with no error --
indistinguishable from a successful empty run. These tests wire a real client to
an ``httpx.MockTransport`` and assert a typed SDK error is raised on failure,
while a successful stream still yields typed events.
"""

import httpx
import pytest

from trix import AsyncTrix, Trix
from trix.exceptions import PermissionError as TrixPermissionError
from trix.exceptions import ServerError as TrixServerError

# One "step" event followed by the [DONE] sentinel.
SSE_BODY = b'data: {"event": "step", "message": "hi"}\n\ndata: [DONE]\n\n'


def _forbidden(request: httpx.Request) -> httpx.Response:
    return httpx.Response(403, json={"message": "forbidden"})


def _server_error(request: httpx.Request) -> httpx.Response:
    return httpx.Response(500, json={"message": "boom"})


def _sse_ok(request: httpx.Request) -> httpx.Response:
    return httpx.Response(200, content=SSE_BODY)


def _sync_client(handler) -> Trix:
    client = Trix(api_key="test_key", base_url="https://api.test.com")
    client._client.close()
    client._client = httpx.Client(base_url=client._base_url, transport=httpx.MockTransport(handler))
    return client


def _async_client(handler) -> AsyncTrix:
    client = AsyncTrix(api_key="test_key", base_url="https://api.test.com")
    client._client = httpx.AsyncClient(
        base_url=client._base_url, transport=httpx.MockTransport(handler)
    )
    return client


class TestSyncRunStream:
    def test_raises_typed_error_on_http_failure(self):
        """A 403 run must raise PermissionError, not yield an empty stream."""
        client = _sync_client(_forbidden)
        try:
            with pytest.raises(TrixPermissionError):
                list(client.bots.run_stream("agent-1", message="hi"))
        finally:
            client.close()

    def test_yields_events_on_success(self):
        """A 200 SSE stream still yields typed BotRunStep events."""
        client = _sync_client(_sse_ok)
        try:
            steps = list(client.bots.run_stream("agent-1", message="hi"))
        finally:
            client.close()
        assert len(steps) == 1
        assert steps[0].event == "step"
        assert steps[0].message == "hi"


class TestAsyncRunStream:
    @pytest.mark.asyncio
    async def test_raises_typed_error_on_http_failure(self):
        """A 5xx run must raise ServerError, not yield an empty stream."""
        client = _async_client(_server_error)
        try:
            with pytest.raises(TrixServerError):
                async for _ in client.bots.run_stream("agent-1", message="hi"):
                    pass
        finally:
            await client.close()

    @pytest.mark.asyncio
    async def test_yields_events_on_success(self):
        """A 200 SSE stream still yields typed BotRunStep events (async)."""
        client = _async_client(_sse_ok)
        try:
            steps = [step async for step in client.bots.run_stream("agent-1", message="hi")]
        finally:
            await client.close()
        assert len(steps) == 1
        assert steps[0].event == "step"
        assert steps[0].message == "hi"
