"""Tests for the Entities resource.

Covers the live API surface only: read-mostly under ``/knowledge/entities`` plus
merge. The previous create/update/delete/search/resolve/bulk/extract/link/
get_types/find_by_memory methods targeted non-existent endpoints (404) and were
removed; the regression guards below fail if any are re-introduced.
"""

import pytest
from unittest.mock import Mock, AsyncMock

from trix.resources.entities import EntitiesResource
from trix.resources.entities_async import AsyncEntitiesResource

ENTITY = {
    "id": "ent_123",
    "name": "Albert Einstein",
    "type": "person",
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z",
}

# Methods that hit endpoints which do not exist on the real API.
REMOVED_ENTITY_METHODS = [
    "create",
    "update",
    "delete",
    "search",
    "resolve",
    "find_by_memory",
    "link_to_memory",
    "unlink_from_memory",
    "bulk_create",
    "bulk_delete",
    "extract",
    "get_types",
]


class TestEntitiesResource:
    """Tests for EntitiesResource (sync)."""

    def test_get_entity_hits_knowledge_entities(self):
        """get() must call GET /knowledge/entities/:id."""
        mock_client = Mock()
        mock_client._request.return_value = ENTITY

        resource = EntitiesResource(mock_client)
        result = resource.get("ent_123")

        call_args = mock_client._request.call_args
        assert call_args[0] == ("GET", "/knowledge/entities/ent_123")
        assert result.id == "ent_123"

    def test_list_entities(self):
        """list() must call GET /knowledge/entities."""
        mock_client = Mock()
        mock_client._request.return_value = {
            "data": [ENTITY],
            "total": 1,
            "limit": 10,
            "offset": 0,
        }

        resource = EntitiesResource(mock_client)
        result = resource.list()

        call_args = mock_client._request.call_args
        assert call_args[0] == ("GET", "/knowledge/entities")
        assert len(result.data) == 1

    def test_find_by_type_filters_via_list(self):
        """find_by_type() filters through the list endpoint."""
        mock_client = Mock()
        mock_client._request.return_value = {"data": [], "total": 0, "limit": 10, "offset": 0}

        resource = EntitiesResource(mock_client)
        resource.find_by_type("person")

        call_args = mock_client._request.call_args
        assert call_args[0][1] == "/knowledge/entities"
        assert call_args[1]["params"]["type"] == "person"

    def test_get_facts_hits_knowledge_entities_facts(self):
        """get_facts() must call GET /knowledge/entities/:id/facts (not /entities/:id/facts)."""
        mock_client = Mock()
        mock_client._request.return_value = {
            "entity_id": "ent_123",
            "facts": [
                {
                    "id": "fact_1",
                    "subject": "ent_123",
                    "predicate": "born_in",
                    "object": "Germany",
                    "confidence": 0.95,
                    "created_at": "2024-01-01T00:00:00Z",
                    "updated_at": "2024-01-01T00:00:00Z",
                },
            ],
        }

        resource = EntitiesResource(mock_client)
        result = resource.get_facts("ent_123")

        call_args = mock_client._request.call_args
        assert call_args[0] == ("GET", "/knowledge/entities/ent_123/facts")
        assert len(result.facts) == 1

    def test_merge_posts_both_ids_to_knowledge_entities_merge(self):
        """merge() POSTs both ids to /knowledge/entities/merge (not nested under an id)."""
        mock_client = Mock()
        mock_client._request.return_value = {
            "merged_entity": ENTITY,
            "deleted_id": "ent_2",
        }

        resource = EntitiesResource(mock_client)
        result = resource.merge("ent_1", "ent_2")

        call_args = mock_client._request.call_args
        assert call_args[0][0] == "POST"
        assert call_args[0][1] == "/knowledge/entities/merge"
        body = call_args[1]["json"]
        assert body == {"source_id": "ent_2", "target_id": "ent_1"}
        assert result.deleted_id == "ent_2"

    def test_merge_validates_both_ids(self):
        """merge() rejects empty ids before issuing a request."""
        mock_client = Mock()
        resource = EntitiesResource(mock_client)
        with pytest.raises(ValueError):
            resource.merge("", "ent_2")
        with pytest.raises(ValueError):
            resource.merge("ent_1", "")
        mock_client._request.assert_not_called()

    @pytest.mark.parametrize("name", REMOVED_ENTITY_METHODS)
    def test_invented_methods_are_removed(self, name):
        """Regression guard: invented (404) methods must not exist."""
        assert not hasattr(EntitiesResource, name)


class TestAsyncEntitiesResource:
    """Tests for AsyncEntitiesResource."""

    @pytest.mark.asyncio
    async def test_get_entity(self):
        mock_client = AsyncMock()
        mock_client._request.return_value = ENTITY

        resource = AsyncEntitiesResource(mock_client)
        result = await resource.get("ent_123")

        call_args = mock_client._request.call_args
        assert call_args[0] == ("GET", "/knowledge/entities/ent_123")
        assert result.id == "ent_123"

    @pytest.mark.asyncio
    async def test_merge(self):
        mock_client = AsyncMock()
        mock_client._request.return_value = {"merged_entity": ENTITY, "deleted_id": "ent_2"}

        resource = AsyncEntitiesResource(mock_client)
        await resource.merge("ent_1", "ent_2")

        call_args = mock_client._request.call_args
        assert call_args[0][1] == "/knowledge/entities/merge"
        assert call_args[1]["json"] == {"source_id": "ent_2", "target_id": "ent_1"}

    @pytest.mark.parametrize("name", REMOVED_ENTITY_METHODS)
    def test_invented_methods_are_removed(self, name):
        """Regression guard for the async resource too."""
        assert not hasattr(AsyncEntitiesResource, name)
