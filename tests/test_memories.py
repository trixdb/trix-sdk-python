"""Tests for memories resource."""

from unittest.mock import patch

import pytest

from trix import AsyncTrix, Memory, MemoryCreate, MemoryList, MemoryType, Trix


@pytest.fixture
def mock_memory_data():
    """Mock memory response data."""
    return {
        "id": "mem_123",
        "content": "Test memory content",
        "type": "text",
        "tags": ["test", "example"],
        "metadata": {"source": "test"},
        "priority": 5,
        "space_id": "space_123",
        "created_at": "2025-01-01T00:00:00Z",
        "updated_at": "2025-01-01T00:00:00Z",
        "access_count": 0,
    }


@pytest.fixture
def mock_memory_list_data(mock_memory_data):
    """Mock memory list response data."""
    return {
        "data": [mock_memory_data],
        "total": 1,
        "limit": 100,
        "offset": 0,
    }


class TestMemoriesCreate:
    """Tests for memories.create()."""

    def test_create_basic(self, mock_memory_data):
        """Test basic memory creation."""
        with patch.object(Trix, "_request") as mock_request:
            mock_request.return_value = mock_memory_data
            client = Trix(api_key="test_key")

            memory = client.memories.create(content="Test memory content")

            assert isinstance(memory, Memory)
            assert memory.id == "mem_123"
            assert memory.content == "Test memory content"
            mock_request.assert_called_once()
            client.close()

    def test_create_with_all_options(self, mock_memory_data):
        """Test memory creation with all options."""
        with patch.object(Trix, "_request") as mock_request:
            mock_request.return_value = mock_memory_data
            client = Trix(api_key="test_key")

            memory = client.memories.create(
                content="Test content",
                type=MemoryType.MARKDOWN,
                tags=["tag1", "tag2"],
                metadata={"key": "value"},
                priority=10,
                space_id="space_123",
            )

            assert isinstance(memory, Memory)
            call_args = mock_request.call_args
            assert call_args[0][0] == "POST"
            assert call_args[0][1] == "/memories"
            client.close()

    def test_create_with_session_id(self, mock_memory_data):
        """Test memory creation with session_id."""
        with patch.object(Trix, "_request") as mock_request:
            mock_request.return_value = mock_memory_data
            client = Trix(api_key="test_key")

            memory = client.memories.create(
                content="Test content",
                session_id="sess_abc123",
            )

            assert isinstance(memory, Memory)
            call_args = mock_request.call_args
            body = call_args[1]["json"]
            assert body["session_id"] == "sess_abc123"
            client.close()


class TestMemoriesList:
    """Tests for memories.list()."""

    def test_list_basic(self, mock_memory_list_data):
        """Test basic memory listing."""
        with patch.object(Trix, "_request") as mock_request:
            mock_request.return_value = mock_memory_list_data
            client = Trix(api_key="test_key")

            result = client.memories.list()

            assert isinstance(result, MemoryList)
            assert len(result.data) == 1
            assert result.total == 1
            client.close()

    def test_list_with_filters(self, mock_memory_list_data):
        """Test memory listing with filters."""
        with patch.object(Trix, "_request") as mock_request:
            mock_request.return_value = mock_memory_list_data
            client = Trix(api_key="test_key")

            client.memories.list(
                q="test query",
                tags=["tag1"],
                limit=50,
                offset=10,
            )

            call_args = mock_request.call_args
            params = call_args[1]["params"]
            assert params["q"] == "test query"
            assert params["limit"] == 50
            assert params["offset"] == 10
            client.close()

    def test_list_with_session_id(self, mock_memory_list_data):
        """Test memory listing filtered by session_id."""
        with patch.object(Trix, "_request") as mock_request:
            mock_request.return_value = mock_memory_list_data
            client = Trix(api_key="test_key")

            client.memories.list(session_id="sess_abc123")

            call_args = mock_request.call_args
            params = call_args[1]["params"]
            assert params["session_id"] == "sess_abc123"
            client.close()


class TestMemoriesGet:
    """Tests for memories.get()."""

    def test_get_by_id(self, mock_memory_data):
        """Test getting memory by ID."""
        with patch.object(Trix, "_request") as mock_request:
            mock_request.return_value = mock_memory_data
            client = Trix(api_key="test_key")

            memory = client.memories.get("mem_123")

            assert memory.id == "mem_123"
            mock_request.assert_called_with("GET", "/memories/mem_123")
            client.close()


class TestMemoriesUpdate:
    """Tests for memories.update()."""

    def test_update_content(self, mock_memory_data):
        """Test updating memory content."""
        with patch.object(Trix, "_request") as mock_request:
            mock_memory_data["content"] = "Updated content"
            mock_request.return_value = mock_memory_data
            client = Trix(api_key="test_key")

            memory = client.memories.update("mem_123", content="Updated content")

            assert memory.content == "Updated content"
            client.close()


class TestMemoriesDelete:
    """Tests for memories.delete()."""

    def test_delete_by_id(self):
        """Test deleting memory by ID."""
        with patch.object(Trix, "_request") as mock_request:
            mock_request.return_value = {}
            client = Trix(api_key="test_key")

            client.memories.delete("mem_123")

            mock_request.assert_called_with("DELETE", "/memories/mem_123")
            client.close()


class TestMemoriesBulkOperations:
    """Tests for bulk memory operations."""

    def test_bulk_create(self, mock_memory_data):
        """Test bulk memory creation."""
        with patch.object(Trix, "_request") as mock_request:
            mock_request.return_value = {"success": 2, "failed": 0, "errors": []}
            client = Trix(api_key="test_key")

            result = client.memories.bulk_create(
                [
                    MemoryCreate(content="First"),
                    MemoryCreate(content="Second"),
                ]
            )

            assert result.success == 2
            assert result.failed == 0
            client.close()

    def test_bulk_delete(self):
        """Test bulk memory deletion."""
        with patch.object(Trix, "_request") as mock_request:
            mock_request.return_value = {"success": 2, "failed": 0, "errors": []}
            client = Trix(api_key="test_key")

            result = client.memories.bulk_delete(["mem_123", "mem_456"])

            call_args = mock_request.call_args
            assert call_args[1]["json"]["ids"] == ["mem_123", "mem_456"]
            assert result.success == 2
            client.close()


class TestAsyncMemories:
    """Tests for async memories operations."""

    @pytest.mark.asyncio
    async def test_async_create(self, mock_memory_data):
        """Test async memory creation."""
        with patch.object(AsyncTrix, "_request") as mock_request:
            mock_request.return_value = mock_memory_data
            async with AsyncTrix(api_key="test_key") as client:
                memory = await client.memories.create(content="Test content")
                assert memory.id == "mem_123"

    @pytest.mark.asyncio
    async def test_async_list(self, mock_memory_list_data):
        """Test async memory listing."""
        with patch.object(AsyncTrix, "_request") as mock_request:
            mock_request.return_value = mock_memory_list_data
            async with AsyncTrix(api_key="test_key") as client:
                result = await client.memories.list()
                assert len(result.data) == 1

    @pytest.mark.asyncio
    async def test_async_get(self, mock_memory_data):
        """Test async memory get."""
        with patch.object(AsyncTrix, "_request") as mock_request:
            mock_request.return_value = mock_memory_data
            async with AsyncTrix(api_key="test_key") as client:
                memory = await client.memories.get("mem_123")
                assert memory.id == "mem_123"

    @pytest.mark.asyncio
    async def test_async_delete(self):
        """Test async memory deletion."""
        with patch.object(AsyncTrix, "_request") as mock_request:
            mock_request.return_value = {}
            async with AsyncTrix(api_key="test_key") as client:
                await client.memories.delete("mem_123")
                mock_request.assert_called_with("DELETE", "/memories/mem_123")


def _mem_page(ids, limit, offset):
    """Build a MemoryList-shaped page for the given memory ids."""
    data = [
        {
            "id": mid,
            "content": f"content {mid}",
            "type": "text",
            "created_at": "2025-01-01T00:00:00Z",
            "updated_at": "2025-01-01T00:00:00Z",
        }
        for mid in ids
    ]
    return {"data": data, "total": 3, "limit": limit, "offset": offset}


class TestMemoriesIter:
    """Auto-pagination via iter() yields typed Memory objects (sync + async)."""

    def test_iter_yields_typed_memory(self, mock_memory_list_data):
        """Sync iter() yields Memory models, not dicts."""
        with patch.object(Trix, "_request") as mock_request:
            mock_request.return_value = mock_memory_list_data
            client = Trix(api_key="test_key")
            items = list(client.memories.iter())
            client.close()

        assert len(items) == 1
        assert all(isinstance(m, Memory) for m in items)
        assert items[0].id == "mem_123"

    @pytest.mark.asyncio
    async def test_async_iter_yields_typed_memory(self, mock_memory_list_data):
        """`async for` over iter() yields Memory models (the fixed bug)."""
        with patch.object(AsyncTrix, "_request") as mock_request:
            mock_request.return_value = mock_memory_list_data
            async with AsyncTrix(api_key="test_key") as client:
                # Used directly with `async for` (no pre-await), like the sync path.
                items = [m async for m in client.memories.iter()]

        assert len(items) == 1
        item = items[0]
        assert isinstance(item, Memory)  # typed model, not a raw dict
        assert not isinstance(item, dict)
        assert item.id == "mem_123"  # attribute access works on the model

    @pytest.mark.asyncio
    async def test_async_iter_paginates_and_stays_typed(self):
        """Async iter() advances across pages and yields typed models throughout."""
        pages = [
            _mem_page(["mem_1", "mem_2"], limit=2, offset=0),  # full page -> continue
            _mem_page(["mem_3"], limit=2, offset=2),  # short page -> stop
        ]
        with patch.object(AsyncTrix, "_request") as mock_request:
            mock_request.side_effect = pages
            async with AsyncTrix(api_key="test_key") as client:
                items = [m async for m in client.memories.iter(page_size=2)]

        assert all(isinstance(m, Memory) for m in items)
        assert [m.id for m in items] == ["mem_1", "mem_2", "mem_3"]
        assert mock_request.call_count == 2
