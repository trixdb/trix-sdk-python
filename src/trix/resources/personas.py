"""Personas resource for Trix SDK."""

from typing import Optional, List, Dict, Any

from .base import BaseAsyncResource, BaseSyncResource
from ..types.persona import (
    Persona,
    PersonaCreate,
    PersonaList,
    PersonaUpdate,
    PersonaAddSpace,
    PersonaSpace,
)
from ..utils.security import validate_id


class PersonasResource(BaseSyncResource):
    """Resource for managing personas.

    Personas are named identities with purpose, behavioral configuration,
    and multi-space access control.

    Example:
        >>> persona = client.personas.create(
        ...     name="Research",
        ...     purpose="Academic research",
        ... )
    """

    def create(
        self,
        name: str,
        slug: Optional[str] = None,
        avatar_url: Optional[str] = None,
        purpose: Optional[str] = None,
        system_prompt: Optional[str] = None,
        goals: Optional[List[Dict[str, Any]]] = None,
        settings: Optional[Dict[str, Any]] = None,
        is_default: Optional[bool] = None,
        can_create_spaces: Optional[bool] = None,
    ) -> Persona:
        """Create a new persona."""
        data = PersonaCreate(
            name=name, slug=slug, avatar_url=avatar_url, purpose=purpose,
            system_prompt=system_prompt, goals=goals, settings=settings,
            is_default=is_default, can_create_spaces=can_create_spaces,
        )
        response = self._request("POST", "/personas", json=data.model_dump(exclude_none=True))
        return Persona.model_validate(response)

    def list(self) -> PersonaList:
        """List all personas."""
        response = self._request("GET", "/personas")
        return PersonaList.model_validate(response)

    def get(self, id: str) -> Persona:
        """Get a persona by ID."""
        validate_id(id, "persona")
        response = self._request("GET", f"/personas/{id}")
        return Persona.model_validate(response)

    def get_by_slug(self, slug: str) -> Persona:
        """Get a persona by slug."""
        if not slug:
            raise ValueError("persona slug cannot be empty")
        response = self._request("GET", f"/personas/slug/{slug}")
        return Persona.model_validate(response)

    def update(
        self,
        id: str,
        name: Optional[str] = None,
        slug: Optional[str] = None,
        avatar_url: Optional[str] = None,
        purpose: Optional[str] = None,
        system_prompt: Optional[str] = None,
        goals: Optional[List[Dict[str, Any]]] = None,
        settings: Optional[Dict[str, Any]] = None,
        is_default: Optional[bool] = None,
        can_create_spaces: Optional[bool] = None,
    ) -> Persona:
        """Update a persona."""
        validate_id(id, "persona")
        data = PersonaUpdate(
            name=name, slug=slug, avatar_url=avatar_url, purpose=purpose,
            system_prompt=system_prompt, goals=goals, settings=settings,
            is_default=is_default, can_create_spaces=can_create_spaces,
        )
        response = self._request(
            "PATCH", f"/personas/{id}", json=data.model_dump(exclude_none=True)
        )
        return Persona.model_validate(response)

    def delete(self, id: str) -> None:
        """Delete a persona."""
        validate_id(id, "persona")
        self._request("DELETE", f"/personas/{id}")

    def add_space(
        self,
        persona_id: str,
        space_id: str,
        role: str = "member",
        can_create_memories: bool = True,
        can_delete_memories: bool = False,
    ) -> PersonaSpace:
        """Add a space to a persona."""
        validate_id(persona_id, "persona")
        data = PersonaAddSpace(
            space_id=space_id, role=role,
            can_create_memories=can_create_memories,
            can_delete_memories=can_delete_memories,
        )
        response = self._request(
            "POST", f"/personas/{persona_id}/spaces", json=data.model_dump()
        )
        return PersonaSpace.model_validate(response)

    def remove_space(self, persona_id: str, space_id: str) -> None:
        """Remove a space from a persona."""
        validate_id(persona_id, "persona")
        validate_id(space_id, "space")
        self._request("DELETE", f"/personas/{persona_id}/spaces/{space_id}")


class AsyncPersonasResource(BaseAsyncResource):
    """Async resource for managing personas."""

    async def create(
        self,
        name: str,
        slug: Optional[str] = None,
        avatar_url: Optional[str] = None,
        purpose: Optional[str] = None,
        system_prompt: Optional[str] = None,
        goals: Optional[List[Dict[str, Any]]] = None,
        settings: Optional[Dict[str, Any]] = None,
        is_default: Optional[bool] = None,
        can_create_spaces: Optional[bool] = None,
    ) -> Persona:
        """Create a new persona (async)."""
        data = PersonaCreate(
            name=name, slug=slug, avatar_url=avatar_url, purpose=purpose,
            system_prompt=system_prompt, goals=goals, settings=settings,
            is_default=is_default, can_create_spaces=can_create_spaces,
        )
        response = await self._request(
            "POST", "/personas", json=data.model_dump(exclude_none=True)
        )
        return Persona.model_validate(response)

    async def list(self) -> PersonaList:
        """List all personas (async)."""
        response = await self._request("GET", "/personas")
        return PersonaList.model_validate(response)

    async def get(self, id: str) -> Persona:
        """Get a persona by ID (async)."""
        validate_id(id, "persona")
        response = await self._request("GET", f"/personas/{id}")
        return Persona.model_validate(response)

    async def get_by_slug(self, slug: str) -> Persona:
        """Get a persona by slug (async)."""
        if not slug:
            raise ValueError("persona slug cannot be empty")
        response = await self._request("GET", f"/personas/slug/{slug}")
        return Persona.model_validate(response)

    async def update(
        self,
        id: str,
        name: Optional[str] = None,
        slug: Optional[str] = None,
        avatar_url: Optional[str] = None,
        purpose: Optional[str] = None,
        system_prompt: Optional[str] = None,
        goals: Optional[List[Dict[str, Any]]] = None,
        settings: Optional[Dict[str, Any]] = None,
        is_default: Optional[bool] = None,
        can_create_spaces: Optional[bool] = None,
    ) -> Persona:
        """Update a persona (async)."""
        validate_id(id, "persona")
        data = PersonaUpdate(
            name=name, slug=slug, avatar_url=avatar_url, purpose=purpose,
            system_prompt=system_prompt, goals=goals, settings=settings,
            is_default=is_default, can_create_spaces=can_create_spaces,
        )
        response = await self._request(
            "PATCH", f"/personas/{id}", json=data.model_dump(exclude_none=True)
        )
        return Persona.model_validate(response)

    async def delete(self, id: str) -> None:
        """Delete a persona (async)."""
        validate_id(id, "persona")
        await self._request("DELETE", f"/personas/{id}")

    async def add_space(
        self,
        persona_id: str,
        space_id: str,
        role: str = "member",
        can_create_memories: bool = True,
        can_delete_memories: bool = False,
    ) -> PersonaSpace:
        """Add a space to a persona (async)."""
        validate_id(persona_id, "persona")
        data = PersonaAddSpace(
            space_id=space_id, role=role,
            can_create_memories=can_create_memories,
            can_delete_memories=can_delete_memories,
        )
        response = await self._request(
            "POST", f"/personas/{persona_id}/spaces", json=data.model_dump()
        )
        return PersonaSpace.model_validate(response)

    async def remove_space(self, persona_id: str, space_id: str) -> None:
        """Remove a space from a persona (async)."""
        validate_id(persona_id, "persona")
        validate_id(space_id, "space")
        await self._request("DELETE", f"/personas/{persona_id}/spaces/{space_id}")
