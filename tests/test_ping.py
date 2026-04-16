"""Tests for ADR-143 health-check ping() method on Trix and AsyncTrix."""

from unittest.mock import patch

import pytest

from trix import AsyncTrix, Trix
from trix.types import PingResult


class TestSyncPing:
    def test_returns_ok_when_server_reports_ok(self):
        with patch.object(Trix, "_request") as mock_request:
            mock_request.return_value = {
                "status": "ok",
                "version": "0.6.0",
                "uptime": 123.4,
                "timestamp": "2026-04-16T09:00:00Z",
            }
            client = Trix(api_key="test_key")
            result = client.ping()

            assert isinstance(result, PingResult)
            assert result.ok is True
            assert result.version == "0.6.0"
            assert isinstance(result.latency_ms, int)
            assert result.latency_ms >= 0
            call_args = mock_request.call_args
            assert call_args[0][0] == "GET"
            assert call_args[0][1] == "/health"
            client.close()

    def test_returns_not_ok_when_status_missing(self):
        with patch.object(Trix, "_request") as mock_request:
            mock_request.return_value = {"status": "degraded"}
            client = Trix(api_key="test_key")
            result = client.ping()

            assert result.ok is False
            assert result.version is None
            client.close()

    def test_returns_not_ok_on_unexpected_payload(self):
        with patch.object(Trix, "_request") as mock_request:
            mock_request.return_value = "not-a-dict"
            client = Trix(api_key="test_key")
            result = client.ping()

            assert result.ok is False
            assert result.version is None
            client.close()


class TestAsyncPing:
    @pytest.mark.asyncio
    async def test_returns_ok_when_server_reports_ok(self):
        async def fake_request(method, path, **kwargs):
            return {"status": "ok", "version": "0.6.0"}

        client = AsyncTrix(api_key="test_key")
        client._request = fake_request  # type: ignore[assignment]
        result = await client.ping()

        assert result.ok is True
        assert result.version == "0.6.0"
        assert isinstance(result.latency_ms, int)
        await client.close()

    @pytest.mark.asyncio
    async def test_returns_not_ok_on_failure(self):
        async def fake_request(method, path, **kwargs):
            return {"status": "down"}

        client = AsyncTrix(api_key="test_key")
        client._request = fake_request  # type: ignore[assignment]
        result = await client.ping()

        assert result.ok is False
        await client.close()
