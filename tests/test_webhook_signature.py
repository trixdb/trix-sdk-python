"""Tests for inbound webhook signature verification.

Covers ``webhooks.verify_signature`` / ``webhooks.unwrap`` on both the sync and
async resources. Signatures are recomputed here exactly as the server does in
trix-api ``src/lib/webhook-service.js`` (HMAC-SHA256 over ``"{timestamp}.{body}"``,
hex-encoded, keyed by the signing secret) to prove cross-implementation parity.
"""

import hashlib
import hmac
import time

import pytest

from tests.support import spec_async_client, spec_client
from trix.exceptions import WebhookVerificationError
from trix.resources.webhooks import AsyncWebhooksResource, WebhooksResource

SECRET = "whsec_super_secret_value"
PAYLOAD = '{"event":"memory.created","data":{"memory_id":"mem_123"}}'


def _sign(payload, secret=SECRET, timestamp=None):
    """Build an ``X-Webhook-Signature`` header exactly as trix-api does."""
    ts = int(time.time()) if timestamp is None else timestamp
    body = payload if isinstance(payload, bytes) else payload.encode("utf-8")
    message = f"{ts}.".encode("utf-8") + body
    digest = hmac.new(secret.encode("utf-8"), message, hashlib.sha256).hexdigest()
    return f"t={ts},v1={digest}"


def _sync():
    return WebhooksResource(spec_client())


def _async():
    return AsyncWebhooksResource(spec_async_client())


class TestVerifySignatureValid:
    """A well-formed, fresh, matching signature verifies as True."""

    def test_correctly_signed_returns_true(self):
        header = _sign(PAYLOAD)
        assert _sync().verify_signature(PAYLOAD, header, SECRET) is True

    def test_bytes_payload_returns_true(self):
        body = PAYLOAD.encode("utf-8")
        header = _sign(body)
        assert _sync().verify_signature(body, header, SECRET) is True

    def test_recent_timestamp_within_tolerance_returns_true(self):
        header = _sign(PAYLOAD, timestamp=int(time.time()) - 120)
        assert _sync().verify_signature(PAYLOAD, header, SECRET) is True

    def test_async_twin_correctly_signed_returns_true(self):
        header = _sign(PAYLOAD)
        assert _async().verify_signature(PAYLOAD, header, SECRET) is True


class TestVerifySignatureInvalid:
    """Tampering, wrong secret, expiry, and bad headers all verify as False."""

    def test_tampered_payload_returns_false(self):
        header = _sign(PAYLOAD)
        tampered = PAYLOAD.replace("mem_123", "mem_evil")
        assert _sync().verify_signature(tampered, header, SECRET) is False

    def test_wrong_secret_returns_false(self):
        header = _sign(PAYLOAD)
        assert _sync().verify_signature(PAYLOAD, header, "whsec_wrong") is False

    def test_expired_timestamp_returns_false(self):
        header = _sign(PAYLOAD, timestamp=int(time.time()) - 301)
        assert _sync().verify_signature(PAYLOAD, header, SECRET) is False

    def test_future_timestamp_beyond_tolerance_returns_false(self):
        header = _sign(PAYLOAD, timestamp=int(time.time()) + 3600)
        assert _sync().verify_signature(PAYLOAD, header, SECRET) is False

    def test_custom_tolerance_allows_older_timestamp(self):
        header = _sign(PAYLOAD, timestamp=int(time.time()) - 301)
        assert _sync().verify_signature(PAYLOAD, header, SECRET, tolerance_seconds=600) is True

    @pytest.mark.parametrize(
        "header",
        [
            "",
            "not-a-signature",
            "v1=abcdef",
            "t=abc,v1=abcdef",
            "t=123",
            "t=123,v1=NOTHEX",
            "t=123,v1=deadbeef",
        ],
    )
    def test_malformed_or_mismatched_header_returns_false(self, header):
        assert _sync().verify_signature(PAYLOAD, header, SECRET) is False

    def test_async_twin_tampered_returns_false(self):
        header = _sign(PAYLOAD)
        assert _async().verify_signature("{}", header, SECRET) is False


class TestUnwrap:
    """unwrap() returns the decoded event or raises WebhookVerificationError."""

    def test_unwrap_valid_returns_dict(self):
        header = _sign(PAYLOAD)
        event = _sync().unwrap(PAYLOAD, header, SECRET)
        assert event == {"event": "memory.created", "data": {"memory_id": "mem_123"}}

    def test_unwrap_async_twin_valid_returns_dict(self):
        header = _sign(PAYLOAD)
        event = _async().unwrap(PAYLOAD, header, SECRET)
        assert event["event"] == "memory.created"

    def test_unwrap_tampered_raises(self):
        header = _sign(PAYLOAD)
        with pytest.raises(WebhookVerificationError):
            _sync().unwrap(PAYLOAD.replace("mem_123", "x"), header, SECRET)

    def test_unwrap_malformed_header_raises(self):
        with pytest.raises(WebhookVerificationError):
            _sync().unwrap(PAYLOAD, "garbage", SECRET)

    def test_unwrap_expired_raises(self):
        header = _sign(PAYLOAD, timestamp=int(time.time()) - 10_000)
        with pytest.raises(WebhookVerificationError):
            _sync().unwrap(PAYLOAD, header, SECRET)

    def test_unwrap_non_object_body_raises(self):
        body = "[1, 2, 3]"
        header = _sign(body)
        with pytest.raises(WebhookVerificationError):
            _sync().unwrap(body, header, SECRET)
