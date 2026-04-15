"""Tests for the ADR-109a account-default pipeline methods on AgentResource."""

from unittest.mock import patch, AsyncMock

import pytest

from trix import Trix, AsyncTrix


class TestGetDefaultPipeline:
    """AgentResource.get_default_pipeline()"""

    def test_returns_name_when_set(self):
        with patch.object(Trix, "_request") as mock_request:
            mock_request.return_value = {"name": "longmem-v1"}
            client = Trix(api_key="test_key")
            assert client.agent.get_default_pipeline() == "longmem-v1"
            call_args = mock_request.call_args
            assert call_args[0][0] == "GET"
            assert call_args[0][1] == "/pipeline-presets/_default"

    def test_returns_none_when_unset(self):
        with patch.object(Trix, "_request") as mock_request:
            mock_request.return_value = {"name": None}
            client = Trix(api_key="test_key")
            assert client.agent.get_default_pipeline() is None

    def test_returns_none_when_response_is_not_a_dict(self):
        with patch.object(Trix, "_request") as mock_request:
            mock_request.return_value = None
            client = Trix(api_key="test_key")
            assert client.agent.get_default_pipeline() is None


class TestSetDefaultPipeline:
    """AgentResource.set_default_pipeline()"""

    def test_sets_and_returns_name(self):
        with patch.object(Trix, "_request") as mock_request:
            mock_request.return_value = {"name": "longmem-v1"}
            client = Trix(api_key="test_key")
            result = client.agent.set_default_pipeline("longmem-v1")
            assert result == "longmem-v1"
            call_args = mock_request.call_args
            assert call_args[0][0] == "POST"
            assert call_args[0][1] == "/pipeline-presets/longmem-v1/set-default"
            # Body is empty object per the API contract
            assert call_args[1]["json"] == {}

    def test_falls_back_to_input_name_when_response_missing(self):
        # Defensive path — unusual response shape shouldn't crash the caller.
        with patch.object(Trix, "_request") as mock_request:
            mock_request.return_value = None
            client = Trix(api_key="test_key")
            assert client.agent.set_default_pipeline("foo") == "foo"


class TestClearDefaultPipeline:
    """AgentResource.clear_default_pipeline()"""

    def test_delete_call(self):
        with patch.object(Trix, "_request") as mock_request:
            mock_request.return_value = None
            client = Trix(api_key="test_key")
            # Returns None; primary assertion is the DELETE call shape.
            result = client.agent.clear_default_pipeline()
            assert result is None
            call_args = mock_request.call_args
            assert call_args[0][0] == "DELETE"
            assert call_args[0][1] == "/pipeline-presets/_default"


@pytest.mark.asyncio
class TestAsyncDefaultPipeline:
    """Async mirror of the above (AsyncAgentResource)."""

    async def test_get_default_pipeline_name(self):
        with patch.object(AsyncTrix, "_request", new_callable=AsyncMock) as mock_request:
            mock_request.return_value = {"name": "longmem-v1"}
            client = AsyncTrix(api_key="test_key")
            assert await client.agent.get_default_pipeline() == "longmem-v1"

    async def test_set_default_pipeline(self):
        with patch.object(AsyncTrix, "_request", new_callable=AsyncMock) as mock_request:
            mock_request.return_value = {"name": "longmem-v1"}
            client = AsyncTrix(api_key="test_key")
            result = await client.agent.set_default_pipeline("longmem-v1")
            assert result == "longmem-v1"
            call_args = mock_request.call_args
            assert call_args[0][0] == "POST"
            assert call_args[0][1] == "/pipeline-presets/longmem-v1/set-default"

    async def test_clear_default_pipeline(self):
        with patch.object(AsyncTrix, "_request", new_callable=AsyncMock) as mock_request:
            mock_request.return_value = None
            client = AsyncTrix(api_key="test_key")
            await client.agent.clear_default_pipeline()
            call_args = mock_request.call_args
            assert call_args[0][0] == "DELETE"
            assert call_args[0][1] == "/pipeline-presets/_default"
