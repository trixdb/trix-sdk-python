"""Tests for sessions resource."""

import pytest
from unittest.mock import patch
from datetime import datetime

from trix import Trix, AsyncTrix
from trix.types import (
    Session,
    SessionsResponse,
    SessionStats,
    SessionType,
    SessionStatus,
    RetentionPolicy,
    CreateSessionParams,
    UpdateSessionParams,
    CompleteSessionParams,
)


@pytest.fixture
def mock_session_data():
    """Mock session response data."""
    return {
        "id": "sess_123",
        "account_id": "acc_456",
        "user_id": "user_789",
        "created_by": "user_789",
        "name": "Test Session",
        "description": "A test session",
        "type": "conversation",
        "status": "active",
        "space_id": "space_123",
        "origin_type": "work",
        "tags": ["test", "example"],
        "retention_policy": "permanent",
        "retention_days": None,
        "summary": None,
        "is_private": False,
        "message_count": 5,
        "memory_count": 3,
        "metadata": {"key": "value"},
        "created_at": "2025-01-01T00:00:00Z",
        "updated_at": "2025-01-01T00:00:00Z",
        "last_active_at": "2025-01-01T00:00:00Z",
        "paused_at": None,
        "completed_at": None,
        "archived_at": None,
    }


@pytest.fixture
def mock_sessions_list_data(mock_session_data):
    """Mock sessions list response data."""
    return {
        "data": [mock_session_data],
        "total": 1,
        "limit": 100,
        "offset": 0,
    }


@pytest.fixture
def mock_session_stats_data():
    """Mock session statistics data."""
    return {
        "total": 10,
        "active": 3,
        "paused": 2,
        "completed": 4,
        "archived": 1,
        "by_type": {
            "conversation": 5,
            "project": 3,
            "task": 2,
            "temporary": 0,
        },
        "total_messages": 150,
        "total_memories": 75,
    }


class TestSessionsCreate:
    """Tests for sessions.create()."""

    def test_create_basic(self, mock_session_data):
        """Test basic session creation."""
        with patch.object(Trix, "_request") as mock_request:
            mock_request.return_value = mock_session_data
            client = Trix(api_key="test_key")

            session = client.sessions.create(name="Test Session")

            assert isinstance(session, Session)
            assert session.id == "sess_123"
            assert session.name == "Test Session"
            assert session.status == SessionStatus.ACTIVE
            mock_request.assert_called_once()
            call_args = mock_request.call_args
            assert call_args[0][0] == "POST"
            assert call_args[0][1] == "/cli-sessions"
            client.close()

    def test_create_with_all_options(self, mock_session_data):
        """Test session creation with all options."""
        with patch.object(Trix, "_request") as mock_request:
            mock_request.return_value = mock_session_data
            client = Trix(api_key="test_key")

            session = client.sessions.create(
                name="Test Session",
                description="A test session",
                type=SessionType.PROJECT,
                space_id="space_123",
                origin_type="work",
                tags=["test", "project"],
                retention_policy=RetentionPolicy.AUTO_DELETE,
                retention_days=30,
                is_private=True,
                metadata={"priority": "high"},
            )

            assert isinstance(session, Session)
            call_args = mock_request.call_args
            assert call_args[0][0] == "POST"
            assert call_args[0][1] == "/cli-sessions"
            json_data = call_args[1]["json"]
            assert json_data["name"] == "Test Session"
            assert json_data["type"] == "project"
            assert json_data["retention_policy"] == "auto_delete"
            client.close()

    @pytest.mark.asyncio
    async def test_create_async(self, mock_session_data):
        """Test async session creation."""
        with patch.object(AsyncTrix, "_request") as mock_request:
            mock_request.return_value = mock_session_data
            client = AsyncTrix(api_key="test_key")

            session = await client.sessions.create(name="Test Session")

            assert isinstance(session, Session)
            assert session.id == "sess_123"
            await client.close()


class TestSessionsList:
    """Tests for sessions.list()."""

    def test_list_basic(self, mock_sessions_list_data):
        """Test basic sessions listing."""
        with patch.object(Trix, "_request") as mock_request:
            mock_request.return_value = mock_sessions_list_data
            client = Trix(api_key="test_key")

            result = client.sessions.list()

            assert isinstance(result, SessionsResponse)
            assert len(result.data) == 1
            assert result.total == 1
            assert isinstance(result.data[0], Session)
            client.close()

    def test_list_with_filters(self, mock_sessions_list_data):
        """Test sessions listing with filters."""
        with patch.object(Trix, "_request") as mock_request:
            mock_request.return_value = mock_sessions_list_data
            client = Trix(api_key="test_key")

            client.sessions.list(
                status=SessionStatus.ACTIVE,
                type=SessionType.PROJECT,
                space_id="space_123",
                tags=["test"],
                search="query",
                limit=50,
                offset=10,
            )

            call_args = mock_request.call_args
            params = call_args[1]["params"]
            assert params["status"] == "active"
            assert params["type"] == "project"
            assert params["space_id"] == "space_123"
            assert params["tags"] == "test"
            assert params["search"] == "query"
            assert params["limit"] == 50
            assert params["offset"] == 10
            client.close()

    @pytest.mark.asyncio
    async def test_list_async(self, mock_sessions_list_data):
        """Test async sessions listing."""
        with patch.object(AsyncTrix, "_request") as mock_request:
            mock_request.return_value = mock_sessions_list_data
            client = AsyncTrix(api_key="test_key")

            result = await client.sessions.list()

            assert isinstance(result, SessionsResponse)
            assert len(result.data) == 1
            await client.close()


class TestSessionsGet:
    """Tests for sessions.get()."""

    def test_get_basic(self, mock_session_data):
        """Test get session by ID."""
        with patch.object(Trix, "_request") as mock_request:
            mock_request.return_value = mock_session_data
            client = Trix(api_key="test_key")

            session = client.sessions.get("sess_123")

            assert isinstance(session, Session)
            assert session.id == "sess_123"
            call_args = mock_request.call_args
            assert call_args[0][1] == "/cli-sessions/sess_123"
            client.close()

    @pytest.mark.asyncio
    async def test_get_async(self, mock_session_data):
        """Test async get session."""
        with patch.object(AsyncTrix, "_request") as mock_request:
            mock_request.return_value = mock_session_data
            client = AsyncTrix(api_key="test_key")

            session = await client.sessions.get("sess_123")

            assert isinstance(session, Session)
            await client.close()


class TestSessionsUpdate:
    """Tests for sessions.update()."""

    def test_update_basic(self, mock_session_data):
        """Test update session."""
        with patch.object(Trix, "_request") as mock_request:
            mock_request.return_value = mock_session_data
            client = Trix(api_key="test_key")

            session = client.sessions.update(
                "sess_123",
                name="Updated Session",
                description="Updated description",
            )

            assert isinstance(session, Session)
            call_args = mock_request.call_args
            assert call_args[0][0] == "PATCH"
            assert call_args[0][1] == "/cli-sessions/sess_123"
            client.close()

    def test_update_with_all_fields(self, mock_session_data):
        """Test update session with all optional fields."""
        with patch.object(Trix, "_request") as mock_request:
            mock_request.return_value = mock_session_data
            client = Trix(api_key="test_key")

            session = client.sessions.update(
                "sess_123",
                name="Updated",
                description="New desc",
                tags=["new", "tags"],
                retention_policy=RetentionPolicy.TEMPORARY,
                retention_days=7,
                is_private=True,
                metadata={"updated": True},
            )

            assert isinstance(session, Session)
            call_args = mock_request.call_args
            json_data = call_args[1]["json"]
            assert json_data["name"] == "Updated"
            assert json_data["retention_policy"] == "temporary"
            client.close()

    @pytest.mark.asyncio
    async def test_update_async(self, mock_session_data):
        """Test async update session."""
        with patch.object(AsyncTrix, "_request") as mock_request:
            mock_request.return_value = mock_session_data
            client = AsyncTrix(api_key="test_key")

            session = await client.sessions.update("sess_123", name="Updated")

            assert isinstance(session, Session)
            await client.close()


class TestSessionsDelete:
    """Tests for sessions.delete()."""

    def test_delete_basic(self):
        """Test delete session."""
        with patch.object(Trix, "_request") as mock_request:
            mock_request.return_value = None
            client = Trix(api_key="test_key")

            client.sessions.delete("sess_123")

            call_args = mock_request.call_args
            assert call_args[0][0] == "DELETE"
            assert call_args[0][1] == "/cli-sessions/sess_123"
            client.close()

    @pytest.mark.asyncio
    async def test_delete_async(self):
        """Test async delete session."""
        with patch.object(AsyncTrix, "_request") as mock_request:
            mock_request.return_value = None
            client = AsyncTrix(api_key="test_key")

            await client.sessions.delete("sess_123")

            mock_request.assert_called_once()
            await client.close()


class TestSessionsGetActive:
    """Tests for sessions.get_active()."""

    def test_get_active(self, mock_sessions_list_data):
        """Test get active sessions."""
        with patch.object(Trix, "_request") as mock_request:
            mock_request.return_value = mock_sessions_list_data
            client = Trix(api_key="test_key")

            result = client.sessions.get_active()

            assert isinstance(result, SessionsResponse)
            call_args = mock_request.call_args
            assert call_args[0][1] == "/cli-sessions/active"
            client.close()

    @pytest.mark.asyncio
    async def test_get_active_async(self, mock_sessions_list_data):
        """Test async get active sessions."""
        with patch.object(AsyncTrix, "_request") as mock_request:
            mock_request.return_value = mock_sessions_list_data
            client = AsyncTrix(api_key="test_key")

            result = await client.sessions.get_active()

            assert isinstance(result, SessionsResponse)
            await client.close()


class TestSessionsGetStats:
    """Tests for sessions.get_stats()."""

    def test_get_stats(self, mock_session_stats_data):
        """Test get session statistics."""
        with patch.object(Trix, "_request") as mock_request:
            mock_request.return_value = mock_session_stats_data
            client = Trix(api_key="test_key")

            stats = client.sessions.get_stats()

            assert isinstance(stats, SessionStats)
            assert stats.total == 10
            assert stats.active == 3
            assert stats.by_type["conversation"] == 5
            call_args = mock_request.call_args
            assert call_args[0][1] == "/cli-sessions/stats"
            client.close()

    @pytest.mark.asyncio
    async def test_get_stats_async(self, mock_session_stats_data):
        """Test async get session statistics."""
        with patch.object(AsyncTrix, "_request") as mock_request:
            mock_request.return_value = mock_session_stats_data
            client = AsyncTrix(api_key="test_key")

            stats = await client.sessions.get_stats()

            assert isinstance(stats, SessionStats)
            await client.close()


class TestSessionsPause:
    """Tests for sessions.pause()."""

    def test_pause_basic(self, mock_session_data):
        """Test pause session."""
        paused_data = mock_session_data.copy()
        paused_data["status"] = "paused"
        paused_data["paused_at"] = "2025-01-01T01:00:00Z"

        with patch.object(Trix, "_request") as mock_request:
            mock_request.return_value = paused_data
            client = Trix(api_key="test_key")

            session = client.sessions.pause("sess_123")

            assert isinstance(session, Session)
            assert session.status == SessionStatus.PAUSED
            assert session.paused_at is not None
            call_args = mock_request.call_args
            assert call_args[0][0] == "POST"
            assert call_args[0][1] == "/cli-sessions/sess_123/pause"
            client.close()

    @pytest.mark.asyncio
    async def test_pause_async(self, mock_session_data):
        """Test async pause session."""
        paused_data = mock_session_data.copy()
        paused_data["status"] = "paused"

        with patch.object(AsyncTrix, "_request") as mock_request:
            mock_request.return_value = paused_data
            client = AsyncTrix(api_key="test_key")

            session = await client.sessions.pause("sess_123")

            assert isinstance(session, Session)
            await client.close()


class TestSessionsResume:
    """Tests for sessions.resume()."""

    def test_resume_basic(self, mock_session_data):
        """Test resume session."""
        with patch.object(Trix, "_request") as mock_request:
            mock_request.return_value = mock_session_data
            client = Trix(api_key="test_key")

            session = client.sessions.resume("sess_123")

            assert isinstance(session, Session)
            assert session.status == SessionStatus.ACTIVE
            call_args = mock_request.call_args
            assert call_args[0][0] == "POST"
            assert call_args[0][1] == "/cli-sessions/sess_123/resume"
            client.close()

    @pytest.mark.asyncio
    async def test_resume_async(self, mock_session_data):
        """Test async resume session."""
        with patch.object(AsyncTrix, "_request") as mock_request:
            mock_request.return_value = mock_session_data
            client = AsyncTrix(api_key="test_key")

            session = await client.sessions.resume("sess_123")

            assert isinstance(session, Session)
            await client.close()


class TestSessionsComplete:
    """Tests for sessions.complete()."""

    def test_complete_basic(self, mock_session_data):
        """Test complete session without summary."""
        completed_data = mock_session_data.copy()
        completed_data["status"] = "completed"
        completed_data["completed_at"] = "2025-01-01T02:00:00Z"

        with patch.object(Trix, "_request") as mock_request:
            mock_request.return_value = completed_data
            client = Trix(api_key="test_key")

            session = client.sessions.complete("sess_123")

            assert isinstance(session, Session)
            assert session.status == SessionStatus.COMPLETED
            assert session.completed_at is not None
            call_args = mock_request.call_args
            assert call_args[0][0] == "POST"
            assert call_args[0][1] == "/cli-sessions/sess_123/complete"
            client.close()

    def test_complete_with_summary(self, mock_session_data):
        """Test complete session with summary."""
        completed_data = mock_session_data.copy()
        completed_data["status"] = "completed"
        completed_data["summary"] = "Session completed successfully"

        with patch.object(Trix, "_request") as mock_request:
            mock_request.return_value = completed_data
            client = Trix(api_key="test_key")

            session = client.sessions.complete(
                "sess_123",
                summary="Session completed successfully"
            )

            assert isinstance(session, Session)
            assert session.summary == "Session completed successfully"
            call_args = mock_request.call_args
            json_data = call_args[1]["json"]
            assert json_data["summary"] == "Session completed successfully"
            client.close()

    @pytest.mark.asyncio
    async def test_complete_async(self, mock_session_data):
        """Test async complete session."""
        completed_data = mock_session_data.copy()
        completed_data["status"] = "completed"

        with patch.object(AsyncTrix, "_request") as mock_request:
            mock_request.return_value = completed_data
            client = AsyncTrix(api_key="test_key")

            session = await client.sessions.complete("sess_123")

            assert isinstance(session, Session)
            await client.close()


class TestSessionsGetMemories:
    """Tests for sessions.get_memories()."""

    def test_get_memories(self):
        """Test get session memories."""
        mock_memories_data = {
            "data": [
                {
                    "id": "mem_123",
                    "content": "Test memory",
                    "type": "text",
                    "tags": [],
                    "created_at": "2025-01-01T00:00:00Z",
                    "updated_at": "2025-01-01T00:00:00Z",
                    "access_count": 0,
                }
            ],
            "total": 1,
            "limit": 100,
            "offset": 0,
        }

        with patch.object(Trix, "_request") as mock_request:
            mock_request.return_value = mock_memories_data
            client = Trix(api_key="test_key")

            result = client.sessions.get_memories("sess_123")

            assert "data" in result
            assert len(result["data"]) == 1
            call_args = mock_request.call_args
            assert call_args[0][1] == "/cli-sessions/sess_123/memories"
            client.close()

    def test_get_memories_with_pagination(self):
        """Test get session memories with pagination."""
        mock_memories_data = {
            "data": [],
            "total": 0,
            "limit": 50,
            "offset": 20,
        }

        with patch.object(Trix, "_request") as mock_request:
            mock_request.return_value = mock_memories_data
            client = Trix(api_key="test_key")

            result = client.sessions.get_memories(
                "sess_123",
                limit=50,
                offset=20
            )

            call_args = mock_request.call_args
            params = call_args[1]["params"]
            assert params["limit"] == 50
            assert params["offset"] == 20
            client.close()

    @pytest.mark.asyncio
    async def test_get_memories_async(self):
        """Test async get session memories."""
        mock_memories_data = {
            "data": [],
            "total": 0,
            "limit": 100,
            "offset": 0,
        }

        with patch.object(AsyncTrix, "_request") as mock_request:
            mock_request.return_value = mock_memories_data
            client = AsyncTrix(api_key="test_key")

            result = await client.sessions.get_memories("sess_123")

            assert "data" in result
            await client.close()


class TestSessionsErrorHandling:
    """Tests for error handling in sessions resource."""

    def test_invalid_session_id(self):
        """Test validation of invalid session ID."""
        with patch.object(Trix, "_request") as mock_request:
            client = Trix(api_key="test_key")

            # This should raise a validation error for invalid ID format
            with pytest.raises(Exception):
                client.sessions.get("invalid_id_without_prefix")

            client.close()
