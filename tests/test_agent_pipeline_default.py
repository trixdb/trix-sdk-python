"""Tests for agent pipeline management — account, space, resolve, triggers."""

import pytest
from unittest.mock import patch, AsyncMock

from trix import Trix, AsyncTrix


# ---------------------------------------------------------------------------
# Account-level default pipeline
# ---------------------------------------------------------------------------


class TestGetDefaultPipeline:
    """AgentResource.get_default_pipeline()"""

    def test_returns_name_when_set(self):
        with patch.object(Trix, "_request") as mock_request:
            mock_request.return_value = {"name": "longmem-v1"}
            client = Trix(api_key="test_key")
            assert client.agent.get_default_pipeline() == "longmem-v1"
            assert mock_request.call_args[0] == ("GET", "/pipeline-presets/_default")
            client.close()

    def test_returns_none_when_unset(self):
        with patch.object(Trix, "_request") as mock_request:
            mock_request.return_value = {"name": None}
            client = Trix(api_key="test_key")
            assert client.agent.get_default_pipeline() is None
            client.close()

    def test_returns_none_when_response_is_not_a_dict(self):
        with patch.object(Trix, "_request") as mock_request:
            mock_request.return_value = None
            client = Trix(api_key="test_key")
            assert client.agent.get_default_pipeline() is None
            client.close()


class TestSetDefaultPipeline:
    """AgentResource.set_default_pipeline()"""

    def test_sets_and_returns_name(self):
        with patch.object(Trix, "_request") as mock_request:
            mock_request.return_value = {"name": "longmem-v1"}
            client = Trix(api_key="test_key")
            result = client.agent.set_default_pipeline("longmem-v1")
            assert result == "longmem-v1"
            call_args = mock_request.call_args
            assert call_args[0] == ("POST", "/pipeline-presets/longmem-v1/set-default")
            assert call_args[1]["json"] == {}
            client.close()

    def test_falls_back_to_input_name_when_response_missing(self):
        with patch.object(Trix, "_request") as mock_request:
            mock_request.return_value = None
            client = Trix(api_key="test_key")
            assert client.agent.set_default_pipeline("foo") == "foo"
            client.close()


class TestClearDefaultPipeline:
    """AgentResource.clear_default_pipeline()"""

    def test_delete_call(self):
        with patch.object(Trix, "_request") as mock_request:
            mock_request.return_value = None
            client = Trix(api_key="test_key")
            result = client.agent.clear_default_pipeline()
            assert result is None
            assert mock_request.call_args[0] == ("DELETE", "/pipeline-presets/_default")
            client.close()


# ---------------------------------------------------------------------------
# Space-level default pipeline
# ---------------------------------------------------------------------------


class TestGetSpaceDefaultPipeline:
    """AgentResource.get_space_default_pipeline()"""

    def test_returns_name(self):
        with patch.object(Trix, "_request") as mock_request:
            mock_request.return_value = {"name": "space-preset"}
            client = Trix(api_key="test_key")
            assert client.agent.get_space_default_pipeline("space_abc") == "space-preset"
            assert mock_request.call_args[0][1] == "/spaces/space_abc/default-pipeline"
            client.close()

    def test_returns_none_when_unset(self):
        with patch.object(Trix, "_request") as mock_request:
            mock_request.return_value = {"name": None}
            client = Trix(api_key="test_key")
            assert client.agent.get_space_default_pipeline("space_abc") is None
            client.close()


class TestSetSpaceDefaultPipeline:
    """AgentResource.set_space_default_pipeline()"""

    def test_sets_and_returns_name(self):
        with patch.object(Trix, "_request") as mock_request:
            mock_request.return_value = {"name": "space-preset"}
            client = Trix(api_key="test_key")
            result = client.agent.set_space_default_pipeline("space_abc", "space-preset")
            assert result == "space-preset"
            call_args = mock_request.call_args
            assert call_args[0] == ("POST", "/spaces/space_abc/default-pipeline/space-preset")
            client.close()


class TestClearSpaceDefaultPipeline:
    """AgentResource.clear_space_default_pipeline()"""

    def test_delete_call(self):
        with patch.object(Trix, "_request") as mock_request:
            mock_request.return_value = None
            client = Trix(api_key="test_key")
            client.agent.clear_space_default_pipeline("space_abc")
            assert mock_request.call_args[0] == ("DELETE", "/spaces/space_abc/default-pipeline")
            client.close()


# ---------------------------------------------------------------------------
# Pipeline resolution (ADR-109a)
# ---------------------------------------------------------------------------


class TestResolvePipeline:
    """AgentResource.resolve_pipeline()"""

    def test_resolve_no_params(self):
        with patch.object(Trix, "_request") as mock_request:
            mock_request.return_value = {
                "name": "default-v1",
                "source": "account",
                "preset": {"steps": []},
            }
            client = Trix(api_key="test_key")
            result = client.agent.resolve_pipeline()
            assert result["name"] == "default-v1"
            assert result["source"] == "account"
            assert mock_request.call_args[0] == ("GET", "/pipeline-presets/_resolve")
            client.close()

    def test_resolve_with_space_and_pipeline(self):
        with patch.object(Trix, "_request") as mock_request:
            mock_request.return_value = {
                "name": "caller-preset",
                "source": "caller",
                "preset": {},
            }
            client = Trix(api_key="test_key")
            result = client.agent.resolve_pipeline(
                space_id="space_abc", pipeline="caller-preset"
            )
            assert result["source"] == "caller"
            params = mock_request.call_args[1]["params"]
            assert params["space_id"] == "space_abc"
            assert params["pipeline"] == "caller-preset"
            client.close()

    def test_resolve_returns_fallback_for_non_dict(self):
        with patch.object(Trix, "_request") as mock_request:
            mock_request.return_value = None
            client = Trix(api_key="test_key")
            result = client.agent.resolve_pipeline()
            assert result == {"name": None, "source": None, "preset": None}
            client.close()


# ---------------------------------------------------------------------------
# ADR-112 pipeline triggers
# ---------------------------------------------------------------------------


class TestSummarizeSession:
    """AgentResource.summarize_session()"""

    def test_summarize_basic(self):
        with patch.object(Trix, "_request") as mock_request:
            mock_request.return_value = {
                "session_id": "chat_123",
                "enqueued": True,
                "job_id": "job_001",
                "pipeline": None,
            }
            client = Trix(api_key="test_key")
            result = client.agent.summarize_session("chat_123")
            assert result["enqueued"] is True
            assert mock_request.call_args[0] == (
                "POST",
                "/agent/sessions/chat_123/summarize",
            )
            client.close()

    def test_summarize_with_pipeline(self):
        with patch.object(Trix, "_request") as mock_request:
            mock_request.return_value = {
                "session_id": "chat_123",
                "enqueued": True,
                "job_id": "job_002",
                "pipeline": "longmem-v1",
            }
            client = Trix(api_key="test_key")
            result = client.agent.summarize_session("chat_123", pipeline="longmem-v1")
            assert mock_request.call_args[1]["json"]["pipeline"] == "longmem-v1"
            assert result["pipeline"] == "longmem-v1"
            client.close()


class TestTriggerMegaSummary:
    """AgentResource.trigger_mega_summary()"""

    def test_trigger_basic(self):
        with patch.object(Trix, "_request") as mock_request:
            mock_request.return_value = {"enqueued": True, "job_id": "job_ms_1"}
            client = Trix(api_key="test_key")
            result = client.agent.trigger_mega_summary(scope_id="acc_123")
            assert result["enqueued"] is True
            json_data = mock_request.call_args[1]["json"]
            assert json_data == {"scope_id": "acc_123", "scope_type": "account"}
            assert mock_request.call_args[0] == ("POST", "/agent/mega-summary/trigger")
            client.close()

    def test_trigger_with_pipeline(self):
        with patch.object(Trix, "_request") as mock_request:
            mock_request.return_value = {"enqueued": True}
            client = Trix(api_key="test_key")
            client.agent.trigger_mega_summary(
                scope_id="acc_123", pipeline="mega-v2"
            )
            json_data = mock_request.call_args[1]["json"]
            assert json_data["pipeline"] == "mega-v2"
            client.close()


class TestTriggerScopedFacts:
    """AgentResource.trigger_scoped_facts()"""

    def test_trigger_basic(self):
        with patch.object(Trix, "_request") as mock_request:
            mock_request.return_value = {"enqueued": True, "job_id": "job_sf_1"}
            client = Trix(api_key="test_key")
            result = client.agent.trigger_scoped_facts(scope_id="chat_123")
            assert result["enqueued"] is True
            json_data = mock_request.call_args[1]["json"]
            assert json_data == {"scope_id": "chat_123", "scope_type": "session"}
            client.close()

    def test_trigger_with_scope_type_and_pipeline(self):
        with patch.object(Trix, "_request") as mock_request:
            mock_request.return_value = {"enqueued": True}
            client = Trix(api_key="test_key")
            client.agent.trigger_scoped_facts(
                scope_id="chat_123", scope_type="account", pipeline="facts-v2"
            )
            json_data = mock_request.call_args[1]["json"]
            assert json_data["scope_type"] == "account"
            assert json_data["pipeline"] == "facts-v2"
            client.close()


# ---------------------------------------------------------------------------
# Async mirrors
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
class TestAsyncPipeline:
    """Async variants of all pipeline methods."""

    async def test_get_default_pipeline(self):
        with patch.object(AsyncTrix, "_request", new_callable=AsyncMock) as mock_req:
            mock_req.return_value = {"name": "longmem-v1"}
            client = AsyncTrix(api_key="test_key")
            assert await client.agent.get_default_pipeline() == "longmem-v1"
            await client.close()

    async def test_set_default_pipeline(self):
        with patch.object(AsyncTrix, "_request", new_callable=AsyncMock) as mock_req:
            mock_req.return_value = {"name": "longmem-v1"}
            client = AsyncTrix(api_key="test_key")
            result = await client.agent.set_default_pipeline("longmem-v1")
            assert result == "longmem-v1"
            assert mock_req.call_args[0] == (
                "POST",
                "/pipeline-presets/longmem-v1/set-default",
            )
            await client.close()

    async def test_clear_default_pipeline(self):
        with patch.object(AsyncTrix, "_request", new_callable=AsyncMock) as mock_req:
            mock_req.return_value = None
            client = AsyncTrix(api_key="test_key")
            await client.agent.clear_default_pipeline()
            assert mock_req.call_args[0] == ("DELETE", "/pipeline-presets/_default")
            await client.close()

    async def test_get_space_default_pipeline(self):
        with patch.object(AsyncTrix, "_request", new_callable=AsyncMock) as mock_req:
            mock_req.return_value = {"name": "space-preset"}
            client = AsyncTrix(api_key="test_key")
            result = await client.agent.get_space_default_pipeline("space_abc")
            assert result == "space-preset"
            await client.close()

    async def test_set_space_default_pipeline(self):
        with patch.object(AsyncTrix, "_request", new_callable=AsyncMock) as mock_req:
            mock_req.return_value = {"name": "space-preset"}
            client = AsyncTrix(api_key="test_key")
            result = await client.agent.set_space_default_pipeline("space_abc", "space-preset")
            assert result == "space-preset"
            await client.close()

    async def test_clear_space_default_pipeline(self):
        with patch.object(AsyncTrix, "_request", new_callable=AsyncMock) as mock_req:
            mock_req.return_value = None
            client = AsyncTrix(api_key="test_key")
            await client.agent.clear_space_default_pipeline("space_abc")
            assert mock_req.call_args[0] == ("DELETE", "/spaces/space_abc/default-pipeline")
            await client.close()

    async def test_resolve_pipeline(self):
        with patch.object(AsyncTrix, "_request", new_callable=AsyncMock) as mock_req:
            mock_req.return_value = {
                "name": "default-v1",
                "source": "account",
                "preset": {},
            }
            client = AsyncTrix(api_key="test_key")
            result = await client.agent.resolve_pipeline(space_id="space_abc")
            assert result["name"] == "default-v1"
            await client.close()

    async def test_summarize_session(self):
        with patch.object(AsyncTrix, "_request", new_callable=AsyncMock) as mock_req:
            mock_req.return_value = {
                "session_id": "chat_123",
                "enqueued": True,
                "job_id": "job_001",
                "pipeline": None,
            }
            client = AsyncTrix(api_key="test_key")
            result = await client.agent.summarize_session("chat_123")
            assert result["enqueued"] is True
            await client.close()

    async def test_trigger_mega_summary(self):
        with patch.object(AsyncTrix, "_request", new_callable=AsyncMock) as mock_req:
            mock_req.return_value = {"enqueued": True, "job_id": "job_ms_1"}
            client = AsyncTrix(api_key="test_key")
            result = await client.agent.trigger_mega_summary(scope_id="acc_123")
            assert result["enqueued"] is True
            await client.close()

    async def test_trigger_scoped_facts(self):
        with patch.object(AsyncTrix, "_request", new_callable=AsyncMock) as mock_req:
            mock_req.return_value = {"enqueued": True, "job_id": "job_sf_1"}
            client = AsyncTrix(api_key="test_key")
            result = await client.agent.trigger_scoped_facts(scope_id="chat_123")
            assert result["enqueued"] is True
            await client.close()
