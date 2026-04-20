"""Tests for agent resource — session lifecycle, memory, context, errors."""

import pytest
from unittest.mock import patch, AsyncMock

from trix import Trix, AsyncTrix
from trix.types import (
    AgentSession,
    SessionMemory,
    SessionMemoryList,
    SessionMessage,
    SessionList,
    AgentContext,
)


# ---------------------------------------------------------------------------
# Mock response data
# ---------------------------------------------------------------------------

MOCK_AGENT_SESSION = {
    "session_id": "chat_123",
    "space_id": "space_abc",
    "metadata": {"user_id": "user_456"},
    "created_at": "2025-01-15T10:00:00Z",
    "ended_at": None,
    "summary": None,
}

MOCK_AGENT_SESSION_ENDED = {
    **MOCK_AGENT_SESSION,
    "ended_at": "2025-01-15T11:00:00Z",
    "summary": "Discussed Python best practices",
}

MOCK_SESSION_MEMORY = {
    "id": "mem_001",
    "session_id": "chat_123",
    "content": "User asked about Python",
    "role": "user",
    "importance": 0.8,
    "created_at": "2025-01-15T10:01:00Z",
}

MOCK_SESSION_MEMORY_LIST = {
    "data": [MOCK_SESSION_MEMORY],
    "total": 1,
}

MOCK_SESSION_MESSAGE = {
    "id": "mem_abc123",
    "session_id": "chat_123",
    "role": "user",
    "content": "What is the weather today?",
    "created_at": "2025-01-15T10:00:00Z",
    "turn_number": 1,
}

MOCK_SESSION_LIST = {
    "data": [MOCK_AGENT_SESSION],
}

MOCK_MEMORY_RESPONSE = {
    "id": "mem_999",
    "content": "Long-term memory about Python",
    "type": "text",
    "tags": ["python"],
    "created_at": "2025-01-01T00:00:00Z",
    "updated_at": "2025-01-01T00:00:00Z",
    "access_count": 2,
}

MOCK_AGENT_CONTEXT = {
    "query": "Tell me about Python",
    "memories": [MOCK_MEMORY_RESPONSE],
    "session_memories": [MOCK_SESSION_MEMORY],
    "relevance_scores": {"mem_999": 0.92, "mem_001": 0.85},
}


# ---------------------------------------------------------------------------
# Session lifecycle — create
# ---------------------------------------------------------------------------


class TestCreateSession:
    """Tests for agent.create_session()."""

    def test_create_basic(self):
        with patch.object(Trix, "_request") as mock_request:
            mock_request.return_value = MOCK_AGENT_SESSION
            client = Trix(api_key="test_key")
            session = client.agent.create_session(session_id="chat_123")
            assert isinstance(session, AgentSession)
            assert session.session_id == "chat_123"
            assert session.ended_at is None
            assert mock_request.call_args[0] == ("POST", "/agent/sessions")
            assert "space_id" not in mock_request.call_args[1]["json"]
            client.close()

    def test_create_with_all_options(self):
        with patch.object(Trix, "_request") as mock_request:
            mock_request.return_value = MOCK_AGENT_SESSION
            client = Trix(api_key="test_key")
            session = client.agent.create_session(
                session_id="chat_123", space_id="space_abc",
                metadata={"user_id": "user_456"},
            )
            assert session.space_id == "space_abc"
            json_data = mock_request.call_args[1]["json"]
            assert json_data["space_id"] == "space_abc"
            assert json_data["metadata"] == {"user_id": "user_456"}
            client.close()

    def test_create_validates_empty_ids(self):
        with patch.object(Trix, "_request"):
            client = Trix(api_key="test_key")
            with pytest.raises(Exception):
                client.agent.create_session(session_id="")
            with pytest.raises(Exception):
                client.agent.create_session(session_id="chat_1", space_id="")
            client.close()

    @pytest.mark.asyncio
    async def test_create_async(self):
        with patch.object(AsyncTrix, "_request", new_callable=AsyncMock) as mock_req:
            mock_req.return_value = MOCK_AGENT_SESSION
            client = AsyncTrix(api_key="test_key")
            session = await client.agent.create_session(
                session_id="chat_123", space_id="space_abc"
            )
            assert isinstance(session, AgentSession)
            await client.close()


# ---------------------------------------------------------------------------
# Session lifecycle — get
# ---------------------------------------------------------------------------


class TestGetSession:
    """Tests for agent.get_session()."""

    def test_get_basic(self):
        with patch.object(Trix, "_request") as mock_request:
            mock_request.return_value = MOCK_SESSION_MEMORY_LIST
            client = Trix(api_key="test_key")
            result = client.agent.get_session("chat_123")
            assert isinstance(result, SessionMemoryList)
            assert result.total == 1
            assert isinstance(result.data[0], SessionMemory)
            assert mock_request.call_args[1]["params"] == {"limit": 100, "offset": 0}
            client.close()

    def test_get_with_pagination(self):
        with patch.object(Trix, "_request") as mock_request:
            mock_request.return_value = {"data": [], "total": 0}
            client = Trix(api_key="test_key")
            client.agent.get_session("chat_123", limit=50, offset=10)
            assert mock_request.call_args[1]["params"] == {"limit": 50, "offset": 10}
            client.close()

    def test_get_validates_session_id(self):
        with patch.object(Trix, "_request"):
            client = Trix(api_key="test_key")
            with pytest.raises(Exception):
                client.agent.get_session("")
            client.close()

    @pytest.mark.asyncio
    async def test_get_async(self):
        with patch.object(AsyncTrix, "_request", new_callable=AsyncMock) as mock_req:
            mock_req.return_value = MOCK_SESSION_MEMORY_LIST
            client = AsyncTrix(api_key="test_key")
            result = await client.agent.get_session("chat_123")
            assert isinstance(result, SessionMemoryList)
            await client.close()


# ---------------------------------------------------------------------------
# Session lifecycle — list
# ---------------------------------------------------------------------------


class TestListSessions:
    """Tests for agent.list_sessions()."""

    def test_list_basic(self):
        with patch.object(Trix, "_request") as mock_request:
            mock_request.return_value = MOCK_SESSION_LIST
            client = Trix(api_key="test_key")
            result = client.agent.list_sessions()
            assert isinstance(result, SessionList)
            assert len(result.data) == 1
            assert isinstance(result.data[0], AgentSession)
            assert mock_request.call_args[0] == ("GET", "/agent/sessions")
            client.close()

    def test_list_with_space_id(self):
        with patch.object(Trix, "_request") as mock_request:
            mock_request.return_value = MOCK_SESSION_LIST
            client = Trix(api_key="test_key")
            client.agent.list_sessions(limit=20, space_id="space_abc")
            params = mock_request.call_args[1]["params"]
            assert params["limit"] == 20
            assert params["space_id"] == "space_abc"
            client.close()

    def test_list_validates_space_id(self):
        with patch.object(Trix, "_request"):
            client = Trix(api_key="test_key")
            with pytest.raises(Exception):
                client.agent.list_sessions(space_id="")
            client.close()

    @pytest.mark.asyncio
    async def test_list_async(self):
        with patch.object(AsyncTrix, "_request", new_callable=AsyncMock) as mock_req:
            mock_req.return_value = MOCK_SESSION_LIST
            client = AsyncTrix(api_key="test_key")
            result = await client.agent.list_sessions()
            assert isinstance(result, SessionList)
            await client.close()


# ---------------------------------------------------------------------------
# Session lifecycle — end
# ---------------------------------------------------------------------------


class TestEndSession:
    """Tests for agent.end_session()."""

    def test_end_basic(self):
        with patch.object(Trix, "_request") as mock_request:
            mock_request.return_value = MOCK_AGENT_SESSION_ENDED
            client = Trix(api_key="test_key")
            session = client.agent.end_session("chat_123")
            assert isinstance(session, AgentSession)
            assert session.ended_at is not None
            assert mock_request.call_args[0] == ("POST", "/agent/sessions/chat_123/end")
            assert mock_request.call_args[1]["json"] == {}
            client.close()

    def test_end_with_summary_and_insights(self):
        with patch.object(Trix, "_request") as mock_request:
            mock_request.return_value = MOCK_AGENT_SESSION_ENDED
            client = Trix(api_key="test_key")
            session = client.agent.end_session(
                session_id="chat_123",
                summary="Discussed Python best practices",
                key_insights=["Use type hints", "Prefer composition"],
            )
            assert session.summary == "Discussed Python best practices"
            json_data = mock_request.call_args[1]["json"]
            assert json_data["summary"] == "Discussed Python best practices"
            assert json_data["key_insights"] == ["Use type hints", "Prefer composition"]
            client.close()

    def test_end_validates_session_id(self):
        with patch.object(Trix, "_request"):
            client = Trix(api_key="test_key")
            with pytest.raises(Exception):
                client.agent.end_session("")
            client.close()

    @pytest.mark.asyncio
    async def test_end_async(self):
        with patch.object(AsyncTrix, "_request", new_callable=AsyncMock) as mock_req:
            mock_req.return_value = MOCK_AGENT_SESSION_ENDED
            client = AsyncTrix(api_key="test_key")
            session = await client.agent.end_session("chat_123", summary="Done")
            assert isinstance(session, AgentSession)
            assert session.ended_at is not None
            await client.close()


# ---------------------------------------------------------------------------
# Memory operations — add_session_memory
# ---------------------------------------------------------------------------


class TestAddSessionMemory:
    """Tests for agent.add_session_memory()."""

    def test_add_memory_basic(self):
        with patch.object(Trix, "_request") as mock_request:
            mock_request.return_value = MOCK_SESSION_MEMORY
            client = Trix(api_key="test_key")
            memory = client.agent.add_session_memory(
                session_id="chat_123", content="User asked about Python"
            )
            assert isinstance(memory, SessionMemory)
            assert memory.id == "mem_001"
            json_data = mock_request.call_args[1]["json"]
            assert json_data == {"content": "User asked about Python"}
            client.close()

    def test_add_memory_with_all_options(self):
        with patch.object(Trix, "_request") as mock_request:
            mock_request.return_value = MOCK_SESSION_MEMORY
            client = Trix(api_key="test_key")
            memory = client.agent.add_session_memory(
                session_id="chat_123",
                content="User asked about Python",
                role="user",
                importance=0.8,
            )
            assert memory.role == "user"
            assert memory.importance == 0.8
            json_data = mock_request.call_args[1]["json"]
            assert json_data["role"] == "user"
            assert json_data["importance"] == 0.8
            client.close()

    def test_add_memory_importance_zero(self):
        """Importance=0.0 must be sent (not treated as falsy)."""
        with patch.object(Trix, "_request") as mock_req:
            mock_req.return_value = {**MOCK_SESSION_MEMORY, "importance": 0.0}
            client = Trix(api_key="test_key")
            client.agent.add_session_memory(session_id="chat_123", content="low", importance=0.0)
            assert mock_req.call_args[1]["json"]["importance"] == 0.0
            client.close()

    def test_add_memory_validates_session_id(self):
        with patch.object(Trix, "_request"):
            client = Trix(api_key="test_key")
            with pytest.raises(Exception):
                client.agent.add_session_memory(session_id="", content="test")
            client.close()

    @pytest.mark.asyncio
    async def test_add_memory_async(self):
        with patch.object(AsyncTrix, "_request", new_callable=AsyncMock) as mock_req:
            mock_req.return_value = MOCK_SESSION_MEMORY
            client = AsyncTrix(api_key="test_key")
            memory = await client.agent.add_session_memory(
                session_id="chat_123", content="User asked about Python", role="user"
            )
            assert isinstance(memory, SessionMemory)
            assert memory.id == "mem_001"
            await client.close()


# ---------------------------------------------------------------------------
# Memory operations — add_session_message
# ---------------------------------------------------------------------------


class TestAddSessionMessage:
    """Tests for agent.add_session_message()."""

    def test_add_message_default_role(self):
        with patch.object(Trix, "_request") as mock_request:
            mock_request.return_value = MOCK_SESSION_MESSAGE
            client = Trix(api_key="test_key")
            msg = client.agent.add_session_message(
                session_id="chat_123", content="What is the weather today?"
            )
            assert isinstance(msg, SessionMessage)
            assert msg.role == "user"
            assert msg.turn_number == 1
            assert mock_request.call_args[0] == ("POST", "/agent/sessions/chat_123/message")
            client.close()

    def test_add_message_assistant_role(self):
        assistant_data = {**MOCK_SESSION_MESSAGE, "role": "assistant", "turn_number": 2}
        with patch.object(Trix, "_request") as mock_request:
            mock_request.return_value = assistant_data
            client = Trix(api_key="test_key")
            msg = client.agent.add_session_message(
                session_id="chat_123", content="Sunny.", role="assistant"
            )
            assert msg.role == "assistant"
            assert msg.turn_number == 2
            client.close()

    def test_add_message_validates_session_id(self):
        with patch.object(Trix, "_request"):
            client = Trix(api_key="test_key")
            with pytest.raises(Exception):
                client.agent.add_session_message(session_id="", content="test")
            client.close()

    @pytest.mark.asyncio
    async def test_add_message_async(self):
        with patch.object(AsyncTrix, "_request", new_callable=AsyncMock) as mock_req:
            mock_req.return_value = MOCK_SESSION_MESSAGE
            client = AsyncTrix(api_key="test_key")
            msg = await client.agent.add_session_message(
                session_id="chat_123", content="What is the weather today?"
            )
            assert isinstance(msg, SessionMessage)
            assert msg.turn_number == 1
            await client.close()


# ---------------------------------------------------------------------------
# Context
# ---------------------------------------------------------------------------


class TestGetContext:
    """Tests for agent.get_context()."""

    def test_get_context_basic(self):
        with patch.object(Trix, "_request") as mock_request:
            mock_request.return_value = MOCK_AGENT_CONTEXT
            client = Trix(api_key="test_key")
            ctx = client.agent.get_context(query="Tell me about Python")
            assert isinstance(ctx, AgentContext)
            assert ctx.query == "Tell me about Python"
            assert len(ctx.memories) == 1
            assert len(ctx.session_memories) == 1
            assert ctx.relevance_scores["mem_999"] == 0.92
            json_data = mock_request.call_args[1]["json"]
            assert json_data["query"] == "Tell me about Python"
            assert json_data["limit"] == 10
            assert "session_id" not in json_data
            client.close()

    def test_get_context_with_session_and_limit(self):
        with patch.object(Trix, "_request") as mock_request:
            mock_request.return_value = MOCK_AGENT_CONTEXT
            client = Trix(api_key="test_key")
            client.agent.get_context(
                query="Tell me about Python", session_id="chat_123", limit=5
            )
            json_data = mock_request.call_args[1]["json"]
            assert json_data["session_id"] == "chat_123"
            assert json_data["limit"] == 5
            client.close()

    def test_get_context_validates_session_id(self):
        with patch.object(Trix, "_request"):
            client = Trix(api_key="test_key")
            with pytest.raises(Exception):
                client.agent.get_context(query="test", session_id="")
            client.close()

    @pytest.mark.asyncio
    async def test_get_context_async(self):
        with patch.object(AsyncTrix, "_request", new_callable=AsyncMock) as mock_req:
            mock_req.return_value = MOCK_AGENT_CONTEXT
            client = AsyncTrix(api_key="test_key")
            ctx = await client.agent.get_context(
                query="Tell me about Python", session_id="chat_123"
            )
            assert isinstance(ctx, AgentContext)
            assert len(ctx.memories) == 1
            await client.close()


# ---------------------------------------------------------------------------
# Error handling
# ---------------------------------------------------------------------------


class TestAgentErrorHandling:
    """Tests for error handling across agent methods."""

    def test_request_error_propagates(self):
        with patch.object(Trix, "_request") as mock_request:
            mock_request.side_effect = Exception("Connection refused")
            client = Trix(api_key="test_key")
            with pytest.raises(Exception, match="Connection refused"):
                client.agent.create_session(session_id="chat_fail")
            client.close()

    def test_invalid_response_raises_validation_error(self):
        with patch.object(Trix, "_request") as mock_request:
            mock_request.return_value = {"unexpected": "data"}
            client = Trix(api_key="test_key")
            with pytest.raises(Exception):
                client.agent.create_session(session_id="chat_bad")
            client.close()

    @pytest.mark.asyncio
    async def test_async_request_error_propagates(self):
        with patch.object(AsyncTrix, "_request", new_callable=AsyncMock) as mock_req:
            mock_req.side_effect = Exception("Timeout")
            client = AsyncTrix(api_key="test_key")
            with pytest.raises(Exception, match="Timeout"):
                await client.agent.create_session(session_id="chat_fail")
            await client.close()

    def test_get_session_invalid_limit(self):
        with patch.object(Trix, "_request"):
            client = Trix(api_key="test_key")
            with pytest.raises(Exception):
                client.agent.get_session("chat_123", limit=-1)
            client.close()

    def test_get_session_invalid_offset(self):
        with patch.object(Trix, "_request"):
            client = Trix(api_key="test_key")
            with pytest.raises(Exception):
                client.agent.get_session("chat_123", offset=-1)
            client.close()
