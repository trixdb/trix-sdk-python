"""Pytest configuration and fixtures."""

import pytest

from tests.support import spec_async_client, spec_client
from trix import AsyncTrix, Trix


@pytest.fixture
def mock_trix():
    """A spec'd sync client mock (issue #12).

    Unlike a bare ``Mock()``, accessing an attribute the real ``Trix`` client
    does not expose raises ``AttributeError`` instead of fabricating a child
    mock — so tests catch calls to client methods that do not exist.
    """
    return spec_client()


@pytest.fixture
def mock_async_trix():
    """A spec'd async client mock (issue #12) — see :func:`mock_trix`."""
    return spec_async_client()


@pytest.fixture
def sync_client():
    """Provide a sync Trix client for testing."""
    client = Trix(api_key="test_api_key", base_url="https://test.api.com")
    yield client
    client.close()


@pytest.fixture
async def async_client():
    """Provide an async Trix client for testing."""
    client = AsyncTrix(api_key="test_api_key", base_url="https://test.api.com")
    yield client
    await client.close()


@pytest.fixture
def mock_memory_response():
    """Provide mock memory response data."""
    return {
        "id": "mem_123",
        "content": "Test memory content",
        "type": "text",
        "tags": ["test"],
        "metadata": {"source": "test"},
        "created_at": "2025-01-01T00:00:00Z",
        "updated_at": "2025-01-01T00:00:00Z",
        "access_count": 0,
    }


@pytest.fixture
def mock_relationship_response():
    """Provide mock relationship response data."""
    return {
        "id": "rel_123",
        "source_id": "mem_123",
        "target_id": "mem_456",
        "relationship_type": "related_to",
        "weight": 1.0,
        "bidirectional": False,
        "created_at": "2025-01-01T00:00:00Z",
        "updated_at": "2025-01-01T00:00:00Z",
        "reinforcement_count": 0,
    }
