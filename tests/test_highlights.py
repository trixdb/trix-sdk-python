"""Tests for highlights resource."""

import pytest
from unittest.mock import patch

from trix import Trix, AsyncTrix, Highlight, HighlightList


@pytest.fixture
def mock_highlight_data():
    """Mock highlight response data."""
    return {
        "id": "hl_123",
        "memory_id": "mem_001",
        "text": "This is important",
        "note": "Key insight",
        "importance": 5,
        "tags": ["insight", "key"],
        "color": "#FFFF00",
        "created_at": "2025-01-01T00:00:00Z",
        "updated_at": "2025-01-01T00:00:00Z",
    }


@pytest.fixture
def mock_highlight_list_data(mock_highlight_data):
    """Mock highlight list response data."""
    return {"data": [mock_highlight_data]}


class TestHighlightsCreate:
    """Tests for highlights.create()."""

    def test_create_basic(self, mock_highlight_data):
        """Test basic highlight creation."""
        with patch.object(Trix, "_request") as mock_request:
            mock_request.return_value = mock_highlight_data
            client = Trix(api_key="test_key")

            hl = client.highlights.create(
                memory_id="mem_001",
                text="This is important",
            )

            assert isinstance(hl, Highlight)
            assert hl.id == "hl_123"
            assert hl.text == "This is important"
            mock_request.assert_called_once()
            client.close()

    def test_create_with_all_options(self, mock_highlight_data):
        """Test highlight creation with all options."""
        with patch.object(Trix, "_request") as mock_request:
            mock_request.return_value = mock_highlight_data
            client = Trix(api_key="test_key")

            hl = client.highlights.create(
                memory_id="mem_001",
                text="This is important",
                note="Key insight",
                importance=5,
                tags=["insight", "key"],
                color="#FFFF00",
            )

            assert isinstance(hl, Highlight)
            call_args = mock_request.call_args
            assert call_args[0][0] == "POST"
            assert call_args[0][1] == "/memories/mem_001/highlights"
            body = call_args[1]["json"]
            assert body["text"] == "This is important"
            assert body["note"] == "Key insight"
            assert body["importance"] == 5
            assert body["color"] == "#FFFF00"
            client.close()


class TestHighlightsGet:
    """Tests for highlights.get()."""

    def test_get_by_id(self, mock_highlight_data):
        """Test getting a highlight by ID."""
        with patch.object(Trix, "_request") as mock_request:
            mock_request.return_value = mock_highlight_data
            client = Trix(api_key="test_key")

            hl = client.highlights.get("hl_123")

            assert hl.id == "hl_123"
            mock_request.assert_called_with("GET", "/highlights/hl_123")
            client.close()


class TestHighlightsList:
    """Tests for highlights.list()."""

    def test_list_by_memory(self, mock_highlight_list_data):
        """Test listing highlights for a memory."""
        with patch.object(Trix, "_request") as mock_request:
            mock_request.return_value = mock_highlight_list_data
            client = Trix(api_key="test_key")

            result = client.highlights.list("mem_001")

            assert isinstance(result, HighlightList)
            assert len(result.data) == 1
            call_args = mock_request.call_args
            assert call_args[0][1] == "/memories/mem_001/highlights"
            client.close()

    def test_list_with_limit(self, mock_highlight_list_data):
        """Test listing highlights with custom limit."""
        with patch.object(Trix, "_request") as mock_request:
            mock_request.return_value = mock_highlight_list_data
            client = Trix(api_key="test_key")

            client.highlights.list("mem_001", limit=50)

            call_args = mock_request.call_args
            assert call_args[1]["params"]["limit"] == 50
            client.close()

    def test_list_global(self, mock_highlight_list_data):
        """Test listing all highlights globally."""
        with patch.object(Trix, "_request") as mock_request:
            mock_request.return_value = mock_highlight_list_data
            client = Trix(api_key="test_key")

            result = client.highlights.list_global(limit=50, offset=10)

            assert isinstance(result, HighlightList)
            call_args = mock_request.call_args
            assert call_args[0][1] == "/highlights"
            assert call_args[1]["params"]["limit"] == 50
            assert call_args[1]["params"]["offset"] == 10
            client.close()


class TestHighlightsUpdate:
    """Tests for highlights.update()."""

    def test_update_importance(self, mock_highlight_data):
        """Test updating highlight importance."""
        with patch.object(Trix, "_request") as mock_request:
            mock_highlight_data["importance"] = 10
            mock_request.return_value = mock_highlight_data
            client = Trix(api_key="test_key")

            hl = client.highlights.update("hl_123", importance=10)

            assert hl.importance == 10
            call_args = mock_request.call_args
            assert call_args[0][0] == "PATCH"
            assert call_args[0][1] == "/highlights/hl_123"
            client.close()

    def test_update_text_and_note(self, mock_highlight_data):
        """Test updating highlight text and note."""
        with patch.object(Trix, "_request") as mock_request:
            mock_highlight_data["text"] = "Updated text"
            mock_highlight_data["note"] = "Updated note"
            mock_request.return_value = mock_highlight_data
            client = Trix(api_key="test_key")

            hl = client.highlights.update(
                "hl_123", text="Updated text", note="Updated note"
            )

            assert hl.text == "Updated text"
            assert hl.note == "Updated note"
            client.close()


class TestHighlightsDelete:
    """Tests for highlights.delete()."""

    def test_delete_by_id(self):
        """Test deleting a highlight by ID."""
        with patch.object(Trix, "_request") as mock_request:
            mock_request.return_value = {}
            client = Trix(api_key="test_key")

            client.highlights.delete("hl_123")

            mock_request.assert_called_with("DELETE", "/highlights/hl_123")
            client.close()


class TestAsyncHighlights:
    """Tests for async highlights operations."""

    @pytest.mark.asyncio
    async def test_async_create(self, mock_highlight_data):
        """Test async highlight creation."""
        with patch.object(AsyncTrix, "_request") as mock_request:
            mock_request.return_value = mock_highlight_data
            async with AsyncTrix(api_key="test_key") as client:
                hl = await client.highlights.create(
                    memory_id="mem_001", text="Important"
                )
                assert hl.id == "hl_123"

    @pytest.mark.asyncio
    async def test_async_list(self, mock_highlight_list_data):
        """Test async highlight listing."""
        with patch.object(AsyncTrix, "_request") as mock_request:
            mock_request.return_value = mock_highlight_list_data
            async with AsyncTrix(api_key="test_key") as client:
                result = await client.highlights.list("mem_001")
                assert len(result.data) == 1

    @pytest.mark.asyncio
    async def test_async_get(self, mock_highlight_data):
        """Test async highlight get."""
        with patch.object(AsyncTrix, "_request") as mock_request:
            mock_request.return_value = mock_highlight_data
            async with AsyncTrix(api_key="test_key") as client:
                hl = await client.highlights.get("hl_123")
                assert hl.id == "hl_123"

    @pytest.mark.asyncio
    async def test_async_delete(self):
        """Test async highlight deletion."""
        with patch.object(AsyncTrix, "_request") as mock_request:
            mock_request.return_value = {}
            async with AsyncTrix(api_key="test_key") as client:
                await client.highlights.delete("hl_123")
                mock_request.assert_called_with("DELETE", "/highlights/hl_123")
