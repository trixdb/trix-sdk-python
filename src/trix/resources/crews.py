"""Crews resource for Trix SDK (ADR-067 Phase 5)."""

from typing import Any, Dict, Optional

from .base import BaseAsyncResource, BaseSyncResource
from ..types.crew import (
    Crew,
    CrewCreate,
    CrewList,
    CrewUpdate,
)
from ..utils.security import validate_id


class CrewsResource(BaseSyncResource):
    """Resource for managing bot crews (groups of bots)."""

    def create(self, name: str, **kwargs: Any) -> Crew:
        """Create a new crew."""
        data = CrewCreate(name=name, **kwargs)
        response = self._request("POST", "/crews", json=data.model_dump(exclude_none=True))
        return Crew.model_validate(response)

    def list(
        self,
        status: Optional[str] = None,
        limit: int = 20,
        offset: int = 0,
    ) -> CrewList:
        """List crews with optional filtering."""
        params: Dict[str, Any] = {"limit": limit, "offset": offset}
        if status is not None:
            params["status"] = status
        response = self._request("GET", "/crews", params=params)
        return CrewList.model_validate(response)

    def get(self, crew_id: str) -> Crew:
        """Get a crew by ID."""
        validate_id(crew_id, "crew")
        response = self._request("GET", f"/crews/{crew_id}")
        return Crew.model_validate(response)

    def update(self, crew_id: str, **kwargs: Any) -> Crew:
        """Update a crew."""
        validate_id(crew_id, "crew")
        data = CrewUpdate(**kwargs)
        response = self._request(
            "PATCH", f"/crews/{crew_id}", json=data.model_dump(exclude_none=True)
        )
        return Crew.model_validate(response)

    def delete(self, crew_id: str) -> None:
        """Delete a crew."""
        validate_id(crew_id, "crew")
        self._request("DELETE", f"/crews/{crew_id}")


class AsyncCrewsResource(BaseAsyncResource):
    """Async resource for managing bot crews (groups of bots)."""

    async def create(self, name: str, **kwargs: Any) -> Crew:
        """Create a new crew (async)."""
        data = CrewCreate(name=name, **kwargs)
        response = await self._request("POST", "/crews", json=data.model_dump(exclude_none=True))
        return Crew.model_validate(response)

    async def list(
        self,
        status: Optional[str] = None,
        limit: int = 20,
        offset: int = 0,
    ) -> CrewList:
        """List crews with optional filtering (async)."""
        params: Dict[str, Any] = {"limit": limit, "offset": offset}
        if status is not None:
            params["status"] = status
        response = await self._request("GET", "/crews", params=params)
        return CrewList.model_validate(response)

    async def get(self, crew_id: str) -> Crew:
        """Get a crew by ID (async)."""
        validate_id(crew_id, "crew")
        response = await self._request("GET", f"/crews/{crew_id}")
        return Crew.model_validate(response)

    async def update(self, crew_id: str, **kwargs: Any) -> Crew:
        """Update a crew (async)."""
        validate_id(crew_id, "crew")
        data = CrewUpdate(**kwargs)
        response = await self._request(
            "PATCH", f"/crews/{crew_id}", json=data.model_dump(exclude_none=True)
        )
        return Crew.model_validate(response)

    async def delete(self, crew_id: str) -> None:
        """Delete a crew (async)."""
        validate_id(crew_id, "crew")
        await self._request("DELETE", f"/crews/{crew_id}")
