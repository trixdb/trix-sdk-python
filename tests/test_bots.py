"""Tests for Bots resource."""

import pytest

from tests.support import spec_async_client, spec_client
from trix.resources.bots import AsyncBotsResource, BotsResource

BOT_RESPONSE = {
    "id": "bot_123",
    "account_id": "acc_1",
    "name": "Summarizer",
    "slug": "summarizer",
    "system_prompt": "Summarize text.",
    "status": "active",
    "model": "gpt-4.1",
    "provider": "openai",
    "temperature": 0.7,
    "max_tokens": 2048,
    "memory_strategy": "search",
    "search_limit": 20,
    "max_turns_per_run": 5,
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z",
}

RUN_RESPONSE = {
    "id": "run_456",
    "bot_id": "bot_123",
    "account_id": "acc_1",
    "trigger_type": "manual",
    "status": "running",
    "created_at": "2024-01-01T00:00:00Z",
}


class TestBotsResource:
    """Tests for BotsResource (sync)."""

    def test_list_bots(self):
        """Test listing bots."""
        mock_client = spec_client()
        # Agents API returns the collection under the ``agents`` key.
        mock_client._request.return_value = {"agents": [BOT_RESPONSE]}

        resource = BotsResource(mock_client)
        result = resource.list()

        call_args = mock_client._request.call_args
        assert call_args[0] == ("GET", "/agents")
        assert call_args[1]["params"]["limit"] == 100
        assert len(result.bots) == 1

    def test_list_bots_with_status_filter(self):
        """Test listing bots filtered by status."""
        mock_client = spec_client()
        mock_client._request.return_value = {"bots": []}

        resource = BotsResource(mock_client)
        resource.list(status="active")

        call_args = mock_client._request.call_args
        assert call_args[1]["params"]["status"] == "active"

    def test_get_bot(self):
        """Test getting a bot by ID."""
        mock_client = spec_client()
        mock_client._request.return_value = BOT_RESPONSE

        resource = BotsResource(mock_client)
        result = resource.get("bot_123")

        call_args = mock_client._request.call_args
        assert call_args[0] == ("GET", "/agents/bot_123")
        assert result.id == "bot_123"
        assert result.name == "Summarizer"

    def test_create_bot(self):
        """Test creating a bot."""
        mock_client = spec_client()
        mock_client._request.return_value = BOT_RESPONSE

        resource = BotsResource(mock_client)
        result = resource.create(name="Summarizer", system_prompt="Summarize text.")

        call_args = mock_client._request.call_args
        assert call_args[0][0] == "POST"
        assert call_args[0][1] == "/agents"
        assert result.name == "Summarizer"

    def test_run_bot(self):
        """Test triggering a bot run."""
        mock_client = spec_client()
        mock_client._request.return_value = RUN_RESPONSE

        resource = BotsResource(mock_client)
        result = resource.run("bot_123", message="Summarize today")

        call_args = mock_client._request.call_args
        assert call_args[0] == ("POST", "/agents/bot_123/run")
        assert result.id == "run_456"
        assert result.status == "running"

    def test_list_runs(self):
        """Test listing bot runs."""
        mock_client = spec_client()
        mock_client._request.return_value = {"runs": [RUN_RESPONSE]}

        resource = BotsResource(mock_client)
        result = resource.list_runs("bot_123")

        call_args = mock_client._request.call_args
        assert call_args[0] == ("GET", "/agents/bot_123/runs")
        assert len(result.runs) == 1

    def test_get_run(self):
        """Test getting a specific bot run."""
        mock_client = spec_client()
        mock_client._request.return_value = {**RUN_RESPONSE, "status": "completed"}

        resource = BotsResource(mock_client)
        result = resource.get_run("bot_123", "run_456")

        call_args = mock_client._request.call_args
        assert call_args[0] == ("GET", "/agents/runs/run_456")
        assert result.status == "completed"

    def test_delete_bot(self):
        """Test deleting a bot."""
        mock_client = spec_client()
        mock_client._request.return_value = None

        resource = BotsResource(mock_client)
        resource.delete("bot_123")

        call_args = mock_client._request.call_args
        assert call_args[0] == ("DELETE", "/agents/bot_123")

    def test_update_bot(self):
        """Test updating a bot."""
        mock_client = spec_client()
        mock_client._request.return_value = {**BOT_RESPONSE, "name": "Updated Bot"}

        resource = BotsResource(mock_client)
        result = resource.update("bot_123", name="Updated Bot")

        call_args = mock_client._request.call_args
        assert call_args[0] == ("PATCH", "/agents/bot_123")
        assert result.name == "Updated Bot"


class TestAsyncBotsResource:
    """Tests for AsyncBotsResource."""

    @pytest.mark.asyncio
    async def test_list_bots(self):
        """Test listing bots asynchronously."""
        mock_client = spec_async_client()
        mock_client._request.return_value = {"agents": [BOT_RESPONSE]}

        resource = AsyncBotsResource(mock_client)
        result = await resource.list()

        mock_client._request.assert_called_once()
        assert len(result.bots) == 1

    @pytest.mark.asyncio
    async def test_run_bot(self):
        """Test triggering a bot run asynchronously."""
        mock_client = spec_async_client()
        mock_client._request.return_value = RUN_RESPONSE

        resource = AsyncBotsResource(mock_client)
        result = await resource.run("bot_123", message="Hello")

        mock_client._request.assert_called_once()
        assert result.status == "running"
