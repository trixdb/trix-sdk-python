"""Facts resource for Trix SDK - knowledge facts.

The live API surface is read-mostly under ``/v1/knowledge/facts`` plus
memory-scoped read/create under ``/v1/memories/:id/facts``. The previous
create/get/update/delete/query/find/bulk/extract/verify methods targeted
endpoints that do not exist on the API (they 404), so they have been removed;
only the real surface is exposed here.
"""

from typing import Any, Dict, Optional

from .base import BaseSyncResource
from ..types import (
    Fact,
    FactList,
    MemoryFactCreate,
    MemoryFactsResult,
)
from ..utils.security import validate_id


def _build_fact_params(
    subject: Optional[str] = None,
    predicate: Optional[str] = None,
    obj: Optional[str] = None,
    min_confidence: Optional[float] = None,
    space_id: Optional[str] = None,
    limit: Optional[int] = None,
    page: Optional[int] = None,
    offset: Optional[int] = None,
) -> Dict[str, Any]:
    """Build query parameters for fact listing."""
    params: Dict[str, Any] = {}
    if subject is not None:
        params["subject"] = subject
    if predicate is not None:
        params["predicate"] = predicate
    if obj is not None:
        params["object"] = obj
    if min_confidence is not None:
        params["minConfidence"] = min_confidence
    if space_id is not None:
        params["spaceId"] = space_id
    if limit is not None:
        params["limit"] = limit
    if page is not None:
        params["page"] = page
    if offset is not None:
        params["offset"] = offset
    return params


class FactsResource(BaseSyncResource):
    """Resource for reading account/memory facts and attaching new ones.

    Example:
        >>> # List facts across the account
        >>> facts = client.facts.list(limit=20)
        >>>
        >>> # Read or attach facts for a specific memory
        >>> memory_facts = client.facts.list_for_memory("mem_123")
        >>> fact = client.facts.create_for_memory(
        ...     "mem_123", content="Project deadline is Friday", importance=8
        ... )
    """

    def list(
        self,
        subject: Optional[str] = None,
        predicate: Optional[str] = None,
        obj: Optional[str] = None,
        min_confidence: Optional[float] = None,
        space_id: Optional[str] = None,
        limit: Optional[int] = None,
        page: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> FactList:
        """List facts with optional filters (``GET /knowledge/facts``).

        Args:
            subject: Filter by subject
            predicate: Filter by predicate
            obj: Filter by object
            min_confidence: Minimum confidence threshold
            space_id: Filter by space
            limit: Maximum results to return
            page: Page number
            offset: Result offset

        Returns:
            Paginated list of facts
        """
        params = _build_fact_params(
            subject=subject,
            predicate=predicate,
            obj=obj,
            min_confidence=min_confidence,
            space_id=space_id,
            limit=limit,
            page=page,
            offset=offset,
        )
        response = self._request("GET", "/knowledge/facts", params=params if params else None)
        return FactList.model_validate(response)

    def list_for_memory(self, memory_id: str) -> MemoryFactsResult:
        """List the facts attached to a specific memory.

        ``GET /memories/:id/facts``

        Args:
            memory_id: Memory ID

        Returns:
            Facts for the memory
        """
        validate_id(memory_id, "memory")
        response = self._request("GET", f"/memories/{memory_id}/facts")
        return MemoryFactsResult.model_validate(response)

    def create_for_memory(
        self,
        memory_id: str,
        content: str,
        importance: int,
        category: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Fact:
        """Attach a new fact to a memory.

        ``POST /memories/:id/facts``

        Args:
            memory_id: Memory ID to attach the fact to
            content: The fact content
            importance: Importance score (1-10)
            category: Optional fact category
            metadata: Optional additional metadata

        Returns:
            Created fact
        """
        validate_id(memory_id, "memory")
        data = MemoryFactCreate(
            content=content,
            importance=importance,
            category=category,
            metadata=metadata,
        )
        response = self._request(
            "POST", f"/memories/{memory_id}/facts", json=data.model_dump(exclude_none=True)
        )
        return Fact.model_validate(response)
