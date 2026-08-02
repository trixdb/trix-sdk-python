"""Tests for the spec'd-mock test helpers (issue #12).

These lock in the property that makes the shared fixtures worth having: a spec'd
client mock raises ``AttributeError`` for attributes the real client does not
expose, so a resource that calls a nonexistent client method fails loudly in
tests instead of silently passing on a bare ``Mock()``.
"""

from unittest.mock import Mock

import pytest

from tests.support import spec_async_client, spec_client

# The client surface resources actually use (all defined on the transport mixin).
REAL_SURFACE = [
    "_request",
    "get",
    "post",
    "put",
    "patch",
    "delete",
    "_request_multipart",
    "_request_raw",
    "_request_stream",
]


class TestSpecClient:
    def test_real_surface_is_accessible(self):
        client = spec_client()
        for attr in REAL_SURFACE:
            assert hasattr(client, attr), f"spec'd client is missing real method {attr}"

    def test_unknown_attribute_raises(self):
        client = spec_client()
        with pytest.raises(AttributeError):
            client.definitely_not_a_client_method  # noqa: B018

    def test_request_return_value_is_configurable(self):
        client = spec_client()
        client._request.return_value = {"ok": True}
        assert client._request("GET", "/x") == {"ok": True}
        assert client._request.call_args[0] == ("GET", "/x")

    def test_fixture_matches_helper(self, mock_trix):
        with pytest.raises(AttributeError):
            mock_trix.nonexistent_method  # noqa: B018


class TestSpecAsyncClient:
    async def test_request_is_async(self):
        client = spec_async_client()
        client._request.return_value = {"ok": True}
        assert await client._request("GET", "/x") == {"ok": True}

    def test_unknown_attribute_raises(self):
        client = spec_async_client()
        with pytest.raises(AttributeError):
            client.definitely_not_a_client_method  # noqa: B018

    def test_fixture(self, mock_async_trix):
        with pytest.raises(AttributeError):
            mock_async_trix.nonexistent_method  # noqa: B018


class _BrokenResource:
    """A resource that calls a client method the real ``Trix`` does not have."""

    def __init__(self, client):
        self._client = client

    def run(self):
        # Real ``Trix`` has no ``.fetch`` — same shape as the ~144 GitHub methods.
        return self._client.fetch("/v1/whatever")


def test_bare_mock_hides_missing_method_but_spec_catches_it():
    # Bare Mock() fabricates ``.fetch`` -> the bug stays invisible (the old style).
    _BrokenResource(Mock()).run()  # does not raise: that is exactly the problem

    # Spec'd mock rejects the nonexistent method -> the bug surfaces in tests.
    with pytest.raises(AttributeError):
        _BrokenResource(spec_client()).run()
