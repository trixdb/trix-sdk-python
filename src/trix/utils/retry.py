"""Retry logic with exponential backoff for Trix SDK."""

import asyncio
import logging
import random
import time
from functools import wraps
from typing import Any, Callable, Optional, Set, Type, TypeVar, cast

import httpx

from ..exceptions import APIError, ConnectionError, RateLimitError, ServerError, TimeoutError

logger = logging.getLogger(__name__)

T = TypeVar("T")


class RetryConfig:
    """Configuration for retry behavior."""

    def __init__(
        self,
        max_retries: int = 3,
        initial_delay: float = 1.0,
        max_delay: float = 60.0,
        exponential_base: float = 2.0,
        jitter: bool = True,
        retryable_exceptions: Optional[Set[Type[Exception]]] = None,
    ) -> None:
        """
        Initialize retry configuration.

        Args:
            max_retries: Maximum number of retry attempts
            initial_delay: Initial delay in seconds before first retry
            max_delay: Maximum delay in seconds between retries
            exponential_base: Base for exponential backoff calculation
            jitter: Whether to add random jitter to delays
            retryable_exceptions: Set of exception types that should trigger retries
        """
        self.max_retries = max_retries
        self.initial_delay = initial_delay
        self.max_delay = max_delay
        self.exponential_base = exponential_base
        self.jitter = jitter
        self.retryable_exceptions = retryable_exceptions or {
            RateLimitError,
            ServerError,
        }

    def calculate_delay(self, attempt: int, retry_after: Optional[int] = None) -> float:
        """
        Calculate delay before next retry.

        Args:
            attempt: Current retry attempt number (0-indexed)
            retry_after: Optional retry-after value from response headers

        Returns:
            Delay in seconds
        """
        if retry_after is not None:
            return float(retry_after)

        delay = min(
            self.initial_delay * (self.exponential_base**attempt),
            self.max_delay,
        )

        if self.jitter:
            delay = delay * (0.5 + random.random())

        return delay


def is_retryable(error: BaseException, config: RetryConfig) -> bool:
    """Return True if ``error`` matches one of the config's retryable types.

    Single source of truth for the retryable-exceptions policy, shared by the
    transport retry loop and the ``retry_with_backoff`` decorator so a custom
    ``RetryConfig(retryable_exceptions=...)`` actually governs both.
    """
    return isinstance(error, tuple(config.retryable_exceptions))


def coerce_httpx_error(error: httpx.HTTPError) -> Exception:
    """Map a raw ``httpx`` transport error onto the SDK's typed exception.

    Lets the transport funnel timeouts/network/HTTP failures through the same
    retryable-exceptions check as server-side errors.
    """
    if isinstance(error, httpx.TimeoutException):
        return TimeoutError(f"Request timed out: {error}")
    if isinstance(error, httpx.NetworkError):
        return ConnectionError(f"Network error: {error}")
    return APIError(f"HTTP error: {error}")


def retry_with_backoff(
    config: Optional[RetryConfig] = None,
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """
    Decorator for retrying functions with exponential backoff.

    Args:
        config: Retry configuration (uses defaults if not provided)

    Returns:
        Decorated function with retry logic
    """
    if config is None:
        config = RetryConfig()

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        if asyncio.iscoroutinefunction(func):

            @wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> T:
                last_exception: Optional[Exception] = None

                for attempt in range(config.max_retries + 1):
                    try:
                        return cast(T, await func(*args, **kwargs))
                    except Exception as e:
                        last_exception = e

                        # Don't retry if it's not a retryable exception
                        if not is_retryable(e, config):
                            raise

                        # Don't retry if we've exhausted attempts
                        if attempt >= config.max_retries:
                            raise

                        # Calculate delay
                        retry_after = None
                        if isinstance(e, RateLimitError):
                            retry_after = e.retry_after

                        delay = config.calculate_delay(attempt, retry_after)

                        logger.warning(
                            f"Attempt {attempt + 1}/{config.max_retries + 1} failed: {e}. "
                            f"Retrying in {delay:.2f}s..."
                        )

                        await asyncio.sleep(delay)

                # Should never reach here, but satisfy type checker
                if last_exception:
                    raise last_exception
                raise RuntimeError("Retry logic failed unexpectedly")

            return cast(Callable[..., T], async_wrapper)
        else:

            @wraps(func)
            def sync_wrapper(*args: Any, **kwargs: Any) -> T:
                last_exception: Optional[Exception] = None

                for attempt in range(config.max_retries + 1):
                    try:
                        return func(*args, **kwargs)
                    except Exception as e:
                        last_exception = e

                        # Don't retry if it's not a retryable exception
                        if not is_retryable(e, config):
                            raise

                        # Don't retry if we've exhausted attempts
                        if attempt >= config.max_retries:
                            raise

                        # Calculate delay
                        retry_after = None
                        if isinstance(e, RateLimitError):
                            retry_after = e.retry_after

                        delay = config.calculate_delay(attempt, retry_after)

                        logger.warning(
                            f"Attempt {attempt + 1}/{config.max_retries + 1} failed: {e}. "
                            f"Retrying in {delay:.2f}s..."
                        )
                        time.sleep(delay)

                # Should never reach here, but satisfy type checker
                if last_exception:
                    raise last_exception
                raise RuntimeError("Retry logic failed unexpectedly")

            return cast(Callable[..., T], sync_wrapper)

    return decorator
