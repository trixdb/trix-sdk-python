"""Async facts resource for Trix SDK - knowledge facts.

The live API surface is read-mostly under ``/v1/knowledge/facts`` plus
memory-scoped read/create under ``/v1/memories/:id/facts``. The previous
create/get/update/delete/query/find/bulk/extract/verify methods targeted
endpoints that do not exist on the API (they 404) and have been removed.
"""

from typing import Any, Dict, Optional

from .base import BaseAsyncResource
from ..types import (
    Fact,
    FactList,
    MemoryFactCreate,
    MemoryFactsResult,
)
from ..utils.security import validate_id
from .facts import _build_fact_params


class AsyncFactsResource(BaseAsyncResource):
    """Async resource for reading account/memory facts and attaching new ones."""

    async def list(
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
        """List facts with optional filters (``GET /knowledge/facts``)."""
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
        response = await self._request("GET", "/knowledge/facts", params=params if params else None)
        return FactList.model_validate(response)

    async def list_for_memory(self, memory_id: str) -> MemoryFactsResult:
        """List the facts attached to a specific memory (``GET /memories/:id/facts``)."""
        validate_id(memory_id, "memory")
        response = await self._request("GET", f"/memories/{memory_id}/facts")
        return MemoryFactsResult.model_validate(response)

    async def create_for_memory(
        self,
        memory_id: str,
        content: str,
        importance: int,
        category: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Fact:
        """Attach a new fact to a memory (``POST /memories/:id/facts``)."""
        validate_id(memory_id, "memory")
        data = MemoryFactCreate(
            content=content,
            importance=importance,
            category=category,
            metadata=metadata,
        )
        response = await self._request(
            "POST", f"/memories/{memory_id}/facts", json=data.model_dump(exclude_none=True)
        )
        return Fact.model_validate(response)
