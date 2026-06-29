"""Synchronous entities resource for Trix SDK - named entities.

The live API surface is read-mostly under ``/v1/knowledge/entities`` plus a
merge endpoint. The previous create/update/delete/search/resolve/bulk/extract/
link/get_types/find_by_memory methods targeted endpoints that do not exist on
the API (they 404), so they have been removed; only the real surface is
exposed here.
"""

from typing import Any, Dict, Optional

from .base import BaseSyncResource
from ..types import (
    Entity,
    EntityList,
    EntityMergeResult,
    EntityFactsResult,
)
from ..utils.security import validate_id


def _build_entity_params(
    entity_type: Optional[str] = None,
    space_id: Optional[str] = None,
    limit: Optional[int] = None,
    page: Optional[int] = None,
    offset: Optional[int] = None,
) -> Dict[str, Any]:
    """Build query parameters for entity listing."""
    params: Dict[str, Any] = {}
    if entity_type is not None:
        params["type"] = entity_type
    if space_id is not None:
        params["spaceId"] = space_id
    if limit is not None:
        params["limit"] = limit
    if page is not None:
        params["page"] = page
    if offset is not None:
        params["offset"] = offset
    return params


class EntitiesResource(BaseSyncResource):
    """Resource for reading named entities and merging duplicates.

    Example:
        >>> entities = client.entities.list(entity_type="person")
        >>> entity = client.entities.get("ent_123")
        >>> facts = client.entities.get_facts("ent_123")
    """

    def get(self, id: str) -> Entity:
        """Get an entity by ID (``GET /knowledge/entities/:id``).

        Args:
            id: Entity ID

        Returns:
            Entity object

        Raises:
            ValidationError: If ID format is invalid
            NotFoundError: If entity doesn't exist
        """
        validate_id(id, "entity")
        response = self._request("GET", f"/knowledge/entities/{id}")
        return Entity.model_validate(response)

    def list(
        self,
        entity_type: Optional[str] = None,
        space_id: Optional[str] = None,
        limit: Optional[int] = None,
        page: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> EntityList:
        """List entities with optional filters (``GET /knowledge/entities``).

        Args:
            entity_type: Filter by entity type
            space_id: Filter by space
            limit: Maximum results to return
            page: Page number
            offset: Result offset

        Returns:
            Paginated list of entities
        """
        params = _build_entity_params(
            entity_type=entity_type,
            space_id=space_id,
            limit=limit,
            page=page,
            offset=offset,
        )
        response = self._request("GET", "/knowledge/entities", params=params if params else None)
        return EntityList.model_validate(response)

    def find_by_type(
        self,
        entity_type: str,
        limit: Optional[int] = None,
    ) -> EntityList:
        """Find entities by type (filtered ``GET /knowledge/entities``)."""
        return self.list(entity_type=entity_type, limit=limit)

    def get_facts(self, entity_id: str) -> EntityFactsResult:
        """Get facts about an entity (``GET /knowledge/entities/:id/facts``).

        Args:
            entity_id: Entity ID

        Returns:
            Facts where the entity is the subject or object
        """
        validate_id(entity_id, "entity")
        response = self._request("GET", f"/knowledge/entities/{entity_id}/facts")
        return EntityFactsResult.model_validate(response)

    def merge(self, target_id: str, source_id: str) -> EntityMergeResult:
        """Merge two entities (``POST /knowledge/entities/merge``).

        The source entity is merged into the target and deleted. Both ids ride
        in the body (the endpoint is not nested under an entity id).

        Args:
            target_id: ID of the entity to merge into
            source_id: ID of the entity to merge from (will be deleted)

        Returns:
            Merge result with the merged entity
        """
        validate_id(target_id, "entity")
        validate_id(source_id, "entity")
        response = self._request(
            "POST",
            "/knowledge/entities/merge",
            json={"source_id": source_id, "target_id": target_id},
        )
        return EntityMergeResult.model_validate(response)
