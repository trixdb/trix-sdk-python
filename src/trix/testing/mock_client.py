"""
Mock Trix client for testing.

Provides fully-typed mock clients that can be used in unit tests
without making real API calls.

Example:
    >>> from trix.testing import MockTrix, create_mock_memory
    >>>
    >>> mock_client = MockTrix()
    >>>
    >>> # Configure mock responses
    >>> mock_client.memories.mock_create(create_mock_memory(content="Test"))
    >>>
    >>> # Use in tests
    >>> memory = mock_client.memories.create(content="Test")
    >>> assert memory.content == "Test"
    >>>
    >>> # Verify calls
    >>> assert len(mock_client.memories.create_calls) == 1
    >>> assert mock_client.memories.create_calls[0]["content"] == "Test"
"""

from __future__ import annotations

import random
import string
from dataclasses import dataclass, field
from datetime import datetime
from typing import (
    Any,
    Optional,
    TypeVar,
)

from ..types import (
    BulkResult,
    Cluster,
    Entity,
    Fact,
    Memory,
    MemoryType,
    PaginatedResponse,
    Pagination,
    Relationship,
    RelationshipType,
)

from .mock_resources import (
    MockAsyncClustersResource,
    MockAsyncEntitiesResource,
    MockAsyncFactsResource,
    MockAsyncMemoriesResource,
    MockClustersResource,
    MockEntitiesResource,
    MockFactsResource,
    MockMemoriesResource,
)

# ============================================================================
# Helper Functions
# ============================================================================


def random_id() -> str:
    """Generate a random ID string."""
    return "".join(random.choices(string.ascii_lowercase + string.digits, k=8))


# ============================================================================
# Mock Data Factories
# ============================================================================


def create_mock_memory(
    id: Optional[str] = None,
    space_id: Optional[str] = None,
    content: str = "Mock memory content",
    type: MemoryType = MemoryType.TEXT,
    tags: Optional[list[str]] = None,
    metadata: Optional[dict[str, Any]] = None,
    **kwargs: Any,
) -> Memory:
    """Create a mock Memory object."""
    now = datetime.utcnow()
    return Memory(
        id=id or f"mem_{random_id()}",
        space_id=space_id,
        content=content,
        type=type,
        tags=tags or [],
        metadata=metadata or {},
        created_at=now,
        updated_at=now,
        **kwargs,
    )


def create_mock_cluster(
    id: Optional[str] = None,
    name: str = "Mock Cluster",
    description: str = "A mock cluster for testing",
    color: Optional[str] = None,
    memory_count: int = 0,
    metadata: Optional[dict[str, Any]] = None,
    **kwargs: Any,
) -> Cluster:
    """Create a mock Cluster object."""
    now = datetime.utcnow()
    return Cluster(
        id=id or f"clus_{random_id()}",
        name=name,
        description=description,
        color=color,
        memory_count=memory_count,
        metadata=metadata or {},
        created_at=now,
        updated_at=now,
        **kwargs,
    )


def create_mock_relationship(
    id: Optional[str] = None,
    source_id: Optional[str] = None,
    target_id: Optional[str] = None,
    relationship_type: RelationshipType = RelationshipType.RELATED_TO,
    description: Optional[str] = None,
    weight: float = 1.0,
    bidirectional: bool = False,
    **kwargs: Any,
) -> Relationship:
    """Create a mock Relationship object."""
    now = datetime.utcnow()
    return Relationship(
        id=id or f"rel_{random_id()}",
        source_id=source_id or f"mem_{random_id()}",
        target_id=target_id or f"mem_{random_id()}",
        relationship_type=relationship_type,
        description=description,
        weight=weight,
        bidirectional=bidirectional,
        created_at=now,
        updated_at=now,
        **kwargs,
    )


def create_mock_entity(
    id: Optional[str] = None,
    name: str = "Mock Entity",
    type: str = "person",
    aliases: Optional[list[str]] = None,
    description: Optional[str] = None,
    properties: Optional[dict[str, Any]] = None,
    memory_ids: Optional[list[str]] = None,
    metadata: Optional[dict[str, Any]] = None,
    space_id: Optional[str] = None,
    **kwargs: Any,
) -> Entity:
    """Create a mock Entity object."""
    now = datetime.utcnow()
    return Entity(
        id=id or f"ent_{random_id()}",
        name=name,
        type=type,
        aliases=aliases or [],
        description=description,
        properties=properties or {},
        memory_ids=memory_ids or [],
        metadata=metadata or {},
        space_id=space_id,
        created_at=now,
        updated_at=now,
        **kwargs,
    )


def create_mock_fact(
    id: Optional[str] = None,
    subject: str = "Subject",
    predicate: str = "is",
    object: str = "Object",
    confidence: float = 1.0,
    metadata: Optional[dict[str, Any]] = None,
    space_id: Optional[str] = None,
    **kwargs: Any,
) -> Fact:
    """Create a mock Fact object."""
    now = datetime.utcnow()
    return Fact(
        id=id or f"fact_{random_id()}",
        subject=subject,
        predicate=predicate,
        object=object,
        confidence=confidence,
        metadata=metadata or {},
        space_id=space_id,
        created_at=now,
        updated_at=now,
        **kwargs,
    )


T = TypeVar("T")


def create_mock_paginated_response(
    data: list[T],
    total: Optional[int] = None,
    page: int = 1,
    limit: int = 100,
    has_more: bool = False,
) -> PaginatedResponse[T]:
    """Create a mock paginated response."""
    return PaginatedResponse(
        data=data,
        pagination=Pagination(
            total=total if total is not None else len(data),
            page=page,
            limit=limit,
            has_more=has_more,
        ),
    )


def create_mock_bulk_result(
    success: int = 1,
    failed: int = 0,
    errors: Optional[list[dict[str, Any]]] = None,
) -> BulkResult:
    """Create a mock bulk result."""
    return BulkResult(
        success=success,
        failed=failed,
        errors=errors or [],
    )


# ============================================================================
# Main Mock Clients
# ============================================================================


@dataclass
class MockTrix:
    """Mock Trix client for synchronous testing.

    Example:
        >>> from trix.testing import MockTrix, create_mock_memory
        >>>
        >>> def test_my_service():
        ...     mock_client = MockTrix()
        ...
        ...     # Configure mock responses
        ...     mock_mem = create_mock_memory(content="Test")
        ...     mock_client.memories.mock_create(mock_mem)
        ...
        ...     # Use in tests
        ...     result = my_service.create_memory(mock_client, "Test")
        ...
        ...     assert result.id == mock_mem.id
        ...     assert len(mock_client.memories.create_calls) == 1
        ...     assert mock_client.memories.create_calls[0]["content"] == "Test"
    """

    memories: MockMemoriesResource = field(default_factory=MockMemoriesResource)
    clusters: MockClustersResource = field(default_factory=MockClustersResource)
    entities: MockEntitiesResource = field(default_factory=MockEntitiesResource)
    facts: MockFactsResource = field(default_factory=MockFactsResource)

    def reset(self) -> None:
        """Reset all mock resources and call history."""
        self.memories.reset()
        self.clusters.reset()
        self.entities.reset()
        self.facts.reset()


@dataclass
class MockAsyncTrix:
    """Mock Trix client for asynchronous testing.

    Example:
        >>> from trix.testing import MockAsyncTrix, create_mock_memory
        >>>
        >>> async def test_my_service():
        ...     mock_client = MockAsyncTrix()
        ...
        ...     # Configure mock responses
        ...     mock_mem = create_mock_memory(content="Test")
        ...     mock_client.memories.mock_create(mock_mem)
        ...
        ...     # Use in tests
        ...     result = await my_service.create_memory(mock_client, "Test")
        ...
        ...     assert result.id == mock_mem.id
        ...     assert len(mock_client.memories.create_calls) == 1
    """

    memories: MockAsyncMemoriesResource = field(default_factory=MockAsyncMemoriesResource)
    clusters: MockAsyncClustersResource = field(default_factory=MockAsyncClustersResource)
    entities: MockAsyncEntitiesResource = field(default_factory=MockAsyncEntitiesResource)
    facts: MockAsyncFactsResource = field(default_factory=MockAsyncFactsResource)

    def reset(self) -> None:
        """Reset all mock resources and call history."""
        self.memories.reset()
        self.clusters.reset()
        self.entities.reset()
        self.facts.reset()
