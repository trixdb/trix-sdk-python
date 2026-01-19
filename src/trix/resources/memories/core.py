"""Core memories resource implementation.

This module provides the main MemoriesResource and AsyncMemoriesResource classes
that combine all operation mixins into complete resource classes.
"""

from typing import Any, Dict, Iterator, List, Optional

from ...protocols import AsyncClientProtocol, SyncClientProtocol
from ...types import (
    BulkResult,
    Memory,
    MemoryConfig,
    MemoryCreate,
    MemoryList,
    MemoryStats,
    MemoryType,
    SearchMode,
)
from ...utils.pagination import AsyncPaginator, SyncPaginator
from ...utils.security import validate_id

from .audio import AsyncAudioOperationsMixin, AudioOperationsMixin
from .base import (
    build_create_data,
    build_iter_params,
    build_list_params,
    build_stats_params,
    build_update_data,
    validate_bulk_ids,
    validate_bulk_updates,
)
from .image import AsyncImageOperationsMixin, ImageOperationsMixin
from .protection import AsyncProtectionOperationsMixin, ProtectionOperationsMixin
from .resource_links import AsyncResourceLinksMixin, ResourceLinksMixin


class MemoriesResource(
    AudioOperationsMixin,
    ImageOperationsMixin,
    ProtectionOperationsMixin,
    ResourceLinksMixin,
):
    """Resource for managing memories.

    Provides comprehensive operations for memory management including:
    - CRUD operations (create, read, update, delete)
    - Bulk operations
    - Audio upload and transcription
    - Image upload and visual search
    - Memory pinning and protection
    - Resource linking
    """

    def __init__(self, client: SyncClientProtocol) -> None:
        """Initialize memories resource with client."""
        self._client = client

    def create(
        self,
        content: str,
        type: Optional[MemoryType] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        priority: Optional[int] = None,
        space_id: Optional[str] = None,
        options: Optional[Dict[str, Any]] = None,
        is_pinned: bool = False,
        protection_level: str = "none",
    ) -> Memory:
        """Create a new memory.

        Args:
            content: The content of the memory
            type: Type of memory (text, markdown, url, audio)
            tags: List of tags for categorization
            metadata: Additional metadata
            priority: Priority level for the memory
            space_id: ID of the space to add memory to
            options: Additional options (transcribe_audio, language, skip_embedding)
            is_pinned: Whether to pin the memory (prevents decay)
            protection_level: Protection level ("none", "soft", "hard")

        Returns:
            Created memory object
        """
        data = build_create_data(
            content, type, tags, metadata, priority, space_id, options, is_pinned, protection_level
        )
        response = self._client._request(
            "POST", "/memories", json=data.model_dump(exclude_none=True)
        )
        return Memory.model_validate(response)

    def list(
        self,
        q: Optional[str] = None,
        mode: Optional[SearchMode] = None,
        limit: int = 100,
        offset: int = 0,
        tags: Optional[List[str]] = None,
        space_id: Optional[str] = None,
        pinned: Optional[bool] = None,
        protected: Optional[bool] = None,
        min_quality: Optional[float] = None,
        include_deleted: bool = False,
    ) -> MemoryList:
        """List memories with optional filtering.

        Args:
            q: Search query
            mode: Search mode (semantic, keyword, hybrid)
            limit: Maximum number of results
            offset: Offset for pagination
            tags: Filter by tags
            space_id: Filter by space
            pinned: Filter by pinned status
            protected: Filter by protection status
            min_quality: Minimum quality score (0-1)
            include_deleted: Include soft-deleted memories

        Returns:
            List of memories with pagination info
        """
        params = build_list_params(
            q, mode, limit, offset, tags, space_id, pinned, protected, min_quality, include_deleted
        )
        response = self._client._request("GET", "/memories", params=params)
        return MemoryList.model_validate(response)

    def iter(
        self,
        q: Optional[str] = None,
        mode: Optional[SearchMode] = None,
        tags: Optional[List[str]] = None,
        space_id: Optional[str] = None,
        page_size: int = 100,
        max_items: Optional[int] = None,
    ) -> Iterator[Memory]:
        """Iterate through all memories with automatic pagination.

        Args:
            q: Search query
            mode: Search mode
            tags: Filter by tags
            space_id: Filter by space
            page_size: Number of items per page
            max_items: Maximum total items to fetch

        Yields:
            Memory objects
        """
        params = build_iter_params(q, mode, tags, space_id)
        paginator = SyncPaginator(
            self.list,
            initial_params=params,
            limit=page_size,
            max_items=max_items,
        )
        for item in paginator:
            yield Memory.model_validate(item)

    def get(self, id: str) -> Memory:
        """Get a memory by ID.

        Args:
            id: Memory ID

        Returns:
            Memory object
        """
        validate_id(id, "memory")
        response = self._client._request("GET", f"/memories/{id}")
        return Memory.model_validate(response)

    def update(
        self,
        id: str,
        content: Optional[str] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        priority: Optional[int] = None,
    ) -> Memory:
        """Update a memory.

        Args:
            id: Memory ID
            content: New content
            tags: New tags
            metadata: New metadata
            priority: New priority

        Returns:
            Updated memory object
        """
        validate_id(id, "memory")
        data = build_update_data(content, tags, metadata, priority)
        response = self._client._request(
            "PATCH", f"/memories/{id}", json=data.model_dump(exclude_none=True)
        )
        return Memory.model_validate(response)

    def delete(self, id: str) -> None:
        """Delete a memory.

        Args:
            id: Memory ID
        """
        validate_id(id, "memory")
        self._client._request("DELETE", f"/memories/{id}")

    def bulk_create(self, memories: List[MemoryCreate]) -> BulkResult:
        """Create multiple memories at once.

        Args:
            memories: List of memory creation requests

        Returns:
            Bulk operation result with success/failure counts
        """
        data = [m.model_dump(exclude_none=True) for m in memories]
        response = self._client._request("POST", "/memories/bulk", json={"memories": data})
        return BulkResult.model_validate(response)

    def bulk_update(self, updates: List[Dict[str, Any]]) -> BulkResult:
        """Update multiple memories at once.

        Args:
            updates: List of update objects with 'id' and update fields

        Returns:
            Bulk operation result with success/failure counts
        """
        validate_bulk_updates(updates)
        response = self._client._request("PATCH", "/memories/bulk", json={"updates": updates})
        return BulkResult.model_validate(response)

    def bulk_delete(self, ids: List[str]) -> BulkResult:
        """Delete multiple memories at once.

        Args:
            ids: List of memory IDs to delete

        Returns:
            Bulk operation result with success/failure counts
        """
        validate_bulk_ids(ids)
        response = self._client._request("DELETE", "/memories/bulk", json={"ids": ids})
        return BulkResult.model_validate(response)

    def get_config(self) -> MemoryConfig:
        """Get memory system configuration.

        Returns:
            Memory configuration
        """
        response = self._client._request("GET", "/memories/config")
        return MemoryConfig.model_validate(response)

    def get_stats(
        self,
        space_id: Optional[str] = None,
        created_after: Optional[str] = None,
        created_before: Optional[str] = None,
        include_type_distribution: bool = False,
        include_tag_distribution: bool = False,
        include_timeline: bool = False,
        timeline_granularity: Optional[str] = None,
    ) -> MemoryStats:
        """Get memory statistics.

        Args:
            space_id: Filter by space ID
            created_after: Filter by creation date (ISO format)
            created_before: Filter by creation date (ISO format)
            include_type_distribution: Include type distribution in stats
            include_tag_distribution: Include tag distribution in stats
            include_timeline: Include timeline in stats
            timeline_granularity: Timeline granularity (hour, day, week, month)

        Returns:
            Memory statistics
        """
        params = build_stats_params(
            space_id,
            created_after,
            created_before,
            include_type_distribution,
            include_tag_distribution,
            include_timeline,
            timeline_granularity,
        )
        response = self._client._request("GET", "/memories/stats", params=params)
        return MemoryStats.model_validate(response)


class AsyncMemoriesResource(
    AsyncAudioOperationsMixin,
    AsyncImageOperationsMixin,
    AsyncProtectionOperationsMixin,
    AsyncResourceLinksMixin,
):
    """Async resource for managing memories.

    Provides comprehensive async operations for memory management including:
    - CRUD operations (create, read, update, delete)
    - Bulk operations
    - Audio upload and transcription
    - Image upload and visual search
    - Memory pinning and protection
    - Resource linking
    """

    def __init__(self, client: AsyncClientProtocol) -> None:
        """Initialize async memories resource with client."""
        self._client = client

    async def create(
        self,
        content: str,
        type: Optional[MemoryType] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        priority: Optional[int] = None,
        space_id: Optional[str] = None,
        options: Optional[Dict[str, Any]] = None,
        is_pinned: bool = False,
        protection_level: str = "none",
    ) -> Memory:
        """Create a new memory (async)."""
        data = build_create_data(
            content, type, tags, metadata, priority, space_id, options, is_pinned, protection_level
        )
        response = await self._client._request(
            "POST", "/memories", json=data.model_dump(exclude_none=True)
        )
        return Memory.model_validate(response)

    async def list(
        self,
        q: Optional[str] = None,
        mode: Optional[SearchMode] = None,
        limit: int = 100,
        offset: int = 0,
        tags: Optional[List[str]] = None,
        space_id: Optional[str] = None,
        pinned: Optional[bool] = None,
        protected: Optional[bool] = None,
        min_quality: Optional[float] = None,
        include_deleted: bool = False,
    ) -> MemoryList:
        """List memories with optional filtering (async)."""
        params = build_list_params(
            q, mode, limit, offset, tags, space_id, pinned, protected, min_quality, include_deleted
        )
        response = await self._client._request("GET", "/memories", params=params)
        return MemoryList.model_validate(response)

    async def iter(
        self,
        q: Optional[str] = None,
        mode: Optional[SearchMode] = None,
        tags: Optional[List[str]] = None,
        space_id: Optional[str] = None,
        page_size: int = 100,
        max_items: Optional[int] = None,
    ) -> AsyncPaginator:
        """Get async iterator for all memories with automatic pagination.

        Returns:
            Async paginator that yields Memory objects
        """
        params = build_iter_params(q, mode, tags, space_id)
        return AsyncPaginator(
            self.list,
            initial_params=params,
            limit=page_size,
            max_items=max_items,
        )

    async def get(self, id: str) -> Memory:
        """Get a memory by ID (async)."""
        validate_id(id, "memory")
        response = await self._client._request("GET", f"/memories/{id}")
        return Memory.model_validate(response)

    async def update(
        self,
        id: str,
        content: Optional[str] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        priority: Optional[int] = None,
    ) -> Memory:
        """Update a memory (async)."""
        validate_id(id, "memory")
        data = build_update_data(content, tags, metadata, priority)
        response = await self._client._request(
            "PATCH", f"/memories/{id}", json=data.model_dump(exclude_none=True)
        )
        return Memory.model_validate(response)

    async def delete(self, id: str) -> None:
        """Delete a memory (async)."""
        validate_id(id, "memory")
        await self._client._request("DELETE", f"/memories/{id}")

    async def bulk_create(self, memories: List[MemoryCreate]) -> BulkResult:
        """Create multiple memories at once (async)."""
        data = [m.model_dump(exclude_none=True) for m in memories]
        response = await self._client._request("POST", "/memories/bulk", json={"memories": data})
        return BulkResult.model_validate(response)

    async def bulk_update(self, updates: List[Dict[str, Any]]) -> BulkResult:
        """Update multiple memories at once (async)."""
        validate_bulk_updates(updates)
        response = await self._client._request(
            "PATCH", "/memories/bulk", json={"updates": updates}
        )
        return BulkResult.model_validate(response)

    async def bulk_delete(self, ids: List[str]) -> BulkResult:
        """Delete multiple memories at once (async)."""
        validate_bulk_ids(ids)
        response = await self._client._request("DELETE", "/memories/bulk", json={"ids": ids})
        return BulkResult.model_validate(response)

    async def get_config(self) -> MemoryConfig:
        """Get memory system configuration (async)."""
        response = await self._client._request("GET", "/memories/config")
        return MemoryConfig.model_validate(response)

    async def get_stats(
        self,
        space_id: Optional[str] = None,
        created_after: Optional[str] = None,
        created_before: Optional[str] = None,
        include_type_distribution: bool = False,
        include_tag_distribution: bool = False,
        include_timeline: bool = False,
        timeline_granularity: Optional[str] = None,
    ) -> MemoryStats:
        """Get memory statistics (async)."""
        params = build_stats_params(
            space_id,
            created_after,
            created_before,
            include_type_distribution,
            include_tag_distribution,
            include_timeline,
            timeline_granularity,
        )
        response = await self._client._request("GET", "/memories/stats", params=params)
        return MemoryStats.model_validate(response)
