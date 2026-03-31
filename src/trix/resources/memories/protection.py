"""Memory protection operations mixin.

Provides pinning, protection level, and soft delete operations.
"""

from typing import Any, List, Optional

from ...types import Memory, Topic
from ...utils.security import validate_id
from .base import build_topics_params, validate_protection_level


class ProtectionOperationsMixin:
    """Mixin providing protection operations for sync memories resource."""

    _client: Any  # Type hint for the client

    def pin(self, id: str) -> Memory:
        """Pin a memory to prevent decay."""
        validate_id(id, "memory")
        response = self._client._request("POST", f"/memories/{id}/pin")
        return Memory.model_validate(response)

    def unpin(self, id: str) -> Memory:
        """Unpin a memory to allow normal decay."""
        validate_id(id, "memory")
        response = self._client._request("POST", f"/memories/{id}/unpin")
        return Memory.model_validate(response)

    def set_protection_level(self, id: str, level: str) -> Memory:
        """Set memory protection level."""
        validate_id(id, "memory")
        validate_protection_level(level)
        response = self._client._request(
            "POST", f"/memories/{id}/protection", json={"level": level}
        )
        return Memory.model_validate(response)

    def soft_delete(self, id: str) -> Memory:
        """Soft delete a memory (can be restored)."""
        validate_id(id, "memory")
        response = self._client._request("POST", f"/memories/{id}/soft-delete")
        return Memory.model_validate(response)

    def restore(self, id: str) -> Memory:
        """Restore a soft-deleted memory."""
        validate_id(id, "memory")
        response = self._client._request("POST", f"/memories/{id}/restore")
        return Memory.model_validate(response)

    def get_quality_score(self, id: str) -> float:
        """Get the quality score for a memory."""
        validate_id(id, "memory")
        response = self._client._request("GET", f"/memories/{id}/quality")
        return float(response.get("quality_score", 0.0))

    def get_topics(
        self,
        id: str,
        refresh: bool = False,
        min_relevance: Optional[float] = None,
        categories: Optional[List[str]] = None,
    ) -> List[Topic]:
        """Get extracted topics for a memory."""
        validate_id(id, "memory")
        params = build_topics_params(refresh, min_relevance, categories)
        response = self._client._request("GET", f"/memories/{id}/topics", params=params)
        return [Topic.model_validate(t) for t in response.get("topics", [])]


class AsyncProtectionOperationsMixin:
    """Mixin providing protection operations for async memories resource."""

    _client: Any  # Type hint for the client

    async def pin(self, id: str) -> Memory:
        """Pin a memory to prevent decay (async)."""
        validate_id(id, "memory")
        response = await self._client._request("POST", f"/memories/{id}/pin")
        return Memory.model_validate(response)

    async def unpin(self, id: str) -> Memory:
        """Unpin a memory to allow normal decay (async)."""
        validate_id(id, "memory")
        response = await self._client._request("POST", f"/memories/{id}/unpin")
        return Memory.model_validate(response)

    async def set_protection_level(self, id: str, level: str) -> Memory:
        """Set memory protection level (async)."""
        validate_id(id, "memory")
        validate_protection_level(level)
        response = await self._client._request(
            "POST", f"/memories/{id}/protection", json={"level": level}
        )
        return Memory.model_validate(response)

    async def soft_delete(self, id: str) -> Memory:
        """Soft delete a memory (can be restored) (async)."""
        validate_id(id, "memory")
        response = await self._client._request("POST", f"/memories/{id}/soft-delete")
        return Memory.model_validate(response)

    async def restore(self, id: str) -> Memory:
        """Restore a soft-deleted memory (async)."""
        validate_id(id, "memory")
        response = await self._client._request("POST", f"/memories/{id}/restore")
        return Memory.model_validate(response)

    async def get_quality_score(self, id: str) -> float:
        """Get the quality score for a memory (async)."""
        validate_id(id, "memory")
        response = await self._client._request("GET", f"/memories/{id}/quality")
        return float(response.get("quality_score", 0.0))

    async def get_topics(
        self,
        id: str,
        refresh: bool = False,
        min_relevance: Optional[float] = None,
        categories: Optional[List[str]] = None,
    ) -> List[Topic]:
        """Get extracted topics for a memory (async)."""
        validate_id(id, "memory")
        params = build_topics_params(refresh, min_relevance, categories)
        response = await self._client._request("GET", f"/memories/{id}/topics", params=params)
        return [Topic.model_validate(t) for t in response.get("topics", [])]
