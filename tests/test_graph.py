"""Tests for graph expansion functionality."""

import pytest
from httpx import Response
from trix.types import GraphExpansionResult


def test_graph_expand_basic(sync_client, respx_mock):
    """Test basic graph expansion from seed memories."""
    # Arrange
    mock_response = {
        "seed_memories": ["mem_1", "mem_2"],
        "expanded_memories": [
            {
                "id": "mem_3",
                "content": "Related memory",
                "type": "text",
                "tags": [],
                "metadata": {},
                "created_at": "2024-01-01T00:00:00Z",
                "updated_at": "2024-01-01T00:00:00Z",
                "access_count": 0,
            }
        ],
        "relationships": [
            {
                "id": "rel_1",
                "source_id": "mem_1",
                "target_id": "mem_3",
                "relationship_type": "related_to",
                "strength": 0.8,
                "created_at": "2024-01-01T00:00:00Z",
                "updated_at": "2024-01-01T00:00:00Z",
            }
        ],
        "stats": {
            "seed_count": 2,
            "expanded_count": 1,
            "final_count": 1,
            "relationships_found": 1,
            "hops_used": 1,
        },
        "scoring": None,
    }

    respx_mock.post("https://test.api.com/graph/expand").mock(
        return_value=Response(200, json=mock_response)
    )

    # Act
    result = sync_client.graph.expand(seed_memory_ids=["mem_1", "mem_2"])

    # Assert
    assert isinstance(result, GraphExpansionResult)
    assert result.seed_memories == ["mem_1", "mem_2"]
    assert len(result.expanded_memories) == 1
    assert result.expanded_memories[0].id == "mem_3"
    assert len(result.relationships) == 1
    # Verify relationship has strength field from graph expansion
    assert result.relationships[0].strength == 0.8
    assert result.stats.seed_count == 2
    assert result.stats.expanded_count == 1
    assert result.scoring is None


def test_graph_expand_with_options(sync_client, respx_mock):
    """Test graph expansion with all optional parameters."""
    # Arrange
    mock_response = {
        "seed_memories": ["mem_1"],
        "expanded_memories": [],
        "relationships": [],
        "stats": {
            "seed_count": 1,
            "expanded_count": 0,
            "final_count": 0,
        },
        "scoring": None,
    }

    respx_mock.post("https://test.api.com/graph/expand").mock(
        return_value=Response(200, json=mock_response)
    )

    # Act
    result = sync_client.graph.expand(
        seed_memory_ids=["mem_1"],
        max_hops=3,
        min_weight=0.5,
        relationship_types=["related_to", "supports"],
        direction="outgoing",
        include_content=False,
        apply_hybrid_scoring=False,
    )

    # Assert
    assert isinstance(result, GraphExpansionResult)
    assert result.seed_memories == ["mem_1"]
    assert len(result.expanded_memories) == 0


def test_graph_expand_with_hybrid_scoring(sync_client, respx_mock):
    """Test graph expansion with hybrid scoring enabled."""
    # Arrange
    mock_response = {
        "seed_memories": ["mem_1"],
        "expanded_memories": [
            {
                "id": "mem_2",
                "content": "Scored memory",
                "type": "text",
                "tags": [],
                "metadata": {},
                "created_at": "2024-01-01T00:00:00Z",
                "updated_at": "2024-01-01T00:00:00Z",
                "access_count": 0,
                "score": 0.85,
            }
        ],
        "relationships": [],
        "stats": {
            "seed_count": 1,
            "expanded_count": 1,
            "final_count": 1,
        },
        "scoring": {
            "applied": True,
            "weights": {
                "semantic": 0.4,
                "graph": 0.3,
                "co_activation": 0.2,
                "recency": 0.05,
                "salience": 0.05,
            },
        },
    }

    respx_mock.post("https://test.api.com/graph/expand").mock(
        return_value=Response(200, json=mock_response)
    )

    # Act
    result = sync_client.graph.expand(
        seed_memory_ids=["mem_1"], apply_hybrid_scoring=True
    )

    # Assert
    assert isinstance(result, GraphExpansionResult)
    assert result.scoring is not None
    assert result.scoring.applied is True
    assert result.scoring.weights is not None
    assert result.scoring.weights.semantic == 0.4
    assert result.scoring.weights.graph == 0.3
    assert result.scoring.weights.co_activation == 0.2


def test_graph_expand_empty_seed_memories_error(sync_client):
    """Test that expand raises error with empty seed memories list."""
    # Act & Assert
    with pytest.raises(ValueError, match="seed_memory_ids cannot be empty"):
        sync_client.graph.expand(seed_memory_ids=[])


@pytest.mark.asyncio
async def test_graph_expand_async_basic(async_client, respx_mock):
    """Test async graph expansion from seed memories."""
    # Arrange
    mock_response = {
        "seed_memories": ["mem_1"],
        "expanded_memories": [
            {
                "id": "mem_2",
                "content": "Related",
                "type": "text",
                "tags": [],
                "metadata": {},
                "created_at": "2024-01-01T00:00:00Z",
                "updated_at": "2024-01-01T00:00:00Z",
                "access_count": 0,
            }
        ],
        "relationships": [],
        "stats": {
            "seed_count": 1,
            "expanded_count": 1,
            "final_count": 1,
        },
        "scoring": None,
    }

    respx_mock.post("https://test.api.com/graph/expand").mock(
        return_value=Response(200, json=mock_response)
    )

    # Act
    result = await async_client.graph.expand(seed_memory_ids=["mem_1"])

    # Assert
    assert isinstance(result, GraphExpansionResult)
    assert result.seed_memories == ["mem_1"]
    assert len(result.expanded_memories) == 1


@pytest.mark.asyncio
async def test_graph_expand_async_empty_error(async_client):
    """Test that async expand raises error with empty seed memories list."""
    # Act & Assert
    with pytest.raises(ValueError, match="seed_memory_ids cannot be empty"):
        await async_client.graph.expand(seed_memory_ids=[])


def test_relationship_strength_and_weight_fields(sync_client, respx_mock):
    """Test that Relationship model supports both strength and weight fields."""
    # Arrange - Test with strength field (from graph expansion)
    mock_response_strength = {
        "seed_memories": ["mem_1"],
        "expanded_memories": [],
        "relationships": [
            {
                "id": "rel_1",
                "source_id": "mem_1",
                "target_id": "mem_2",
                "relationship_type": "related_to",
                "strength": 0.9,  # Graph expansion uses strength
                "created_at": "2024-01-01T00:00:00Z",
                "updated_at": "2024-01-01T00:00:00Z",
            }
        ],
        "stats": {"seed_count": 1, "expanded_count": 0, "final_count": 0},
        "scoring": None,
    }

    respx_mock.post("https://test.api.com/graph/expand").mock(
        return_value=Response(200, json=mock_response_strength)
    )

    # Act
    result = sync_client.graph.expand(seed_memory_ids=["mem_1"])

    # Assert - Verify strength field is populated
    assert len(result.relationships) == 1
    assert result.relationships[0].strength == 0.9
    assert result.relationships[0].weight == 1.0  # Default value when not provided
