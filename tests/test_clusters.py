"""Tests for ClustersResource."""

from unittest.mock import Mock

from trix.resources.clusters import ClustersResource


CLUSTER_RESPONSE = {
    "id": "cluster_123",
    "name": "Work Projects",
    "description": "All work-related memories",
    "color": "#FF5733",
    "metadata": {"category": "work"},
    "memory_count": 10,
    "created_at": "2025-01-01T00:00:00Z",
    "updated_at": "2025-01-01T00:00:00Z",
}

CLUSTER_LIST_RESPONSE = {
    "data": [CLUSTER_RESPONSE],
    "cursor": "next_page_cursor",
}

MEMBERSHIP_RESPONSE = {
    "cluster_id": "cluster_123",
    "memory_id": "mem_456",
    "confidence": 0.95,
    "added_at": "2025-01-01T00:00:00Z",
}


class TestClustersCreate:
    """Tests for clusters.create()."""

    def test_create_basic(self):
        """Test creating a cluster with name only."""
        mock_client = Mock()
        mock_client._request.return_value = CLUSTER_RESPONSE

        resource = ClustersResource(mock_client)
        result = resource.create(name="Work Projects")

        call_args = mock_client._request.call_args
        assert call_args[0] == ("POST", "/clusters")
        assert call_args[1]["json"]["name"] == "Work Projects"
        assert result.id == "cluster_123"
        assert result.name == "Work Projects"

    def test_create_with_all_options(self):
        """Test creating a cluster with all options."""
        mock_client = Mock()
        mock_client._request.return_value = CLUSTER_RESPONSE

        resource = ClustersResource(mock_client)
        resource.create(
            name="Work Projects",
            description="All work-related memories",
            color="#FF5733",
            metadata={"category": "work"},
        )

        call_args = mock_client._request.call_args
        body = call_args[1]["json"]
        assert body["name"] == "Work Projects"
        assert body["description"] == "All work-related memories"
        assert body["color"] == "#FF5733"
        assert body["metadata"] == {"category": "work"}


class TestClustersList:
    """Tests for clusters.list()."""

    def test_list_basic(self):
        """Test listing clusters with defaults."""
        mock_client = Mock()
        mock_client._request.return_value = CLUSTER_LIST_RESPONSE

        resource = ClustersResource(mock_client)
        result = resource.list()

        call_args = mock_client._request.call_args
        assert call_args[0] == ("GET", "/clusters")
        assert call_args[1]["params"]["limit"] == 100
        assert len(result.data) == 1
        assert result.cursor == "next_page_cursor"

    def test_list_with_filters(self):
        """Test listing clusters with query and scale filter."""
        mock_client = Mock()
        mock_client._request.return_value = CLUSTER_LIST_RESPONSE

        resource = ClustersResource(mock_client)
        resource.list(q="work", scale="fine", limit=50, sort="name")

        call_args = mock_client._request.call_args
        params = call_args[1]["params"]
        assert params["q"] == "work"
        assert params["scale"] == "fine"
        assert params["limit"] == 50
        assert params["sort"] == "name"

    def test_list_empty(self):
        """Test listing when no clusters exist."""
        mock_client = Mock()
        mock_client._request.return_value = {"data": [], "cursor": None}

        resource = ClustersResource(mock_client)
        result = resource.list()

        assert len(result.data) == 0


class TestClustersGet:
    """Tests for clusters.get()."""

    def test_get_by_id(self):
        """Test getting a cluster by ID."""
        mock_client = Mock()
        mock_client._request.return_value = CLUSTER_RESPONSE

        resource = ClustersResource(mock_client)
        result = resource.get("cluster_123")

        call_args = mock_client._request.call_args
        assert call_args[0] == ("GET", "/clusters/cluster_123")
        assert result.id == "cluster_123"
        assert result.name == "Work Projects"

    def test_get_with_memories(self):
        """Test getting a cluster with included memories."""
        mock_client = Mock()
        mock_client._request.return_value = CLUSTER_RESPONSE

        resource = ClustersResource(mock_client)
        resource.get("cluster_123", include_memories=True)

        call_args = mock_client._request.call_args
        assert call_args[1]["params"]["include_memories"] == "true"


class TestClustersUpdate:
    """Tests for clusters.update()."""

    def test_update_name(self):
        """Test updating a cluster name."""
        mock_client = Mock()
        updated = {**CLUSTER_RESPONSE, "name": "Updated Name"}
        mock_client._request.return_value = updated

        resource = ClustersResource(mock_client)
        result = resource.update("cluster_123", name="Updated Name")

        call_args = mock_client._request.call_args
        assert call_args[0] == ("PATCH", "/clusters/cluster_123")
        assert call_args[1]["json"]["name"] == "Updated Name"
        assert result.name == "Updated Name"


class TestClustersDelete:
    """Tests for clusters.delete()."""

    def test_delete_by_id(self):
        """Test deleting a cluster."""
        mock_client = Mock()
        mock_client._request.return_value = None

        resource = ClustersResource(mock_client)
        resource.delete("cluster_123")

        call_args = mock_client._request.call_args
        assert call_args[0] == ("DELETE", "/clusters/cluster_123")


class TestClustersMemories:
    """Tests for clusters.add_memory() and remove_memory()."""

    def test_add_memory(self):
        """Test adding a memory to a cluster."""
        mock_client = Mock()
        mock_client._request.return_value = MEMBERSHIP_RESPONSE

        resource = ClustersResource(mock_client)
        result = resource.add_memory("cluster_123", "mem_456", confidence=0.95)

        call_args = mock_client._request.call_args
        assert call_args[0] == ("POST", "/clusters/cluster_123/memories/mem_456")
        assert call_args[1]["json"]["confidence"] == 0.95
        assert result.cluster_id == "cluster_123"
        assert result.memory_id == "mem_456"
        assert result.confidence == 0.95

    def test_add_memory_default_confidence(self):
        """Test adding a memory with default confidence."""
        mock_client = Mock()
        mock_client._request.return_value = {
            **MEMBERSHIP_RESPONSE,
            "confidence": 1.0,
        }

        resource = ClustersResource(mock_client)
        result = resource.add_memory("cluster_123", "mem_456")

        call_args = mock_client._request.call_args
        assert call_args[1]["json"]["confidence"] == 1.0
        assert result.confidence == 1.0

    def test_remove_memory(self):
        """Test removing a memory from a cluster."""
        mock_client = Mock()
        mock_client._request.return_value = None

        resource = ClustersResource(mock_client)
        resource.remove_memory("cluster_123", "mem_456")

        call_args = mock_client._request.call_args
        assert call_args[0] == ("DELETE", "/clusters/cluster_123/memories/mem_456")


class TestClustersExpand:
    """Tests for clusters.expand()."""

    def test_expand_basic(self):
        """Test expanding a cluster with default params."""
        mock_client = Mock()
        mock_client._request.return_value = {
            "suggestions": [
                {"memory_id": "mem_789", "score": 0.85},
                {"memory_id": "mem_101", "score": 0.78},
            ],
        }

        resource = ClustersResource(mock_client)
        result = resource.expand("cluster_123")

        call_args = mock_client._request.call_args
        assert call_args[0] == ("POST", "/clusters/cluster_123/expand")
        assert call_args[1]["params"]["limit"] == 10
        assert call_args[1]["params"]["threshold"] == 0.7
        assert len(result) == 2
        assert result[0]["memory_id"] == "mem_789"
