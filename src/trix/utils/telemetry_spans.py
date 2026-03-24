"""
Request span implementations for OpenTelemetry integration.

Provides RequestSpan abstract base class and its implementations:
- NoOpRequestSpan: Does nothing when telemetry is disabled
- ActiveRequestSpan: Delegates to OpenTelemetry span when enabled
"""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from typing import Any, Optional, Union

logger = logging.getLogger(__name__)


class SpanProtocol:
    """Protocol for OpenTelemetry-compatible Span.

    Note: This is duplicated from telemetry.py to avoid circular imports.
    The actual protocol check happens at the telemetry module level.
    """

    def set_attribute(self, key: str, value: Union[str, int, float, bool]) -> None:
        """Set an attribute on the span."""
        ...

    def set_status(self, status: Any) -> None:
        """Set the status of the span."""
        ...

    def record_exception(self, exception: BaseException) -> None:
        """Record an exception on the span."""
        ...

    def end(self) -> None:
        """End the span."""
        ...


class RequestSpan(ABC):
    """Abstract base class for request span wrappers.

    This class defines the interface for request spans used in telemetry.
    Implementations include:
    - NoOpRequestSpan: Does nothing when telemetry is disabled
    - ActiveRequestSpan: Delegates to OpenTelemetry span when enabled
    """

    @abstractmethod
    def set_request_body(self, body: Any) -> None:
        """Set request body attribute (if enabled in config)."""
        ...

    @abstractmethod
    def set_status_code(self, code: int) -> None:
        """Set response status code."""
        ...

    @abstractmethod
    def set_response_body(self, body: Any) -> None:
        """Set response body attribute (if enabled in config)."""
        ...

    @abstractmethod
    def set_response_size(self, size: int) -> None:
        """Set response size in bytes."""
        ...

    @abstractmethod
    def record_error(self, error: BaseException) -> None:
        """Record an error."""
        ...

    @abstractmethod
    def success(self) -> None:
        """Mark span as successful and end it."""
        ...

    @abstractmethod
    def failure(self, message: Optional[str] = None) -> None:
        """Mark span as failed and end it."""
        ...

    @abstractmethod
    def set_attribute(self, key: str, value: Union[str, int, float, bool]) -> None:
        """Add custom attribute."""
        ...


class NoOpRequestSpan(RequestSpan):
    """No-op span implementation when telemetry is disabled.

    All methods are intentionally empty - this span does nothing when
    telemetry is not configured.
    """

    def set_request_body(self, body: Any) -> None:
        """No-op: telemetry disabled."""
        pass

    def set_status_code(self, code: int) -> None:
        """No-op: telemetry disabled."""
        pass

    def set_response_body(self, body: Any) -> None:
        """No-op: telemetry disabled."""
        pass

    def set_response_size(self, size: int) -> None:
        """No-op: telemetry disabled."""
        pass

    def record_error(self, error: BaseException) -> None:
        """No-op: telemetry disabled."""
        pass

    def success(self) -> None:
        """No-op: telemetry disabled."""
        pass

    def failure(self, message: Optional[str] = None) -> None:
        """No-op: telemetry disabled."""
        pass

    def set_attribute(self, key: str, value: Union[str, int, float, bool]) -> None:
        """No-op: telemetry disabled."""
        pass


class ActiveRequestSpan(RequestSpan):
    """Active span implementation."""

    def __init__(self, span: Any, config: Any) -> None:
        self._span = span
        self._config = config

    def set_request_body(self, body: Any) -> None:
        if self._config.record_request_body and body:
            try:
                import json

                body_str = body if isinstance(body, str) else json.dumps(body)
                # Truncate large bodies
                if len(body_str) > 1000:
                    body_str = body_str[:1000] + "..."
                self._span.set_attribute("http.request.body", body_str)
            except Exception as e:
                logger.debug("Failed to serialize for telemetry: %s", e)

    def set_status_code(self, code: int) -> None:
        self._span.set_attribute("http.status_code", code)

    def set_response_body(self, body: Any) -> None:
        if self._config.record_response_body and body:
            try:
                import json

                body_str = body if isinstance(body, str) else json.dumps(body)
                if len(body_str) > 1000:
                    body_str = body_str[:1000] + "..."
                self._span.set_attribute("http.response.body", body_str)
            except Exception as e:
                logger.debug("Failed to serialize for telemetry: %s", e)

    def set_response_size(self, size: int) -> None:
        self._span.set_attribute("http.response_content_length", size)

    def record_error(self, error: BaseException) -> None:
        self._span.record_exception(error)
        self._span.set_attribute("error.type", type(error).__name__)
        self._span.set_attribute("error.message", str(error))

    def success(self) -> None:
        try:
            from opentelemetry.trace import Status, StatusCode

            self._span.set_status(Status(StatusCode.OK))
        except ImportError:
            pass
        self._span.end()

    def failure(self, message: Optional[str] = None) -> None:
        try:
            from opentelemetry.trace import Status, StatusCode

            self._span.set_status(Status(StatusCode.ERROR, message))
        except ImportError:
            pass
        self._span.end()

    def set_attribute(self, key: str, value: Union[str, int, float, bool]) -> None:
        self._span.set_attribute(key, value)
