"""Tests for relationships resource."""

import pytest
from unittest.mock import patch

from trix import (
    Trix,
    AsyncTrix,
    Relationship,
    RelationshipList,
    RelationshipType,
)


@pytest.fixture
def mock_relationship_data():
    """Mock relationship response data."""
    return {
        "id": "rel_123",
        "source_id": "mem_001",
        "target_id": "mem_002",
        "relationship_type": "related_to",
        "description": "Test relationship",
        "weight": 1.0,
        "strength": 0.8,
        "bidirectional": False,
        "created_at": "2025-01-01T00:00:00Z",
        "updated_at": "2025-01-01T00:00:00Z",
        "reinforcement_count": 0,
    }


@pytest.fixture
def mock_relationship_list_data(mock_relationship_data):
    """Mock relationship list response data."""
    return {"data": [mock_relationship_data]}


class TestRelationshipsCreate:
    """Tests for relationships.create()."""

    def test_create_basic(self, mock_relationship_data):
        """Test basic relationship creation."""
        with patch.object(Trix, "_request") as mock_request:
            mock_request.return_value = mock_relationship_data
            client = Trix(api_key="test_key")

            rel = client.relationships.create(
                source_id="mem_001",
                target_id="mem_002",
                relationship_type=RelationshipType.RELATED_TO,
            )

            assert isinstance(rel, Relationship)
            assert rel.id == "rel_123"
            assert rel.source_id == "mem_001"
            assert rel.target_id == "mem_002"
            mock_request.assert_called_once()
            client.close()

    def test_create_with_options(self, mock_relationship_data):
        """Test relationship creation with all options."""
        with patch.object(Trix, "_request") as mock_request:
            mock_request.return_value = mock_relationship_data
            client = Trix(api_key="test_key")

            rel = client.relationships.create(
                source_id="mem_001",
                target_id="mem_002",
                relationship_type=RelationshipType.RELATED_TO,
                description="Strong connection",
                weight=2.0,
                bidirectional=True,
            )

            assert isinstance(rel, Relationship)
            call_args = mock_request.call_args
            assert call_args[0][0] == "POST"
            assert call_args[0][1] == "/relationships/mem_001/create/mem_002"
            body = call_args[1]["json"]
            assert body["description"] == "Strong connection"
            assert body["weight"] == 2.0
            assert body["bidirectional"] is True
            client.close()


class TestRelationshipsGet:
    """Tests for relationships.get_incoming() and get_outgoing()."""

    def test_get_incoming(self, mock_relationship_list_data):
        """Test getting incoming relationships."""
        with patch.object(Trix, "_request") as mock_request:
            mock_request.return_value = mock_relationship_list_data
            client = Trix(api_key="test_key")

            result = client.relationships.get_incoming("mem_001")

            assert isinstance(result, RelationshipList)
            assert len(result.data) == 1
            mock_request.assert_called_with("GET", "/relationships/mem_001/incoming")
            client.close()

    def test_get_outgoing(self, mock_relationship_list_data):
        """Test getting outgoing relationships."""
        with patch.object(Trix, "_request") as mock_request:
            mock_request.return_value = mock_relationship_list_data
            client = Trix(api_key="test_key")

            result = client.relationships.get_outgoing("mem_001")

            assert isinstance(result, RelationshipList)
            assert len(result.data) == 1
            mock_request.assert_called_with("GET", "/relationships/mem_001/outgoing")
            client.close()


class TestRelationshipsUpdate:
    """Tests for relationships.update()."""

    def test_update_weight(self, mock_relationship_data):
        """Test updating relationship weight."""
        with patch.object(Trix, "_request") as mock_request:
            mock_relationship_data["weight"] = 2.5
            mock_request.return_value = mock_relationship_data
            client = Trix(api_key="test_key")

            rel = client.relationships.update("rel_123", weight=2.5)

            assert rel.weight == 2.5
            call_args = mock_request.call_args
            assert call_args[0][0] == "PATCH"
            assert call_args[0][1] == "/relationships/rel_123"
            client.close()

    def test_update_description(self, mock_relationship_data):
        """Test updating relationship description."""
        with patch.object(Trix, "_request") as mock_request:
            mock_relationship_data["description"] = "Updated description"
            mock_request.return_value = mock_relationship_data
            client = Trix(api_key="test_key")

            rel = client.relationships.update("rel_123", description="Updated description")

            assert rel.description == "Updated description"
            client.close()


class TestRelationshipsDelete:
    """Tests for relationships.delete()."""

    def test_delete_by_id(self):
        """Test deleting a relationship by ID."""
        with patch.object(Trix, "_request") as mock_request:
            mock_request.return_value = {}
            client = Trix(api_key="test_key")

            client.relationships.delete("rel_123")

            mock_request.assert_called_with("DELETE", "/relationships/rel_123")
            client.close()


class TestRelationshipsReinforceWeaken:
    """Tests for relationships.reinforce() and weaken()."""

    def test_reinforce(self, mock_relationship_data):
        """Test reinforcing a relationship."""
        with patch.object(Trix, "_request") as mock_request:
            mock_relationship_data["weight"] = 1.5
            mock_request.return_value = mock_relationship_data
            client = Trix(api_key="test_key")

            rel = client.relationships.reinforce("rel_123", boost=0.5)

            assert isinstance(rel, Relationship)
            call_args = mock_request.call_args
            assert call_args[0][0] == "POST"
            assert call_args[0][1] == "/relationships/rel_123/reinforce"
            assert call_args[1]["params"]["boost"] == "0.5"
            client.close()

    def test_reinforce_with_context(self, mock_relationship_data):
        """Test reinforcing with context."""
        with patch.object(Trix, "_request") as mock_request:
            mock_request.return_value = mock_relationship_data
            client = Trix(api_key="test_key")

            client.relationships.reinforce("rel_123", context="co-occurred in search")

            call_args = mock_request.call_args
            assert call_args[1]["params"]["context"] == "co-occurred in search"
            client.close()

    def test_weaken(self, mock_relationship_data):
        """Test weakening a relationship."""
        with patch.object(Trix, "_request") as mock_request:
            mock_relationship_data["weight"] = 0.8
            mock_request.return_value = mock_relationship_data
            client = Trix(api_key="test_key")

            rel = client.relationships.weaken("rel_123", amount=0.2)

            assert isinstance(rel, Relationship)
            call_args = mock_request.call_args
            assert call_args[0][0] == "POST"
            assert call_args[0][1] == "/relationships/rel_123/weaken"
            assert call_args[1]["json"]["amount"] == 0.2
            client.close()


class TestRelationshipsBulk:
    """Tests for bulk relationship operations."""

    def test_reinforce_group(self):
        """Test reinforcing a group of relationships."""
        with patch.object(Trix, "_request") as mock_request:
            mock_request.return_value = {"reinforced": 2, "failed": 0}
            client = Trix(api_key="test_key")

            result = client.relationships.reinforce_group(
                ["rel_123", "rel_456"], amount=0.1
            )

            assert result.reinforced == 2
            assert result.failed == 0
            call_args = mock_request.call_args
            assert call_args[0][0] == "POST"
            assert call_args[0][1] == "/relationships/reinforce-group"
            body = call_args[1]["json"]
            assert body["relationship_ids"] == ["rel_123", "rel_456"]
            assert body["amount"] == 0.1
            client.close()


class TestAsyncRelationships:
    """Tests for async relationships operations."""

    @pytest.mark.asyncio
    async def test_async_create(self, mock_relationship_data):
        """Test async relationship creation."""
        with patch.object(AsyncTrix, "_request") as mock_request:
            mock_request.return_value = mock_relationship_data
            async with AsyncTrix(api_key="test_key") as client:
                rel = await client.relationships.create(
                    source_id="mem_001",
                    target_id="mem_002",
                    relationship_type=RelationshipType.RELATED_TO,
                )
                assert rel.id == "rel_123"

    @pytest.mark.asyncio
    async def test_async_get_incoming(self, mock_relationship_list_data):
        """Test async get incoming relationships."""
        with patch.object(AsyncTrix, "_request") as mock_request:
            mock_request.return_value = mock_relationship_list_data
            async with AsyncTrix(api_key="test_key") as client:
                result = await client.relationships.get_incoming("mem_001")
                assert len(result.data) == 1

    @pytest.mark.asyncio
    async def test_async_delete(self):
        """Test async relationship deletion."""
        with patch.object(AsyncTrix, "_request") as mock_request:
            mock_request.return_value = {}
            async with AsyncTrix(api_key="test_key") as client:
                await client.relationships.delete("rel_123")
                mock_request.assert_called_with("DELETE", "/relationships/rel_123")
