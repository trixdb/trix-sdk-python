"""Security utilities for Trix SDK."""

import os
import re
from typing import Any, Optional
from urllib.parse import urlparse

# Re-export validate_webhook_url for backwards compatibility
from .security_webhook import validate_webhook_url  # noqa: F401


# Pattern for valid resource IDs - alphanumeric, underscores, hyphens
ID_PATTERN = re.compile(r"^[a-zA-Z0-9_-]{1,255}$")

# Sensitive keys that should be redacted in logs
SENSITIVE_KEYS = frozenset(
    {
        "api_key",
        "apikey",
        "api-key",
        "token",
        "jwt_token",
        "jwt",
        "bearer",
        "password",
        "secret",
        "credential",
        "authorization",
        "auth",
    }
)


def validate_id(resource_id: str, resource_type: str = "resource") -> str:
    """
    Validate a resource ID to prevent path traversal attacks.

    Args:
        resource_id: The ID to validate
        resource_type: Type of resource for error messages

    Returns:
        The validated ID

    Raises:
        ValueError: If the ID is invalid
    """
    if not resource_id:
        raise ValueError(f"{resource_type} ID cannot be empty")

    if not isinstance(resource_id, str):
        raise ValueError(f"{resource_type} ID must be a string, got {type(resource_id).__name__}")

    # Check for path traversal attempts
    if ".." in resource_id or "/" in resource_id or "\\" in resource_id:
        raise ValueError(f"Invalid {resource_type} ID: contains path traversal characters")

    # Validate against pattern
    if not ID_PATTERN.match(resource_id):
        raise ValueError(
            f"Invalid {resource_type} ID: must be 1-255 characters, "
            "containing only letters, numbers, underscores, and hyphens"
        )

    return resource_id


def validate_base_url(url: str, allow_http: bool = False) -> str:
    """
    Validate a base URL for the API.

    Args:
        url: The URL to validate
        allow_http: Whether to allow HTTP (insecure, for local dev only)

    Returns:
        The validated URL (without trailing slash)

    Raises:
        ValueError: If the URL is invalid or insecure
    """
    if not url:
        raise ValueError("Base URL cannot be empty")

    try:
        parsed = urlparse(url)
    except Exception as e:
        raise ValueError(f"Invalid URL format: {e}")

    # Check scheme
    if not parsed.scheme:
        raise ValueError("URL must include a scheme (https://)")

    if parsed.scheme == "http":
        if not allow_http:
            raise ValueError(
                "HTTP is not allowed for security reasons. Use HTTPS. "
                "Set allow_http=True only for local development."
            )
    elif parsed.scheme != "https":
        raise ValueError(f"Invalid URL scheme '{parsed.scheme}'. Only HTTPS is allowed.")

    # Check host
    if not parsed.netloc:
        raise ValueError("URL must include a host")

    # Block localhost in production (unless allow_http is set)
    if not allow_http:
        host = parsed.netloc.lower().split(":")[0]
        if host in ("localhost", "127.0.0.1", "::1", "0.0.0.0"):
            raise ValueError(
                "Localhost URLs are not allowed in production. "
                "Set allow_http=True for local development."
            )

    return url.rstrip("/")


def redact_sensitive_data(data: Any, max_depth: int = 10) -> Any:
    """
    Redact sensitive data from a dictionary or object for safe logging.

    Args:
        data: Data to redact
        max_depth: Maximum recursion depth

    Returns:
        Data with sensitive values replaced with "[REDACTED]"
    """
    if max_depth <= 0:
        return "[MAX DEPTH EXCEEDED]"

    if isinstance(data, dict):
        return {
            key: (
                "[REDACTED]"
                if _is_sensitive_key(key)
                else redact_sensitive_data(value, max_depth - 1)
            )
            for key, value in data.items()
        }
    elif isinstance(data, (list, tuple)):
        return type(data)(redact_sensitive_data(item, max_depth - 1) for item in data)
    elif isinstance(data, str):
        # Redact Bearer tokens in strings
        if data.startswith("Bearer "):
            return "Bearer [REDACTED]"
        return data
    else:
        return data


def _is_sensitive_key(key: str) -> bool:
    """Check if a key name suggests sensitive data."""
    if not isinstance(key, str):
        return False
    key_lower = key.lower().replace("_", "").replace("-", "")
    return any(sensitive in key_lower for sensitive in SENSITIVE_KEYS)


def get_env_credential(
    env_var: str = "TRIX_API_KEY",
    required: bool = True,
) -> Optional[str]:
    """
    Get API credential from environment variable.

    Args:
        env_var: Environment variable name
        required: Whether to raise if not found

    Returns:
        The credential value or None

    Raises:
        ValueError: If required and not found
    """
    value = os.environ.get(env_var)

    if value is None and required:
        raise ValueError(
            f"Environment variable {env_var} is not set. "
            f"Either set {env_var} or pass api_key explicitly."
        )

    if value is not None:
        value = value.strip()
        if not value:
            if required:
                raise ValueError(f"Environment variable {env_var} is empty")
            return None

    return value


def mask_credential(credential: str, visible_chars: int = 4) -> str:
    """
    Mask a credential for display, showing only the last few characters.

    Args:
        credential: The credential to mask
        visible_chars: Number of characters to show at the end

    Returns:
        Masked credential like "****abcd"
    """
    if not credential:
        return "[EMPTY]"

    if len(credential) <= visible_chars:
        return "*" * len(credential)

    return "*" * (len(credential) - visible_chars) + credential[-visible_chars:]


def validate_limit(limit: int, max_limit: int = 1000, param_name: str = "limit") -> int:
    """
    Validate a limit parameter for pagination.

    Args:
        limit: The limit value to validate
        max_limit: Maximum allowed limit value
        param_name: Name of the parameter for error messages

    Returns:
        The validated limit

    Raises:
        ValueError: If the limit is invalid
    """
    if not isinstance(limit, int):
        raise ValueError(f"{param_name} must be an integer, got {type(limit).__name__}")

    if limit < 1:
        raise ValueError(f"{param_name} must be at least 1, got {limit}")

    if limit > max_limit:
        raise ValueError(f"{param_name} cannot exceed {max_limit}, got {limit}")

    return limit


def validate_offset(offset: int, param_name: str = "offset") -> int:
    """
    Validate an offset parameter for pagination.

    Args:
        offset: The offset value to validate
        param_name: Name of the parameter for error messages

    Returns:
        The validated offset

    Raises:
        ValueError: If the offset is invalid
    """
    if not isinstance(offset, int):
        raise ValueError(f"{param_name} must be an integer, got {type(offset).__name__}")

    if offset < 0:
        raise ValueError(f"{param_name} cannot be negative, got {offset}")

    return offset


def validate_threshold(
    threshold: float, min_value: float = 0.0, max_value: float = 1.0, param_name: str = "threshold"
) -> float:
    """
    Validate a threshold/confidence parameter.

    Args:
        threshold: The threshold value to validate
        min_value: Minimum allowed value (default: 0.0)
        max_value: Maximum allowed value (default: 1.0)
        param_name: Name of the parameter for error messages

    Returns:
        The validated threshold

    Raises:
        ValueError: If the threshold is invalid
    """
    if not isinstance(threshold, (int, float)):
        raise ValueError(f"{param_name} must be a number, got {type(threshold).__name__}")

    if threshold < min_value or threshold > max_value:
        raise ValueError(
            f"{param_name} must be between {min_value} and {max_value}, got {threshold}"
        )

    return float(threshold)


def validate_positive_int(value: int, param_name: str = "value", allow_zero: bool = False) -> int:
    """
    Validate a positive integer parameter.

    Args:
        value: The value to validate
        param_name: Name of the parameter for error messages
        allow_zero: Whether to allow zero as a valid value

    Returns:
        The validated value

    Raises:
        ValueError: If the value is invalid
    """
    if not isinstance(value, int):
        raise ValueError(f"{param_name} must be an integer, got {type(value).__name__}")

    if allow_zero:
        if value < 0:
            raise ValueError(f"{param_name} cannot be negative, got {value}")
    else:
        if value < 1:
            raise ValueError(f"{param_name} must be at least 1, got {value}")

    return value
