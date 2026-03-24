"""Tests for SearchResource."""

from unittest.mock import Mock

from trix.resources.search import SearchResource


SEARCH_RESULT_DATA = {
    "data": [
        {
            "memory": {
                "id": "mem_123",
                "content": "Test memory content",
                "type": "text",
                "tags": ["test"],
                "metadata": {},
                "priority": 5,
                "space_id": "space_123",
                "created_at": "2025-01-01T00:00:00Z",
                "updated_at": "2025-01-01T00:00:00Z",
                "access_count": 0,
            },
            "score": 0.95,
            "highlights": ["Test memory"],
        }
    ],
    "query": "test query",
}

EMPTY_SEARCH_RESULTS = {"data": [], "query": "nothing"}

EMBEDDING_RESPONSE = {
    "memory_ids": ["mem_123", "mem_456"],
    "embeddings": [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]],
}

EMBED_ALL_RESPONSE = {
    "total_processed": 42,
    "batch_size": 100,
    "status": "completed",
}

SEARCH_CONFIG = {
    "default_limit": 10,
    "max_limit": 100,
    "min_similarity_threshold": 0.5,
}


class TestSearchQuery:
    """Tests for search.query()."""

    def test_query_basic(self):
        """Test basic semantic search query."""
        mock_client = Mock()
        mock_client._request.return_value = SEARCH_RESULT_DATA

        resource = SearchResource(mock_client)
        result = resource.query("test query")

        call_args = mock_client._request.call_args
        assert call_args[0] == ("GET", "/search")
        assert call_args[1]["params"]["q"] == "test query"
        assert call_args[1]["params"]["limit"] == 10
        assert len(result.data) == 1
        assert result.data[0].score == 0.95
        assert result.query == "test query"

    def test_query_with_filters(self):
        """Test search query with tags, threshold, and limit."""
        mock_client = Mock()
        mock_client._request.return_value = SEARCH_RESULT_DATA

        resource = SearchResource(mock_client)
        resource.query(
            "test query",
            limit=20,
            threshold=0.8,
            tags=["important", "work"],
            space_id="space_abc",
        )

        call_args = mock_client._request.call_args
        params = call_args[1]["params"]
        assert params["q"] == "test query"
        assert params["limit"] == 20
        assert params["threshold"] == "0.8"
        assert params["tags"] == "important,work"
        assert params["space_id"] == "space_abc"

    def test_query_with_cluster_scale(self):
        """Test search query filtered by cluster scale."""
        mock_client = Mock()
        mock_client._request.return_value = SEARCH_RESULT_DATA

        resource = SearchResource(mock_client)
        resource.query("test query", cluster_scale="coarse")

        call_args = mock_client._request.call_args
        assert call_args[1]["params"]["cluster_scale"] == "coarse"

    def test_query_empty_results(self):
        """Test search query returning no results."""
        mock_client = Mock()
        mock_client._request.return_value = EMPTY_SEARCH_RESULTS

        resource = SearchResource(mock_client)
        result = resource.query("nothing")

        assert len(result.data) == 0
        assert result.query == "nothing"


class TestSearchSimilar:
    """Tests for search.similar()."""

    def test_similar_basic(self):
        """Test finding similar memories by memory ID."""
        mock_client = Mock()
        mock_client._request.return_value = SEARCH_RESULT_DATA

        resource = SearchResource(mock_client)
        result = resource.similar("mem_123")

        call_args = mock_client._request.call_args
        assert call_args[0] == ("GET", "/search/similar/mem_123")
        assert call_args[1]["params"]["limit"] == 10
        assert len(result.data) == 1

    def test_similar_with_threshold(self):
        """Test similar search with threshold and limit."""
        mock_client = Mock()
        mock_client._request.return_value = SEARCH_RESULT_DATA

        resource = SearchResource(mock_client)
        resource.similar("mem_123", limit=5, threshold=0.7)

        call_args = mock_client._request.call_args
        params = call_args[1]["params"]
        assert params["limit"] == 5
        assert params["threshold"] == "0.7"


class TestSearchEmbed:
    """Tests for search.embed() and embed_all()."""

    def test_embed_memory_ids(self):
        """Test generating embeddings for specific memories."""
        mock_client = Mock()
        mock_client._request.return_value = EMBEDDING_RESPONSE

        resource = SearchResource(mock_client)
        result = resource.embed(["mem_123", "mem_456"])

        call_args = mock_client._request.call_args
        assert call_args[0] == ("POST", "/search/embed")
        assert call_args[1]["json"]["memory_ids"] == ["mem_123", "mem_456"]
        assert result.memory_ids == ["mem_123", "mem_456"]
        assert len(result.embeddings) == 2

    def test_embed_all_default_batch(self):
        """Test embed_all with default batch size."""
        mock_client = Mock()
        mock_client._request.return_value = EMBED_ALL_RESPONSE

        resource = SearchResource(mock_client)
        result = resource.embed_all()

        call_args = mock_client._request.call_args
        assert call_args[0] == ("POST", "/search/embed-all")
        assert call_args[1]["params"]["batch_size"] == 100
        assert result.total_processed == 42
        assert result.status == "completed"

    def test_embed_all_custom_batch(self):
        """Test embed_all with custom batch size."""
        mock_client = Mock()
        mock_client._request.return_value = EMBED_ALL_RESPONSE

        resource = SearchResource(mock_client)
        resource.embed_all(batch_size=500)

        call_args = mock_client._request.call_args
        assert call_args[1]["params"]["batch_size"] == 500


class TestSearchByTopic:
    """Tests for search.by_topic()."""

    def test_by_topic_basic(self):
        """Test searching memories by topic."""
        mock_client = Mock()
        mock_client._request.return_value = SEARCH_RESULT_DATA

        resource = SearchResource(mock_client)
        result = resource.by_topic("machine learning")

        call_args = mock_client._request.call_args
        assert call_args[0] == ("GET", "/search/topic")
        assert call_args[1]["params"]["topic"] == "machine learning"
        assert call_args[1]["params"]["limit"] == 10
        assert len(result.data) == 1

    def test_by_topic_with_space(self):
        """Test searching by topic within a space."""
        mock_client = Mock()
        mock_client._request.return_value = SEARCH_RESULT_DATA

        resource = SearchResource(mock_client)
        resource.by_topic("machine learning", limit=20, space_id="space_abc")

        call_args = mock_client._request.call_args
        params = call_args[1]["params"]
        assert params["limit"] == 20
        assert params["space_id"] == "space_abc"


class TestSearchConfig:
    """Tests for search.get_config()."""

    def test_get_config(self):
        """Test getting search configuration."""
        mock_client = Mock()
        mock_client._request.return_value = SEARCH_CONFIG

        resource = SearchResource(mock_client)
        result = resource.get_config()

        call_args = mock_client._request.call_args
        assert call_args[0] == ("GET", "/search/config")
        assert result.default_limit == 10
        assert result.max_limit == 100
        assert result.min_similarity_threshold == 0.5
