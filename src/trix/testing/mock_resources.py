"""
Mock resource classes for testing.

Provides typed mock resource classes that track method calls
and return configured responses.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import (
    Any,
    Callable,
    Generic,
    Optional,
    TypeVar,
    Union,
)

from ..types import (
    BulkResult,
    Cluster,
    Entity,
    Fact,
    Memory,
    PaginatedResponse,
    Pagination,
)

T = TypeVar("T")
TItem = TypeVar("TItem")
MockResponse = Union[TItem, Exception, Callable[[], TItem]]


def _default_paginated_response() -> PaginatedResponse[Any]:
    """Create an empty paginated response for default mock behavior."""
    return PaginatedResponse(
        data=[],
        pagination=Pagination(total=0, page=1, limit=100, has_more=False),
    )


def _default_bulk_result(count: int) -> BulkResult:
    """Create a default bulk result for mock behavior."""
    return BulkResult(success=count, failed=0, errors=[])


# ============================================================================
# Mock Resource Classes (Sync)
# ============================================================================


@dataclass
class MockResource(Generic[TItem]):
    """Base mock resource with call tracking."""

    _create_response: Optional[MockResponse[TItem]] = None
    _list_response: Optional[MockResponse[PaginatedResponse[TItem]]] = None
    _get_response: Optional[MockResponse[TItem]] = None
    _update_response: Optional[MockResponse[TItem]] = None
    _delete_response: Optional[MockResponse[None]] = None

    create_calls: list[dict[str, Any]] = field(default_factory=list)
    list_calls: list[dict[str, Any]] = field(default_factory=list)
    get_calls: list[str] = field(default_factory=list)
    update_calls: list[dict[str, Any]] = field(default_factory=list)
    delete_calls: list[str] = field(default_factory=list)

    def mock_create(self, response: MockResponse[TItem]) -> None:
        """Set mock response for create calls."""
        self._create_response = response

    def mock_list(self, response: MockResponse[PaginatedResponse[TItem]]) -> None:
        """Set mock response for list calls."""
        self._list_response = response

    def mock_get(self, response: MockResponse[TItem]) -> None:
        """Set mock response for get calls."""
        self._get_response = response

    def mock_update(self, response: MockResponse[TItem]) -> None:
        """Set mock response for update calls."""
        self._update_response = response

    def mock_delete(self, response: MockResponse[None]) -> None:
        """Set mock response for delete calls."""
        self._delete_response = response

    def _resolve_response(self, response: Optional[MockResponse[T]]) -> T:
        """Resolve a mock response value."""
        if response is None:
            raise ValueError("No mock response configured")
        if isinstance(response, Exception):
            raise response
        if callable(response):
            return response()
        return response

    def create(self, **kwargs: Any) -> TItem:
        """Mock create method."""
        self.create_calls.append(kwargs)
        return self._resolve_response(self._create_response)

    def list(self, **kwargs: Any) -> PaginatedResponse[TItem]:
        """Mock list method."""
        self.list_calls.append(kwargs)
        return self._resolve_response(self._list_response)

    def get(self, id: str) -> TItem:
        """Mock get method."""
        self.get_calls.append(id)
        return self._resolve_response(self._get_response)

    def update(self, id: str, **kwargs: Any) -> TItem:
        """Mock update method."""
        self.update_calls.append({"id": id, **kwargs})
        return self._resolve_response(self._update_response)

    def delete(self, id: str) -> None:
        """Mock delete method."""
        self.delete_calls.append(id)
        self._resolve_response(self._delete_response)  # type: ignore[arg-type]

    def reset(self) -> None:
        """Reset all mock responses and call history."""
        self._create_response = None
        self._list_response = None
        self._get_response = None
        self._update_response = None
        self._delete_response = None
        self.create_calls.clear()
        self.list_calls.clear()
        self.get_calls.clear()
        self.update_calls.clear()
        self.delete_calls.clear()


@dataclass
class MockMemoriesResource(MockResource[Memory]):
    """Mock Memories resource with additional methods."""

    _bulk_create_response: Optional[MockResponse[BulkResult]] = None
    bulk_create_calls: list[list[dict[str, Any]]] = field(default_factory=list)

    def mock_bulk_create(self, response: MockResponse[BulkResult]) -> None:
        """Set mock response for bulk_create calls."""
        self._bulk_create_response = response

    def bulk_create(self, memories: list[dict[str, Any]]) -> BulkResult:
        """Mock bulk_create method."""
        self.bulk_create_calls.append(memories)
        if self._bulk_create_response is None:
            return _default_bulk_result(len(memories))
        return self._resolve_response(self._bulk_create_response)


@dataclass
class MockClustersResource(MockResource[Cluster]):
    """Mock Clusters resource."""

    pass


@dataclass
class MockEntitiesResource(MockResource[Entity]):
    """Mock Entities resource with search."""

    _search_response: Optional[MockResponse[PaginatedResponse[Entity]]] = None
    search_calls: list[dict[str, Any]] = field(default_factory=list)

    def mock_search(self, response: MockResponse[PaginatedResponse[Entity]]) -> None:
        """Set mock response for search calls."""
        self._search_response = response

    def search(self, query: str, **kwargs: Any) -> PaginatedResponse[Entity]:
        """Mock search method."""
        self.search_calls.append({"query": query, **kwargs})
        if self._search_response is None:
            return _default_paginated_response()
        return self._resolve_response(self._search_response)


@dataclass
class MockFactsResource(MockResource[Fact]):
    """Mock Facts resource."""

    pass


# ============================================================================
# Mock Resource Classes (Async)
# ============================================================================


@dataclass
class MockAsyncResource(Generic[TItem]):
    """Base async mock resource with call tracking."""

    _create_response: Optional[MockResponse[TItem]] = None
    _list_response: Optional[MockResponse[PaginatedResponse[TItem]]] = None
    _get_response: Optional[MockResponse[TItem]] = None
    _update_response: Optional[MockResponse[TItem]] = None
    _delete_response: Optional[MockResponse[None]] = None

    create_calls: list[dict[str, Any]] = field(default_factory=list)
    list_calls: list[dict[str, Any]] = field(default_factory=list)
    get_calls: list[str] = field(default_factory=list)
    update_calls: list[dict[str, Any]] = field(default_factory=list)
    delete_calls: list[str] = field(default_factory=list)

    def mock_create(self, response: MockResponse[TItem]) -> None:
        """Set mock response for create calls."""
        self._create_response = response

    def mock_list(self, response: MockResponse[PaginatedResponse[TItem]]) -> None:
        """Set mock response for list calls."""
        self._list_response = response

    def mock_get(self, response: MockResponse[TItem]) -> None:
        """Set mock response for get calls."""
        self._get_response = response

    def mock_update(self, response: MockResponse[TItem]) -> None:
        """Set mock response for update calls."""
        self._update_response = response

    def mock_delete(self, response: MockResponse[None]) -> None:
        """Set mock response for delete calls."""
        self._delete_response = response

    def _resolve_response(self, response: Optional[MockResponse[T]]) -> T:
        """Resolve a mock response value."""
        if response is None:
            raise ValueError("No mock response configured")
        if isinstance(response, Exception):
            raise response
        if callable(response):
            return response()
        return response

    async def create(self, **kwargs: Any) -> TItem:
        """Mock async create method."""
        self.create_calls.append(kwargs)
        return self._resolve_response(self._create_response)

    async def list(self, **kwargs: Any) -> PaginatedResponse[TItem]:
        """Mock async list method."""
        self.list_calls.append(kwargs)
        return self._resolve_response(self._list_response)

    async def get(self, id: str) -> TItem:
        """Mock async get method."""
        self.get_calls.append(id)
        return self._resolve_response(self._get_response)

    async def update(self, id: str, **kwargs: Any) -> TItem:
        """Mock async update method."""
        self.update_calls.append({"id": id, **kwargs})
        return self._resolve_response(self._update_response)

    async def delete(self, id: str) -> None:
        """Mock async delete method."""
        self.delete_calls.append(id)
        self._resolve_response(self._delete_response)  # type: ignore[arg-type]

    def reset(self) -> None:
        """Reset all mock responses and call history."""
        self._create_response = None
        self._list_response = None
        self._get_response = None
        self._update_response = None
        self._delete_response = None
        self.create_calls.clear()
        self.list_calls.clear()
        self.get_calls.clear()
        self.update_calls.clear()
        self.delete_calls.clear()


@dataclass
class MockAsyncMemoriesResource(MockAsyncResource[Memory]):
    """Mock async Memories resource."""

    _bulk_create_response: Optional[MockResponse[BulkResult]] = None
    bulk_create_calls: list[list[dict[str, Any]]] = field(default_factory=list)

    def mock_bulk_create(self, response: MockResponse[BulkResult]) -> None:
        """Set mock response for bulk_create calls."""
        self._bulk_create_response = response

    async def bulk_create(self, memories: list[dict[str, Any]]) -> BulkResult:
        """Mock async bulk_create method."""
        self.bulk_create_calls.append(memories)
        if self._bulk_create_response is None:
            return _default_bulk_result(len(memories))
        return self._resolve_response(self._bulk_create_response)


@dataclass
class MockAsyncClustersResource(MockAsyncResource[Cluster]):
    """Mock async Clusters resource."""

    pass


@dataclass
class MockAsyncEntitiesResource(MockAsyncResource[Entity]):
    """Mock async Entities resource with search."""

    _search_response: Optional[MockResponse[PaginatedResponse[Entity]]] = None
    search_calls: list[dict[str, Any]] = field(default_factory=list)

    def mock_search(self, response: MockResponse[PaginatedResponse[Entity]]) -> None:
        """Set mock response for search calls."""
        self._search_response = response

    async def search(self, query: str, **kwargs: Any) -> PaginatedResponse[Entity]:
        """Mock async search method."""
        self.search_calls.append({"query": query, **kwargs})
        if self._search_response is None:
            return _default_paginated_response()
        return self._resolve_response(self._search_response)


@dataclass
class MockAsyncFactsResource(MockAsyncResource[Fact]):
    """Mock async Facts resource."""

    pass
