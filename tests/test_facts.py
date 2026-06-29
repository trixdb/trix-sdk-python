"""Tests for the Facts resource.

Covers the live API surface only: account-wide list (``/knowledge/facts``) and
memory-scoped read/create (``/memories/:id/facts``). The previous
create/get/update/delete/query/find/bulk/extract/verify methods targeted
non-existent endpoints (404) and were removed; the regression guards below fail
if any of them are re-introduced.
"""

import pytest
from unittest.mock import Mock, AsyncMock

from trix.resources.facts import FactsResource
from trix.resources.facts_async import AsyncFactsResource

# Subject-Predicate-Object shaped fact used for response parsing.
SPO_FACT = {
    "id": "fact_1",
    "subject": "A",
    "predicate": "is",
    "object": "B",
    "confidence": 1.0,
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z",
}

# Methods that hit endpoints which do not exist on the real API.
REMOVED_FACT_METHODS = [
    "create",
    "get",
    "update",
    "delete",
    "query",
    "find_by_subject",
    "find_by_predicate",
    "find_by_object",
    "bulk_create",
    "bulk_delete",
    "extract",
    "verify",
]


class TestFactsResource:
    """Tests for FactsResource (sync)."""

    def test_list_facts_hits_knowledge_facts(self):
        """list() must call GET /knowledge/facts."""
        mock_client = Mock()
        mock_client._request.return_value = {
            "data": [SPO_FACT],
            "total": 1,
            "limit": 10,
            "offset": 0,
        }

        resource = FactsResource(mock_client)
        result = resource.list()

        call_args = mock_client._request.call_args
        assert call_args[0] == ("GET", "/knowledge/facts")
        assert len(result.data) == 1

    def test_list_facts_passes_filters(self):
        """list() forwards filters as query params."""
        mock_client = Mock()
        mock_client._request.return_value = {"data": [], "total": 0, "limit": 10, "offset": 0}

        resource = FactsResource(mock_client)
        resource.list(subject="Einstein", min_confidence=0.9)

        call_args = mock_client._request.call_args
        assert call_args[0][1] == "/knowledge/facts"
        assert call_args[1]["params"]["subject"] == "Einstein"

    def test_list_for_memory_hits_memory_facts(self):
        """list_for_memory() must call GET /memories/:id/facts."""
        mock_client = Mock()
        mock_client._request.return_value = {
            "memory_id": "11111111-1111-1111-1111-111111111111",
            "facts": [SPO_FACT],
            "total": 1,
        }

        resource = FactsResource(mock_client)
        result = resource.list_for_memory("11111111-1111-1111-1111-111111111111")

        call_args = mock_client._request.call_args
        assert call_args[0] == (
            "GET",
            "/memories/11111111-1111-1111-1111-111111111111/facts",
        )
        assert result.total == 1
        assert len(result.facts) == 1

    def test_list_for_memory_rejects_invalid_id(self):
        """An invalid memory id is rejected before any request is issued."""
        mock_client = Mock()
        resource = FactsResource(mock_client)
        with pytest.raises(ValueError):
            resource.list_for_memory("../etc/passwd")
        mock_client._request.assert_not_called()

    def test_create_for_memory_posts_content_body(self):
        """create_for_memory() POSTs the content/importance body to /memories/:id/facts."""
        mock_client = Mock()
        mock_client._request.return_value = SPO_FACT

        resource = FactsResource(mock_client)
        result = resource.create_for_memory(
            "11111111-1111-1111-1111-111111111111",
            content="Project deadline is Friday",
            importance=8,
        )

        call_args = mock_client._request.call_args
        assert call_args[0][0] == "POST"
        assert call_args[0][1] == "/memories/11111111-1111-1111-1111-111111111111/facts"
        body = call_args[1]["json"]
        assert body["content"] == "Project deadline is Friday"
        assert body["importance"] == 8
        # Not the SPO triple shape.
        assert "subject" not in body and "predicate" not in body
        assert result.id == "fact_1"

    @pytest.mark.parametrize("name", REMOVED_FACT_METHODS)
    def test_invented_methods_are_removed(self, name):
        """Regression guard: invented (404) methods must not exist."""
        assert not hasattr(FactsResource, name)


class TestAsyncFactsResource:
    """Tests for AsyncFactsResource."""

    @pytest.mark.asyncio
    async def test_list_facts(self):
        mock_client = AsyncMock()
        mock_client._request.return_value = {
            "data": [SPO_FACT],
            "total": 1,
            "limit": 10,
            "offset": 0,
        }

        resource = AsyncFactsResource(mock_client)
        result = await resource.list()

        call_args = mock_client._request.call_args
        assert call_args[0] == ("GET", "/knowledge/facts")
        assert len(result.data) == 1

    @pytest.mark.asyncio
    async def test_create_for_memory(self):
        mock_client = AsyncMock()
        mock_client._request.return_value = SPO_FACT

        resource = AsyncFactsResource(mock_client)
        await resource.create_for_memory(
            "11111111-1111-1111-1111-111111111111", content="hi", importance=5
        )

        call_args = mock_client._request.call_args
        assert call_args[0][1] == "/memories/11111111-1111-1111-1111-111111111111/facts"

    @pytest.mark.parametrize("name", REMOVED_FACT_METHODS)
    def test_invented_methods_are_removed(self, name):
        """Regression guard for the async resource too."""
        assert not hasattr(AsyncFactsResource, name)
