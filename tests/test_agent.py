"""Tests for agent resource — add_session_message method."""

import pytest
from unittest.mock import patch

from trix import Trix, AsyncTrix
from trix.types import SessionMessage

MOCK_SESSION_MESSAGE = {
    "id": "mem_abc123",
    "session_id": "chat_123",
    "role": "user",
    "content": "What is the weather today?",
    "created_at": "2025-01-15T10:00:00Z",
    "turn_number": 1,
}


class TestAddSessionMessage:
    """Tests for agent.add_session_message()."""

    def test_add_message_default_role(self):
        """Test adding a message with default role."""
        with patch.object(Trix, "_request") as mock_request:
            mock_request.return_value = MOCK_SESSION_MESSAGE
            client = Trix(api_key="test_key")

            msg = client.agent.add_session_message(
                session_id="chat_123",
                content="What is the weather today?",
            )

            assert isinstance(msg, SessionMessage)
            assert msg.id == "mem_abc123"
            assert msg.session_id == "chat_123"
            assert msg.role == "user"
            assert msg.content == "What is the weather today?"
            assert msg.turn_number == 1

            call_args = mock_request.call_args
            assert call_args[0][0] == "POST"
            assert call_args[0][1] == "/agent/sessions/chat_123/message"
            json_data = call_args[1]["json"]
            assert json_data["role"] == "user"
            assert json_data["content"] == "What is the weather today?"
            client.close()

    def test_add_message_assistant_role(self):
        """Test adding a message with assistant role."""
        assistant_data = {**MOCK_SESSION_MESSAGE, "role": "assistant", "turn_number": 2}
        with patch.object(Trix, "_request") as mock_request:
            mock_request.return_value = assistant_data
            client = Trix(api_key="test_key")

            msg = client.agent.add_session_message(
                session_id="chat_123",
                content="The weather is sunny.",
                role="assistant",
            )

            assert isinstance(msg, SessionMessage)
            assert msg.role == "assistant"
            assert msg.turn_number == 2

            json_data = mock_request.call_args[1]["json"]
            assert json_data["role"] == "assistant"
            client.close()

    def test_add_message_validates_session_id(self):
        """Test that invalid session IDs are rejected."""
        with patch.object(Trix, "_request"):
            client = Trix(api_key="test_key")

            with pytest.raises(Exception):
                client.agent.add_session_message(
                    session_id="",
                    content="test",
                )

            client.close()

    @pytest.mark.asyncio
    async def test_add_message_async(self):
        """Test async add_session_message."""
        with patch.object(AsyncTrix, "_request") as mock_request:
            mock_request.return_value = MOCK_SESSION_MESSAGE
            client = AsyncTrix(api_key="test_key")

            msg = await client.agent.add_session_message(
                session_id="chat_123",
                content="What is the weather today?",
            )

            assert isinstance(msg, SessionMessage)
            assert msg.id == "mem_abc123"
            assert msg.role == "user"
            assert msg.turn_number == 1

            call_args = mock_request.call_args
            assert call_args[0][0] == "POST"
            assert call_args[0][1] == "/agent/sessions/chat_123/message"
            await client.close()

    @pytest.mark.asyncio
    async def test_add_message_async_with_role(self):
        """Test async add_session_message with explicit role."""
        assistant_data = {**MOCK_SESSION_MESSAGE, "role": "assistant"}
        with patch.object(AsyncTrix, "_request") as mock_request:
            mock_request.return_value = assistant_data
            client = AsyncTrix(api_key="test_key")

            msg = await client.agent.add_session_message(
                session_id="chat_123",
                content="Response here.",
                role="assistant",
            )

            assert isinstance(msg, SessionMessage)
            assert msg.role == "assistant"
            await client.close()
