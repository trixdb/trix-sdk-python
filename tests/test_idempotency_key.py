"""Regression tests for idempotent retries (GitHub issue #7).

The client auto-retries 5xx / 429 on *all* methods. Without an idempotency key,
a retried POST/PUT/PATCH/DELETE can duplicate a write when the first attempt
actually reached the server. The transport now attaches a single stable
``Idempotency-Key`` (uuid4 hex) per logical request — generated once, before the
retry loop — so the backend (``trix-api`` ``plugins/idempotency.js``) dedupes
the retries. GET (and other non-mutating methods) must NOT carry a key.
"""

import datetime

import httpx

from trix import AsyncTrix, Trix
from trix.client_base import apply_idempotency_key
from trix.utils.retry import RetryConfig

FAST_RETRY = RetryConfig(max_retries=3, initial_delay=0.0, jitter=False)


def _resp(status, body):
    response = httpx.Response(status, json=body)
    response._elapsed = datetime.timedelta(seconds=0)
    return response


# --------------------------------------------------------------------------- #
# Unit: the apply_idempotency_key helper                                       #
# --------------------------------------------------------------------------- #


class TestApplyIdempotencyKey:
    def test_mutating_methods_get_a_uuid_key(self):
        for method in ("POST", "PUT", "PATCH", "DELETE", "post", "patch"):
            headers: dict = {}
            apply_idempotency_key(headers, method)
            key = headers.get("Idempotency-Key")
            assert key is not None, method
            assert len(key) == 32 and all(c in "0123456789abcdef" for c in key)

    def test_non_mutating_methods_get_no_key(self):
        for method in ("GET", "HEAD", "OPTIONS", "get"):
            headers: dict = {}
            apply_idempotency_key(headers, method)
            assert "Idempotency-Key" not in headers

    def test_existing_key_is_preserved(self):
        headers = {"idempotency-key": "caller-supplied"}
        apply_idempotency_key(headers, "POST")
        assert headers["idempotency-key"] == "caller-supplied"
        # No second (differently-cased) key was added.
        assert [k for k in headers if k.lower() == "idempotency-key"] == ["idempotency-key"]


# --------------------------------------------------------------------------- #
# Integration: the key is stable across retries and absent on GET             #
# --------------------------------------------------------------------------- #


def _sync_client(handler) -> Trix:
    client = Trix(api_key="test_key", base_url="https://api.test.com", retry_config=FAST_RETRY)
    client._client.close()
    client._client = httpx.Client(base_url=client._base_url, transport=httpx.MockTransport(handler))
    return client


class TestIdempotentRetries:
    def test_post_retry_reuses_the_same_key(self):
        """A POST that 500s then succeeds must carry ONE key across both tries."""
        keys: list = []
        state = {"n": 0}

        def handler(request: httpx.Request) -> httpx.Response:
            keys.append(request.headers.get("idempotency-key"))
            state["n"] += 1
            return _resp(500, {"error": "boom"}) if state["n"] == 1 else _resp(200, {"ok": True})

        client = _sync_client(handler)
        try:
            result = client._request("POST", "/memories", json={"content": "x"})
        finally:
            client.close()

        assert result == {"ok": True}
        assert len(keys) == 2  # one failed attempt + one successful retry
        assert keys[0] is not None
        assert keys[0] == keys[1]  # SAME key on the retry (not regenerated)

    def test_get_sends_no_idempotency_key(self):
        seen: dict = {}

        def handler(request: httpx.Request) -> httpx.Response:
            seen["key"] = request.headers.get("idempotency-key")
            return _resp(200, {"ok": True})

        client = _sync_client(handler)
        try:
            client._request("GET", "/memories")
        finally:
            client.close()

        assert seen["key"] is None

    async def test_async_post_retry_reuses_the_same_key(self):
        keys: list = []
        state = {"n": 0}

        def handler(request: httpx.Request) -> httpx.Response:
            keys.append(request.headers.get("idempotency-key"))
            state["n"] += 1
            return _resp(503, {"error": "boom"}) if state["n"] == 1 else _resp(200, {"ok": True})

        client = AsyncTrix(
            api_key="test_key", base_url="https://api.test.com", retry_config=FAST_RETRY
        )
        client._client = httpx.AsyncClient(
            base_url=client._base_url, transport=httpx.MockTransport(handler)
        )
        try:
            result = await client._request("POST", "/memories", json={"content": "x"})
        finally:
            await client.close()

        assert result == {"ok": True}
        assert len(keys) == 2
        assert keys[0] is not None and keys[0] == keys[1]
