"""Async entities resource for Trix SDK - named entities.

The live API surface is read-mostly under ``/v1/knowledge/entities`` plus a
merge endpoint. The previous create/update/delete/search/resolve/bulk/extract/
link/get_types/find_by_memory methods targeted endpoints that do not exist on
the API (they 404) and have been removed.
"""

from typing import Optional

from .base import BaseAsyncResource
from ..types import (
    Entity,
    EntityList,
    EntityMergeResult,
    EntityFactsResult,
)
from ..utils.security import validate_id
from .entities import _build_entity_params


class AsyncEntitiesResource(BaseAsyncResource):
    """Async resource for reading named entities and merging duplicates."""

    async def get(self, id: str) -> Entity:
        """Get an entity by ID (``GET /knowledge/entities/:id``)."""
        validate_id(id, "entity")
        response = await self._request("GET", f"/knowledge/entities/{id}")
        return Entity.model_validate(response)

    async def list(
        self,
        entity_type: Optional[str] = None,
        space_id: Optional[str] = None,
        limit: Optional[int] = None,
        page: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> EntityList:
        """List entities with optional filters (``GET /knowledge/entities``)."""
        params = _build_entity_params(
            entity_type=entity_type,
            space_id=space_id,
            limit=limit,
            page=page,
            offset=offset,
        )
        response = await self._request(
            "GET", "/knowledge/entities", params=params if params else None
        )
        return EntityList.model_validate(response)

    async def find_by_type(
        self,
        entity_type: str,
        limit: Optional[int] = None,
    ) -> EntityList:
        """Find entities by type (filtered ``GET /knowledge/entities``)."""
        return await self.list(entity_type=entity_type, limit=limit)

    async def get_facts(self, entity_id: str) -> EntityFactsResult:
        """Get facts about an entity (``GET /knowledge/entities/:id/facts``)."""
        validate_id(entity_id, "entity")
        response = await self._request("GET", f"/knowledge/entities/{entity_id}/facts")
        return EntityFactsResult.model_validate(response)

    async def merge(self, target_id: str, source_id: str) -> EntityMergeResult:
        """Merge two entities (``POST /knowledge/entities/merge``).

        The source entity is merged into the target and deleted; both ids ride
        in the body (the endpoint is not nested under an entity id).
        """
        validate_id(target_id, "entity")
        validate_id(source_id, "entity")
        response = await self._request(
            "POST",
            "/knowledge/entities/merge",
            json={"source_id": source_id, "target_id": target_id},
        )
        return EntityMergeResult.model_validate(response)
