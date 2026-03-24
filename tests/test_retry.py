"""Tests for retry logic with exponential backoff."""

import asyncio
from unittest.mock import patch

import pytest

from trix.exceptions import RateLimitError, ServerError
from trix.utils.retry import RetryConfig, retry_with_backoff


class TestRetryConfig:
    """Tests for RetryConfig."""

    def test_default_values(self):
        """Test default configuration values."""
        config = RetryConfig()
        assert config.max_retries == 3
        assert config.initial_delay == 1.0
        assert config.max_delay == 60.0
        assert config.exponential_base == 2.0
        assert config.jitter is True
        assert config.retryable_exceptions == {RateLimitError, ServerError}

    def test_custom_values(self):
        """Test custom configuration values."""
        config = RetryConfig(
            max_retries=5,
            initial_delay=0.5,
            max_delay=30.0,
            exponential_base=3.0,
            jitter=False,
            retryable_exceptions={ValueError},
        )
        assert config.max_retries == 5
        assert config.initial_delay == 0.5
        assert config.max_delay == 30.0
        assert config.exponential_base == 3.0
        assert config.jitter is False
        assert config.retryable_exceptions == {ValueError}


class TestCalculateDelay:
    """Tests for exponential backoff delay calculation."""

    def test_exponential_backoff_without_jitter(self):
        """Test delay increases exponentially without jitter."""
        config = RetryConfig(initial_delay=1.0, exponential_base=2.0, jitter=False)
        assert config.calculate_delay(0) == 1.0
        assert config.calculate_delay(1) == 2.0
        assert config.calculate_delay(2) == 4.0
        assert config.calculate_delay(3) == 8.0

    def test_max_delay_cap(self):
        """Test delay is capped at max_delay."""
        config = RetryConfig(initial_delay=1.0, max_delay=5.0, jitter=False)
        assert config.calculate_delay(10) == 5.0

    def test_retry_after_overrides_calculation(self):
        """Test retry_after from response overrides exponential backoff."""
        config = RetryConfig(initial_delay=1.0, jitter=False)
        assert config.calculate_delay(0, retry_after=30) == 30.0

    def test_jitter_adds_randomness(self):
        """Test jitter produces values in expected range."""
        config = RetryConfig(initial_delay=2.0, jitter=True)
        delays = {config.calculate_delay(0) for _ in range(50)}
        # With jitter: delay * (0.5 + random()) => range [1.0, 3.0)
        assert all(1.0 <= d < 3.0 for d in delays)
        # Should have some variation
        assert len(delays) > 1


class TestSyncRetry:
    """Tests for sync retry decorator."""

    @patch("trix.utils.retry.time.sleep")
    def test_success_on_first_attempt(self, mock_sleep):
        """Test function succeeds on first attempt without retries."""
        config = RetryConfig(max_retries=3, jitter=False)

        @retry_with_backoff(config)
        def succeed():
            return "ok"

        result = succeed()
        assert result == "ok"
        mock_sleep.assert_not_called()

    @patch("trix.utils.retry.time.sleep")
    def test_success_after_failures(self, mock_sleep):
        """Test function succeeds after transient failures."""
        config = RetryConfig(max_retries=3, initial_delay=1.0, jitter=False)
        call_count = 0

        @retry_with_backoff(config)
        def flaky():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise ServerError("Server error")
            return "recovered"

        result = flaky()
        assert result == "recovered"
        assert call_count == 3
        assert mock_sleep.call_count == 2

    @patch("trix.utils.retry.time.sleep")
    def test_exhaustion_raises(self, mock_sleep):
        """Test max retries exhaustion raises the last exception."""
        config = RetryConfig(max_retries=2, initial_delay=0.1, jitter=False)

        @retry_with_backoff(config)
        def always_fail():
            raise ServerError("persistent failure")

        with pytest.raises(ServerError, match="persistent failure"):
            always_fail()
        # Called max_retries + 1 times total, slept max_retries times
        assert mock_sleep.call_count == 2

    @patch("trix.utils.retry.time.sleep")
    def test_non_retryable_exception_not_retried(self, mock_sleep):
        """Test non-retryable exceptions are raised immediately."""
        config = RetryConfig(max_retries=3, retryable_exceptions={ServerError})

        @retry_with_backoff(config)
        def bad_input():
            raise ValueError("invalid input")

        with pytest.raises(ValueError, match="invalid input"):
            bad_input()
        mock_sleep.assert_not_called()

    @patch("trix.utils.retry.time.sleep")
    def test_rate_limit_uses_retry_after(self, mock_sleep):
        """Test RateLimitError uses retry_after for delay."""
        config = RetryConfig(max_retries=2, initial_delay=1.0, jitter=False)
        call_count = 0

        @retry_with_backoff(config)
        def rate_limited():
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                raise RateLimitError("rate limited", retry_after=42)
            return "ok"

        result = rate_limited()
        assert result == "ok"
        mock_sleep.assert_called_once_with(42.0)


async def _noop_sleep(delay):
    """No-op replacement for asyncio.sleep in tests."""
    pass


class TestAsyncRetry:
    """Tests for async retry decorator."""

    @pytest.mark.asyncio
    async def test_async_success_after_failures(self):
        """Test async function succeeds after transient failures."""
        config = RetryConfig(max_retries=3, initial_delay=0.01, jitter=False)
        call_count = 0

        @retry_with_backoff(config)
        async def flaky_async():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise ServerError("server error")
            return "recovered"

        with patch("trix.utils.retry.asyncio.sleep", side_effect=_noop_sleep):
            result = await flaky_async()
        assert result == "recovered"
        assert call_count == 3

    @pytest.mark.asyncio
    async def test_async_exhaustion_raises(self):
        """Test async max retries exhaustion raises the last exception."""
        config = RetryConfig(max_retries=1, initial_delay=0.01, jitter=False)

        @retry_with_backoff(config)
        async def always_fail_async():
            raise ServerError("persistent")

        with patch("trix.utils.retry.asyncio.sleep", side_effect=_noop_sleep):
            with pytest.raises(ServerError, match="persistent"):
                await always_fail_async()

    @pytest.mark.asyncio
    async def test_async_non_retryable_not_retried(self):
        """Test async non-retryable exceptions are raised immediately."""
        config = RetryConfig(max_retries=3, retryable_exceptions={ServerError})

        @retry_with_backoff(config)
        async def bad_async():
            raise TypeError("wrong type")

        with pytest.raises(TypeError, match="wrong type"):
            await bad_async()
