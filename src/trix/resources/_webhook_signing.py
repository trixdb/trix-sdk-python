"""Inbound webhook signature verification for the Trix SDK.

Trix signs every webhook delivery with HMAC-SHA256 over ``"{timestamp}.{body}"``
using the endpoint's signing secret and sends it as the header
``X-Webhook-Signature: t=<unix_seconds>,v1=<hex>``. The helpers here recompute
that signature over the *raw* request body and compare it in constant time,
rejecting deliveries whose timestamp is outside the allowed tolerance (replay
protection). The scheme mirrors trix-api ``src/lib/webhook-service.js`` exactly.
"""

import hashlib
import hmac
import json
import re
import time
from typing import Any, Dict, Optional, Tuple, Union

from ..exceptions import WebhookVerificationError

# ``t=<unix_seconds>,v1=<hex_hmac_sha256>`` — keep in lockstep with trix-api.
_SIGNATURE_HEADER_RE = re.compile(r"^t=(\d+),v1=([a-f0-9]+)$")

DEFAULT_TOLERANCE_SECONDS = 300


def _payload_bytes(payload: Union[str, bytes]) -> bytes:
    """Return the raw UTF-8 bytes of a str/bytes payload unchanged."""
    return payload if isinstance(payload, bytes) else payload.encode("utf-8")


def _parse_signature_header(header: str) -> Optional[Tuple[str, str]]:
    """Parse ``t=<ts>,v1=<hex>`` into ``(timestamp, hex_signature)`` or None."""
    match = _SIGNATURE_HEADER_RE.match(header)
    if match is None:
        return None
    return match.group(1), match.group(2)


def _expected_signature(secret: str, timestamp: str, payload: Union[str, bytes]) -> str:
    """Recompute the hex HMAC-SHA256 over ``"{timestamp}.{payload}"``."""
    message = timestamp.encode("utf-8") + b"." + _payload_bytes(payload)
    return hmac.new(secret.encode("utf-8"), message, hashlib.sha256).hexdigest()


def verify_webhook_signature(
    payload: Union[str, bytes],
    signature_header: str,
    secret: str,
    *,
    tolerance_seconds: int = DEFAULT_TOLERANCE_SECONDS,
) -> bool:
    """Verify the ``X-Webhook-Signature`` of an inbound webhook delivery.

    Args:
        payload: The raw request body exactly as received (``str`` or ``bytes``).
            Do not re-serialize parsed JSON — any whitespace or key-order change
            invalidates the signature.
        signature_header: The ``X-Webhook-Signature`` header value.
        secret: The webhook's signing secret.
        tolerance_seconds: Maximum allowed clock skew in seconds (default 300).

    Returns:
        ``True`` if the signature is present, well-formed, fresh, and matches;
        ``False`` otherwise (missing/malformed header, wrong secret, tampered
        body, or expired timestamp).

    Example:
        >>> verify_webhook_signature(
        ...     raw_body, request.headers["X-Webhook-Signature"], "whsec_..."
        ... )
        True
    """
    parsed = _parse_signature_header(signature_header) if signature_header else None
    if parsed is None:
        return False
    timestamp, provided = parsed
    if abs(int(time.time()) - int(timestamp)) > tolerance_seconds:
        return False
    expected = _expected_signature(secret, timestamp, payload)
    return hmac.compare_digest(expected, provided)


def unwrap_webhook(
    payload: Union[str, bytes],
    signature_header: str,
    secret: str,
    *,
    tolerance_seconds: int = DEFAULT_TOLERANCE_SECONDS,
) -> Dict[str, Any]:
    """Verify an inbound webhook and return its decoded JSON body.

    Same verification as :func:`verify_webhook_signature`, but raises on failure
    instead of returning ``False`` and returns the parsed event on success.

    Args:
        payload: The raw request body exactly as received (``str`` or ``bytes``).
        signature_header: The ``X-Webhook-Signature`` header value.
        secret: The webhook's signing secret.
        tolerance_seconds: Maximum allowed clock skew in seconds (default 300).

    Returns:
        The webhook event as a ``dict``.

    Raises:
        WebhookVerificationError: If the signature is missing, malformed,
            expired, or does not match, or the body is not a JSON object.

    Example:
        >>> event = unwrap_webhook(raw_body, header, "whsec_...")
        >>> event["event"]
        'memory.created'
    """
    if not verify_webhook_signature(
        payload, signature_header, secret, tolerance_seconds=tolerance_seconds
    ):
        raise WebhookVerificationError("Webhook signature verification failed")
    try:
        decoded = json.loads(_payload_bytes(payload))
    except json.JSONDecodeError as exc:
        raise WebhookVerificationError(f"Webhook payload is not valid JSON: {exc}") from exc
    if not isinstance(decoded, dict):
        raise WebhookVerificationError("Webhook payload is not a JSON object")
    return decoded
