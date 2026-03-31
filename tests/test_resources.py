"""Tests for Resources API"""

import pytest
from unittest.mock import patch
from trix import Trix
from trix.types import Resource, ResourceList


@pytest.fixture
def mock_resource_data():
    """Mock resource response data."""
    return {
        "id": "res_123456",
        "name": "My Project",
        "type": "project",
        "description": "Project description",
        "metadata": {"key": "value"},
        "created_at": "2026-01-07T00:00:00Z",
        "updated_at": "2026-01-07T00:00:00Z",
    }


@pytest.fixture
def mock_list_response(mock_resource_data):
    """Mock list resources response."""
    return {
        "data": [mock_resource_data],
        "pagination": {
            "total": 1,
            "page": 1,
            "limit": 50,
            "has_more": False,
        },
    }


class TestResourcesCreate:
    """Tests for resources.create()."""

    def test_create_with_name_only(self, mock_resource_data):
        """Test creating a resource with name only."""
        with patch.object(Trix, "_request") as mock_request:
            mock_request.return_value = mock_resource_data
            client = Trix(api_key="test_key")
            resource = client.resources.create(name="My Project")
            assert isinstance(resource, Resource)
            assert resource.id == "res_123456"
            assert resource.name == "My Project"
            client.close()

    def test_create_with_all_fields(self, mock_resource_data):
        """Test creating a resource with all fields."""
        with patch.object(Trix, "_request") as mock_request:
            mock_request.return_value = mock_resource_data
            client = Trix(api_key="test_key")
            resource = client.resources.create(
                name="My Project",
                type="project",
                description="Project description",
                metadata={"key": "value"},
            )
            assert resource.name == "My Project"
            assert resource.type == "project"
            client.close()


class TestResourcesList:
    """Tests for resources.list()."""

    def test_list_default(self, mock_list_response):
        """Test listing resources with defaults."""
        with patch.object(Trix, "_request") as mock_request:
            mock_request.return_value = mock_list_response
            client = Trix(api_key="test_key")
            result = client.resources.list()
            assert isinstance(result, ResourceList)
            assert len(result.data) == 1
            assert isinstance(result.data[0], Resource)
            client.close()

    def test_list_with_filters(self, mock_list_response):
        """Test listing resources with filters."""
        with patch.object(Trix, "_request") as mock_request:
            mock_request.return_value = mock_list_response
            client = Trix(api_key="test_key")
            result = client.resources.list(
                type="project",
                search="my project",
                limit=20,
                offset=0,
                sort="name",
                order="asc",
            )
            assert len(result.data) == 1
            client.close()


class TestResourcesGet:
    """Tests for resources.get()."""

    def test_get_by_id(self, mock_resource_data):
        """Test getting a resource by ID."""
        with patch.object(Trix, "_request") as mock_request:
            mock_request.return_value = mock_resource_data
            client = Trix(api_key="test_key")
            resource = client.resources.get("res_123456")
            assert isinstance(resource, Resource)
            assert resource.id == "res_123456"
            client.close()

    def test_get_validates_id(self):
        """Test that get validates the resource ID."""
        client = Trix(api_key="test_key")
        with pytest.raises(ValueError):
            client.resources.get("")
        client.close()


class TestResourcesUpdate:
    """Tests for resources.update()."""

    def test_update_name(self, mock_resource_data):
        """Test updating resource name."""
        updated_data = {**mock_resource_data, "name": "Updated Name"}
        with patch.object(Trix, "_request") as mock_request:
            mock_request.return_value = updated_data
            client = Trix(api_key="test_key")
            resource = client.resources.update("res_123456", name="Updated Name")
            assert resource.name == "Updated Name"
            client.close()

    def test_update_validates_id(self):
        """Test that update validates the resource ID."""
        client = Trix(api_key="test_key")
        with pytest.raises(ValueError):
            client.resources.update("", name="New Name")
        client.close()


class TestResourcesDelete:
    """Tests for resources.delete()."""

    def test_delete(self):
        """Test deleting a resource."""
        with patch.object(Trix, "_request") as mock_request:
            mock_request.return_value = None
            client = Trix(api_key="test_key")
            client.resources.delete("res_123456")
            mock_request.assert_called_once()
            client.close()

    def test_delete_validates_id(self):
        """Test that delete validates the resource ID."""
        client = Trix(api_key="test_key")
        with pytest.raises(ValueError):
            client.resources.delete("")
        client.close()


class TestResourcesGetMemories:
    """Tests for resources.get_memories()."""

    def test_get_memories(self):
        """Test getting memories linked to a resource."""
        mock_response = {
            "resource_id": "res_123456",
            "data": [
                {
                    "id": "mem_1",
                    "content": "Memory 1",
                    "relationship_type": "primary",
                    "linked_at": "2026-01-07T00:00:00Z",
                }
            ],
            "pagination": {"total": 1, "limit": 50, "offset": 0, "has_more": False},
        }
        with patch.object(Trix, "_request") as mock_request:
            mock_request.return_value = mock_response
            client = Trix(api_key="test_key")
            result = client.resources.get_memories("res_123456")
            assert result["resource_id"] == "res_123456"
            assert len(result["data"]) == 1
            client.close()

    def test_get_memories_validates_id(self):
        """Test that get_memories validates the resource ID."""
        client = Trix(api_key="test_key")
        with pytest.raises(ValueError):
            client.resources.get_memories("")
        client.close()


class TestMemoryResourceLinking:
    """Tests for memory-resource linking methods."""

    def test_link_resource(self):
        """Test linking a resource to a memory."""
        mock_response = {
            "memory_id": "mem_123",
            "resource_id": "res_456",
            "relationship_type": "primary",
            "linked": True,
        }
        with patch.object(Trix, "_request") as mock_request:
            mock_request.return_value = mock_response
            client = Trix(api_key="test_key")
            result = client.memories.link_resource(
                "mem_123", resource_id="res_456", relationship_type="primary"
            )
            assert result["linked"] is True
            assert result["memory_id"] == "mem_123"
            client.close()

    def test_link_resource_validates_ids(self):
        """Test that link_resource validates memory and resource IDs."""
        client = Trix(api_key="test_key")
        with pytest.raises(ValueError):
            client.memories.link_resource("", resource_id="res_456")
        client.close()

    def test_get_resources(self):
        """Test getting resources linked to a memory."""
        mock_response = {
            "memory_id": "mem_123",
            "data": [
                {
                    "id": "res_1",
                    "name": "Resource 1",
                    "relationship_type": "primary",
                    "linked_at": "2026-01-07T00:00:00Z",
                }
            ],
        }
        with patch.object(Trix, "_request") as mock_request:
            mock_request.return_value = mock_response
            client = Trix(api_key="test_key")
            result = client.memories.get_resources("mem_123")
            assert result["memory_id"] == "mem_123"
            assert len(result["data"]) == 1
            client.close()

    def test_unlink_resource(self):
        """Test unlinking a resource from a memory."""
        mock_response = {
            "memory_id": "mem_123",
            "resource_id": "res_456",
            "unlinked": True,
        }
        with patch.object(Trix, "_request") as mock_request:
            mock_request.return_value = mock_response
            client = Trix(api_key="test_key")
            result = client.memories.unlink_resource("mem_123", "res_456")
            assert result["unlinked"] is True
            client.close()

    def test_unlink_resource_validates_ids(self):
        """Test that unlink_resource validates both IDs."""
        client = Trix(api_key="test_key")
        with pytest.raises(ValueError):
            client.memories.unlink_resource("", "res_456")
        client.close()
