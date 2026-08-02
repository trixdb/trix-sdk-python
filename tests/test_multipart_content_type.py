"""Regression tests for multipart Content-Type (GitHub issue #6).

``_get_headers()`` used to bake ``Content-Type: application/json`` into the
headers that become the ``httpx.Client`` / ``httpx.AsyncClient`` defaults. Those
client-level defaults leak into every request, so even though
``_request_multipart`` stripped ``Content-Type`` from *its* per-request headers,
the baked-in ``application/json`` still won and httpx never emitted the
``multipart/form-data; boundary=...`` it generates for ``files=``. Uploads went
out mislabelled as JSON.

The fix drops ``Content-Type`` from the client defaults and lets httpx set it
per request from the ``json=`` / ``files=`` body. These tests wire a real
client to an ``httpx.MockTransport`` and assert the on-the-wire Content-Type for
both an upload and a normal JSON POST.
"""

import datetime
import io

import httpx

from trix import AsyncTrix, Trix
from trix.types.file import ChatFile

CHAT_FILE_BODY = {"id": "file_123", "filename": "test.txt"}


def _make_handler(captured, body):
    def handler(request: httpx.Request) -> httpx.Response:
        captured["content_type"] = request.headers.get("content-type")
        captured["body"] = request.content
        response = httpx.Response(200, json=body)
        response._elapsed = datetime.timedelta(seconds=0)
        return response

    return handler


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


class TestMultipartContentType:
    def test_client_defaults_have_no_content_type(self):
        """The client-level default headers must not pin Content-Type."""
        client = Trix(api_key="test_key", base_url="https://api.test.com")
        try:
            default_keys = {k.lower() for k in client._client.headers}
            assert "content-type" not in default_keys
            assert "content-type" not in {k.lower() for k in client._get_headers()}
        finally:
            client.close()

    def test_upload_sends_multipart_content_type(self):
        """A file upload must go out as multipart/form-data with a real body."""
        captured: dict = {}
        client = _sync_client(_make_handler(captured, CHAT_FILE_BODY))
        try:
            result = client.files.upload(
                io.BytesIO(b"hello world"), filename="test.txt", content_type="text/plain"
            )
        finally:
            client.close()

        assert captured["content_type"].startswith("multipart/form-data")
        assert "boundary=" in captured["content_type"]
        # A genuine multipart body: part headers + filename + the file bytes.
        body = captured["body"]
        assert b'Content-Disposition: form-data; name="file"' in body
        assert b'filename="test.txt"' in body
        assert b"hello world" in body
        assert isinstance(result, ChatFile)
        assert result.id == "file_123"

    def test_json_post_still_sends_application_json(self):
        """A normal JSON POST must still be labelled application/json."""
        captured: dict = {}
        client = _sync_client(_make_handler(captured, {}))
        try:
            client._request("POST", "/memories", json={"content": "hi"})
        finally:
            client.close()

        assert captured["content_type"] == "application/json"
        assert captured["body"] == b'{"content":"hi"}'

    async def test_async_upload_sends_multipart_content_type(self):
        """The async multipart transport must also emit multipart/form-data."""
        captured: dict = {}
        client = _async_client(_make_handler(captured, CHAT_FILE_BODY))
        try:
            await client._request_multipart(
                "POST",
                "/files/upload",
                data={"conversation_id": "c1"},
                files={"file": ("a.bin", io.BytesIO(b"async bytes"), "application/octet-stream")},
            )
        finally:
            await client.close()

        assert captured["content_type"].startswith("multipart/form-data")
        assert "boundary=" in captured["content_type"]
        assert b"async bytes" in captured["body"]
        assert b'filename="a.bin"' in captured["body"]

    async def test_async_json_post_still_sends_application_json(self):
        captured: dict = {}
        client = _async_client(_make_handler(captured, {}))
        try:
            await client._request("POST", "/memories", json={"content": "hi"})
        finally:
            await client.close()

        assert captured["content_type"] == "application/json"
