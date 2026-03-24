"""Webhook URL validation for Trix SDK.

Provides SSRF-safe webhook URL validation with checks for:
- HTTPS requirement
- Private/internal IP blocking (IPv4 and IPv6)
- Cloud metadata service blocking
- IPv4-mapped IPv6 address detection
"""

import re
from urllib.parse import urlparse


def validate_webhook_url(url: str) -> str:
    """
    Validate a webhook URL.

    Args:
        url: The webhook URL to validate

    Returns:
        The validated URL

    Raises:
        ValueError: If the URL is invalid or insecure
    """
    if not url:
        raise ValueError("Webhook URL cannot be empty")

    try:
        parsed = urlparse(url)
    except Exception as e:
        raise ValueError(f"Invalid webhook URL format: {e}")

    # Must be HTTPS
    if parsed.scheme != "https":
        raise ValueError("Webhook URL must use HTTPS for security")

    if not parsed.netloc:
        raise ValueError("Webhook URL must include a host")

    # Block internal/private IPs
    # Use parsed.hostname to correctly handle IPv6 addresses
    host = parsed.hostname
    if not host:
        raise ValueError("Webhook URL must include a host")

    # Normalize: lowercase and strip brackets for IPv6
    normalized_host = host.lower().strip("[]")

    # Block localhost variants
    if normalized_host in ("localhost", "0.0.0.0"):
        raise ValueError("Webhook URL cannot point to localhost")

    # Block IPv4 loopback (127.0.0.0/8)
    if normalized_host.startswith("127."):
        raise ValueError("Webhook URL cannot point to localhost")

    # Block IPv6 loopback (::1)
    if normalized_host == "::1":
        raise ValueError("Webhook URL cannot point to localhost")

    # Block IPv6 zero address (::)
    if normalized_host in ("::", "0:0:0:0:0:0:0:0"):
        raise ValueError("Webhook URL cannot point to the zero address")

    _check_private_ipv4(normalized_host)
    _check_private_ipv6(normalized_host)

    return url


def _check_private_ipv4(normalized_host: str) -> None:
    """Check and block private IPv4 ranges."""
    # 10.0.0.0/8
    if normalized_host.startswith("10."):
        raise ValueError("Webhook URL cannot point to private IP addresses")

    # 192.168.0.0/16
    if normalized_host.startswith("192.168."):
        raise ValueError("Webhook URL cannot point to private IP addresses")

    # 172.16.0.0/12 (172.16.0.0 - 172.31.255.255)
    if normalized_host.startswith("172."):
        parts = normalized_host.split(".")
        if len(parts) >= 2 and parts[1].isdigit():
            second_octet = int(parts[1])
            if 16 <= second_octet <= 31:
                raise ValueError("Webhook URL cannot point to private IP addresses")

    # Block link-local addresses (169.254.0.0/16)
    if normalized_host.startswith("169.254."):
        raise ValueError("Webhook URL cannot point to link-local addresses")

    # Block AWS/cloud metadata service
    if normalized_host == "169.254.169.254":
        raise ValueError("Webhook URL cannot point to metadata service")


def _check_private_ipv6(normalized_host: str) -> None:
    """Check and block private IPv6 ranges."""
    # fc00::/7 (Unique Local Addresses - includes fc and fd prefixes)
    if normalized_host.startswith("fc") or normalized_host.startswith("fd"):
        raise ValueError("Webhook URL cannot point to private IPv6 addresses")

    # fe80::/10 (Link-local addresses)
    if (
        normalized_host.startswith("fe8")
        or normalized_host.startswith("fe9")
        or normalized_host.startswith("fea")
        or normalized_host.startswith("feb")
    ):
        raise ValueError("Webhook URL cannot point to IPv6 link-local addresses")

    # Block IPv4-mapped IPv6 addresses (::ffff:x.x.x.x)
    if "ffff:" in normalized_host.lower():
        _check_ipv4_mapped_ipv6(normalized_host)

    # Block site-local addresses (deprecated but still valid: fec0::/10)
    if (
        normalized_host.startswith("fec")
        or normalized_host.startswith("fed")
        or normalized_host.startswith("fee")
        or normalized_host.startswith("fef")
    ):
        raise ValueError("Webhook URL cannot point to deprecated IPv6 site-local addresses")


def _check_ipv4_mapped_ipv6(normalized_host: str) -> None:
    """Check IPv4-mapped IPv6 addresses for private ranges."""
    ipv4_match = re.search(r"::ffff:(\d+\.\d+\.\d+\.\d+)$", normalized_host, re.IGNORECASE)
    if not ipv4_match:
        ipv4_match = re.search(r":ffff:(\d+\.\d+\.\d+\.\d+)$", normalized_host, re.IGNORECASE)
    if ipv4_match:
        ipv4 = ipv4_match.group(1)
        if (
            ipv4.startswith("127.")
            or ipv4.startswith("10.")
            or ipv4.startswith("192.168.")
            or ipv4.startswith("169.254.")
            or ipv4 == "0.0.0.0"
        ):
            raise ValueError("Webhook URL cannot point to private IPv4-mapped IPv6 addresses")
        if ipv4.startswith("172."):
            parts = ipv4.split(".")
            if len(parts) >= 2 and parts[1].isdigit():
                second_octet = int(parts[1])
                if 16 <= second_octet <= 31:
                    raise ValueError(
                        "Webhook URL cannot point to private IPv4-mapped IPv6 addresses"
                    )
