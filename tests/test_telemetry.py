"""Tests for telemetry module."""

from unittest.mock import MagicMock

import pytest

from trix.utils.telemetry import (
    ActiveRequestSpan,
    NoOpRequestSpan,
    RequestSpan,
    TelemetryConfig,
    configure_telemetry,
    create_request_span,
    get_telemetry_config,
    is_telemetry_enabled,
    traced,
    with_tracing,
)


class TestRequestSpanAbstract:
    """Test that RequestSpan is properly abstract."""

    def test_cannot_instantiate_abstract_class(self) -> None:
        """RequestSpan cannot be instantiated directly."""
        with pytest.raises(TypeError, match="abstract"):
            RequestSpan()  # type: ignore[abstract]


class TestNoOpRequestSpan:
    """Test NoOpRequestSpan implementation."""

    def test_set_request_body_does_nothing(self) -> None:
        """set_request_body should be a no-op."""
        span = NoOpRequestSpan()
        span.set_request_body({"key": "value"})  # Should not raise

    def test_set_status_code_does_nothing(self) -> None:
        """set_status_code should be a no-op."""
        span = NoOpRequestSpan()
        span.set_status_code(200)  # Should not raise

    def test_set_response_body_does_nothing(self) -> None:
        """set_response_body should be a no-op."""
        span = NoOpRequestSpan()
        span.set_response_body({"result": "data"})  # Should not raise

    def test_set_response_size_does_nothing(self) -> None:
        """set_response_size should be a no-op."""
        span = NoOpRequestSpan()
        span.set_response_size(1024)  # Should not raise

    def test_record_error_does_nothing(self) -> None:
        """record_error should be a no-op."""
        span = NoOpRequestSpan()
        span.record_error(ValueError("test error"))  # Should not raise

    def test_success_does_nothing(self) -> None:
        """success should be a no-op."""
        span = NoOpRequestSpan()
        span.success()  # Should not raise

    def test_failure_does_nothing(self) -> None:
        """failure should be a no-op."""
        span = NoOpRequestSpan()
        span.failure("error message")  # Should not raise
        span.failure()  # Also with no message

    def test_set_attribute_does_nothing(self) -> None:
        """set_attribute should be a no-op."""
        span = NoOpRequestSpan()
        span.set_attribute("key", "value")  # Should not raise
        span.set_attribute("count", 42)  # Should not raise


class TestActiveRequestSpan:
    """Test ActiveRequestSpan implementation."""

    def _create_mock_span(self) -> MagicMock:
        """Create a mock span for testing."""
        mock = MagicMock()
        mock.set_attribute = MagicMock()
        mock.set_status = MagicMock()
        mock.record_exception = MagicMock()
        mock.end = MagicMock()
        return mock

    def test_set_status_code(self) -> None:
        """set_status_code should set http.status_code attribute."""
        mock_span = self._create_mock_span()
        config = TelemetryConfig()
        span = ActiveRequestSpan(mock_span, config)

        span.set_status_code(200)

        mock_span.set_attribute.assert_called_with("http.status_code", 200)

    def test_set_response_size(self) -> None:
        """set_response_size should set http.response_content_length attribute."""
        mock_span = self._create_mock_span()
        config = TelemetryConfig()
        span = ActiveRequestSpan(mock_span, config)

        span.set_response_size(1024)

        mock_span.set_attribute.assert_called_with("http.response_content_length", 1024)

    def test_set_attribute(self) -> None:
        """set_attribute should delegate to underlying span."""
        mock_span = self._create_mock_span()
        config = TelemetryConfig()
        span = ActiveRequestSpan(mock_span, config)

        span.set_attribute("custom.key", "custom_value")

        mock_span.set_attribute.assert_called_with("custom.key", "custom_value")

    def test_record_error(self) -> None:
        """record_error should record exception and set error attributes."""
        mock_span = self._create_mock_span()
        config = TelemetryConfig()
        span = ActiveRequestSpan(mock_span, config)

        error = ValueError("test error message")
        span.record_error(error)

        mock_span.record_exception.assert_called_once_with(error)
        calls = mock_span.set_attribute.call_args_list
        assert any(c[0] == ("error.type", "ValueError") for c in calls)
        assert any(c[0] == ("error.message", "test error message") for c in calls)

    def test_set_request_body_disabled(self) -> None:
        """set_request_body should not set attribute when disabled."""
        mock_span = self._create_mock_span()
        config = TelemetryConfig(record_request_body=False)
        span = ActiveRequestSpan(mock_span, config)

        span.set_request_body({"key": "value"})

        mock_span.set_attribute.assert_not_called()

    def test_set_request_body_enabled(self) -> None:
        """set_request_body should set attribute when enabled."""
        mock_span = self._create_mock_span()
        config = TelemetryConfig(record_request_body=True)
        span = ActiveRequestSpan(mock_span, config)

        span.set_request_body({"key": "value"})

        mock_span.set_attribute.assert_called_once()
        call_args = mock_span.set_attribute.call_args[0]
        assert call_args[0] == "http.request.body"
        assert "key" in call_args[1]

    def test_set_request_body_truncates_large_body(self) -> None:
        """set_request_body should truncate bodies larger than 1000 chars."""
        mock_span = self._create_mock_span()
        config = TelemetryConfig(record_request_body=True)
        span = ActiveRequestSpan(mock_span, config)

        large_body = "x" * 2000
        span.set_request_body(large_body)

        call_args = mock_span.set_attribute.call_args[0]
        assert len(call_args[1]) < 1010  # 1000 + "..."
        assert call_args[1].endswith("...")

    def test_set_response_body_disabled(self) -> None:
        """set_response_body should not set attribute when disabled."""
        mock_span = self._create_mock_span()
        config = TelemetryConfig(record_response_body=False)
        span = ActiveRequestSpan(mock_span, config)

        span.set_response_body({"result": "data"})

        mock_span.set_attribute.assert_not_called()

    def test_set_response_body_enabled(self) -> None:
        """set_response_body should set attribute when enabled."""
        mock_span = self._create_mock_span()
        config = TelemetryConfig(record_response_body=True)
        span = ActiveRequestSpan(mock_span, config)

        span.set_response_body({"result": "data"})

        mock_span.set_attribute.assert_called_once()
        call_args = mock_span.set_attribute.call_args[0]
        assert call_args[0] == "http.response.body"

    def test_success_ends_span(self) -> None:
        """success should end the span."""
        mock_span = self._create_mock_span()
        config = TelemetryConfig()
        span = ActiveRequestSpan(mock_span, config)

        span.success()

        mock_span.end.assert_called_once()

    def test_failure_ends_span(self) -> None:
        """failure should end the span."""
        mock_span = self._create_mock_span()
        config = TelemetryConfig()
        span = ActiveRequestSpan(mock_span, config)

        span.failure("error occurred")

        mock_span.end.assert_called_once()


class TestTelemetryConfiguration:
    """Test telemetry configuration functions."""

    def test_default_config_disabled(self) -> None:
        """Telemetry should be disabled by default."""
        # Reset to default
        configure_telemetry()
        assert not is_telemetry_enabled()

    def test_configure_enables_telemetry(self) -> None:
        """Configuring with a tracer should enable telemetry."""
        mock_tracer = MagicMock()
        configure_telemetry(tracer=mock_tracer)

        assert is_telemetry_enabled()
        config = get_telemetry_config()
        assert config.tracer is mock_tracer

        # Clean up
        configure_telemetry()

    def test_configure_sets_all_options(self) -> None:
        """configure_telemetry should set all configuration options."""
        mock_tracer = MagicMock()
        configure_telemetry(
            tracer=mock_tracer,
            record_request_body=True,
            record_response_body=True,
            span_name_prefix="custom",
            default_attributes={"env": "test"},
        )

        config = get_telemetry_config()
        assert config.tracer is mock_tracer
        assert config.record_request_body is True
        assert config.record_response_body is True
        assert config.span_name_prefix == "custom"
        assert config.default_attributes == {"env": "test"}

        # Clean up
        configure_telemetry()


class TestCreateRequestSpan:
    """Test create_request_span function."""

    def test_returns_noop_when_disabled(self) -> None:
        """Should return NoOpRequestSpan when telemetry is disabled."""
        configure_telemetry()  # Reset to disabled

        span = create_request_span("GET", "/api/test", "test.operation")

        assert isinstance(span, NoOpRequestSpan)

    def test_returns_active_when_enabled(self) -> None:
        """Should return ActiveRequestSpan when telemetry is enabled."""
        mock_tracer = MagicMock()
        mock_span = MagicMock()
        mock_tracer.start_span.return_value = mock_span
        configure_telemetry(tracer=mock_tracer)

        span = create_request_span("GET", "/api/test", "test.operation")

        assert isinstance(span, ActiveRequestSpan)

        # Clean up
        configure_telemetry()


class TestWithTracing:
    """Test with_tracing context manager."""

    def test_yields_span(self) -> None:
        """with_tracing should yield a span."""
        configure_telemetry()  # Disabled, will yield NoOpRequestSpan

        with with_tracing("test.operation") as span:
            assert isinstance(span, RequestSpan)

    def test_calls_success_on_normal_exit(self) -> None:
        """with_tracing should call success when block completes normally."""
        mock_tracer = MagicMock()
        mock_span = MagicMock()
        mock_tracer.start_span.return_value = mock_span
        configure_telemetry(tracer=mock_tracer)

        with with_tracing("test.operation"):
            pass

        mock_span.end.assert_called_once()

        # Clean up
        configure_telemetry()

    def test_calls_failure_on_exception(self) -> None:
        """with_tracing should call failure and re-raise on exception."""
        mock_tracer = MagicMock()
        mock_span = MagicMock()
        mock_tracer.start_span.return_value = mock_span
        configure_telemetry(tracer=mock_tracer)

        with pytest.raises(ValueError, match="test error"):
            with with_tracing("test.operation"):
                raise ValueError("test error")

        mock_span.record_exception.assert_called_once()
        mock_span.end.assert_called_once()

        # Clean up
        configure_telemetry()


class TestTracedDecorator:
    """Test traced decorator."""

    def test_traces_sync_function(self) -> None:
        """traced should wrap sync functions with tracing."""
        configure_telemetry()  # Disabled

        @traced("test.sync")
        def sync_func() -> str:
            return "result"

        result = sync_func()
        assert result == "result"

    async def test_traces_async_function(self) -> None:
        """traced should wrap async functions with tracing."""
        configure_telemetry()  # Disabled

        @traced("test.async")
        async def async_func() -> str:
            return "async result"

        result = await async_func()
        assert result == "async result"

    def test_propagates_exception_sync(self) -> None:
        """traced should propagate exceptions from sync functions."""
        configure_telemetry()

        @traced("test.error")
        def error_func() -> None:
            raise ValueError("sync error")

        with pytest.raises(ValueError, match="sync error"):
            error_func()

    async def test_propagates_exception_async(self) -> None:
        """traced should propagate exceptions from async functions."""
        configure_telemetry()

        @traced("test.error")
        async def error_func() -> None:
            raise ValueError("async error")

        with pytest.raises(ValueError, match="async error"):
            await error_func()
