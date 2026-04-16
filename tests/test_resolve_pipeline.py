"""Tests for ADR-109a resolve_pipeline (tick 79)."""

from unittest.mock import patch

import pytest

from trix import AsyncTrix, Trix


class TestSyncResolvePipeline:
    def test_all_null_when_nothing_applies(self):
        with patch.object(Trix, "_request") as mock_request:
            mock_request.return_value = {"name": None, "source": None, "preset": None}
            client = Trix(api_key="test_key")
            result = client.agent.resolve_pipeline()

            assert result == {"name": None, "source": None, "preset": None}
            call_args = mock_request.call_args
            assert call_args[0] == ("GET", "/pipeline-presets/_resolve")
            # No params when both args are None
            assert call_args[1].get("params") is None
            client.close()

    def test_passes_caller_pipeline(self):
        with patch.object(Trix, "_request") as mock_request:
            mock_request.return_value = {
                "name": "longmem-v1",
                "source": "caller",
                "preset": {"name": "longmem-v1", "retrieval": {}},
            }
            client = Trix(api_key="test_key")
            result = client.agent.resolve_pipeline(pipeline="longmem-v1")

            assert result["source"] == "caller"
            assert result["name"] == "longmem-v1"
            call_args = mock_request.call_args
            assert call_args[1]["params"] == {"pipeline": "longmem-v1"}
            client.close()

    def test_passes_space_and_pipeline(self):
        with patch.object(Trix, "_request") as mock_request:
            mock_request.return_value = {
                "name": "space-pref",
                "source": "space",
                "preset": {"name": "space-pref"},
            }
            client = Trix(api_key="test_key")
            result = client.agent.resolve_pipeline(
                space_id="space-123",
                pipeline="caller-pref",
            )

            assert result["source"] == "space"
            call_args = mock_request.call_args
            params = call_args[1]["params"]
            assert params == {
                "space_id": "space-123",
                "pipeline": "caller-pref",
            }
            client.close()

    def test_handles_non_dict_response_defensively(self):
        with patch.object(Trix, "_request") as mock_request:
            mock_request.return_value = "unexpected"
            client = Trix(api_key="test_key")
            result = client.agent.resolve_pipeline()
            assert result == {"name": None, "source": None, "preset": None}
            client.close()


class TestAsyncResolvePipeline:
    @pytest.mark.asyncio
    async def test_async_resolve(self):
        captured = {}

        async def fake_request(method, path, params=None, json=None):
            captured["method"] = method
            captured["path"] = path
            captured["params"] = params
            return {
                "name": "longmem-v1",
                "source": "account",
                "preset": {"name": "longmem-v1"},
            }

        client = AsyncTrix(api_key="test_key")
        client._request = fake_request  # type: ignore[assignment]
        result = await client.agent.resolve_pipeline(space_id="my-space")

        assert result["source"] == "account"
        assert captured["method"] == "GET"
        assert captured["path"] == "/pipeline-presets/_resolve"
        assert captured["params"] == {"space_id": "my-space"}
        await client.close()
