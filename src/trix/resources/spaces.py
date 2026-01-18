"""Spaces resource for Trix SDK."""

from typing import Optional

from .base import BaseAsyncResource, BaseSyncResource
from ..types import Space, SpaceCreate, SpaceList, SpaceUpdate
from ..utils.security import validate_id


class SpacesResource(BaseSyncResource):
    """Resource for managing spaces.

    Spaces are containers for organizing memories into logical groups.

    Example:
        >>> # Create a space
        >>> space = client.spaces.create(
        ...     name="Personal",
        ...     description="Personal memories"
        ... )
        >>>
        >>> # List all spaces
        >>> spaces = client.spaces.list()
        >>>
        >>> # Get a specific space
        >>> space = client.spaces.get("space_123")
    """

    def create(
        self, name: str, slug: Optional[str] = None, description: Optional[str] = None
    ) -> Space:
        """Create a new space.

        Args:
            name: Space name
            slug: Optional URL-friendly identifier (auto-generated if not provided)
            description: Optional description

        Returns:
            Created space object

        Example:
            >>> space = client.spaces.create(
            ...     name="Personal",
            ...     slug="personal",
            ...     description="Personal memories"
            ... )
        """
        data = SpaceCreate(name=name, slug=slug, description=description)
        response = self._request("POST", "/spaces", json=data.model_dump(exclude_none=True))
        return Space.model_validate(response)

    def list(self) -> SpaceList:
        """List all spaces.

        Returns:
            List of spaces

        Example:
            >>> spaces = client.spaces.list()
        """
        response = self._request("GET", "/spaces")
        return SpaceList.model_validate(response)

    def get(self, id: str) -> Space:
        """Get a space by ID.

        Args:
            id: Space ID

        Returns:
            Space object

        Raises:
            ValidationError: If ID format is invalid
            NotFoundError: If space doesn't exist

        Example:
            >>> space = client.spaces.get("space_123")
        """
        validate_id(id, "space")
        response = self._request("GET", f"/spaces/{id}")
        return Space.model_validate(response)

    def get_by_slug(self, slug: str) -> Space:
        """Get a space by its slug.

        Args:
            slug: Space slug (URL-friendly identifier)

        Returns:
            Space object

        Raises:
            ValueError: If slug is empty
            NotFoundError: If space doesn't exist

        Example:
            >>> space = client.spaces.get_by_slug("my-project")
        """
        if not slug:
            raise ValueError("Slug must be a non-empty string")
        response = self._request("GET", f"/spaces/{slug}")
        return Space.model_validate(response)

    def update(
        self,
        id: str,
        name: Optional[str] = None,
        slug: Optional[str] = None,
        description: Optional[str] = None,
    ) -> Space:
        """Update a space.

        Args:
            id: Space ID
            name: New name
            slug: New slug (URL-friendly identifier)
            description: New description

        Returns:
            Updated space object

        Raises:
            ValidationError: If ID format is invalid
            NotFoundError: If space doesn't exist

        Example:
            >>> space = client.spaces.update(
            ...     "space_123",
            ...     name="Updated Name",
            ...     slug="updated-slug"
            ... )
        """
        validate_id(id, "space")
        data = SpaceUpdate(name=name, slug=slug, description=description)
        response = self._request("PATCH", f"/spaces/{id}", json=data.model_dump(exclude_none=True))
        return Space.model_validate(response)

    def delete(self, id: str) -> None:
        """Delete a space.

        Args:
            id: Space ID

        Raises:
            ValidationError: If ID format is invalid
            NotFoundError: If space doesn't exist

        Example:
            >>> client.spaces.delete("space_123")
        """
        validate_id(id, "space")
        self._request("DELETE", f"/spaces/{id}")


class AsyncSpacesResource(BaseAsyncResource):
    """Async resource for managing spaces.

    Spaces are containers for organizing memories into logical groups.

    Example:
        >>> # Create a space
        >>> space = await client.spaces.create(
        ...     name="Personal",
        ...     description="Personal memories"
        ... )
    """

    async def create(
        self, name: str, slug: Optional[str] = None, description: Optional[str] = None
    ) -> Space:
        """Create a new space (async).

        Args:
            name: Space name
            slug: Optional URL-friendly identifier (auto-generated if not provided)
            description: Optional description

        Returns:
            Created space object
        """
        data = SpaceCreate(name=name, slug=slug, description=description)
        response = await self._request("POST", "/spaces", json=data.model_dump(exclude_none=True))
        return Space.model_validate(response)

    async def list(self) -> SpaceList:
        """List all spaces (async).

        Returns:
            List of spaces
        """
        response = await self._request("GET", "/spaces")
        return SpaceList.model_validate(response)

    async def get(self, id: str) -> Space:
        """Get a space by ID (async).

        Args:
            id: Space ID

        Returns:
            Space object
        """
        validate_id(id, "space")
        response = await self._request("GET", f"/spaces/{id}")
        return Space.model_validate(response)

    async def get_by_slug(self, slug: str) -> Space:
        """Get a space by its slug (async).

        Args:
            slug: Space slug (URL-friendly identifier)

        Returns:
            Space object

        Raises:
            ValueError: If slug is empty
            NotFoundError: If space doesn't exist
        """
        if not slug:
            raise ValueError("Slug must be a non-empty string")
        response = await self._request("GET", f"/spaces/{slug}")
        return Space.model_validate(response)

    async def update(
        self,
        id: str,
        name: Optional[str] = None,
        slug: Optional[str] = None,
        description: Optional[str] = None,
    ) -> Space:
        """Update a space (async).

        Args:
            id: Space ID
            name: New name
            slug: New slug (URL-friendly identifier)
            description: New description

        Returns:
            Updated space object
        """
        validate_id(id, "space")
        data = SpaceUpdate(name=name, slug=slug, description=description)
        response = await self._request(
            "PATCH", f"/spaces/{id}", json=data.model_dump(exclude_none=True)
        )
        return Space.model_validate(response)

    async def delete(self, id: str) -> None:
        """Delete a space (async).

        Args:
            id: Space ID
        """
        validate_id(id, "space")
        await self._request("DELETE", f"/spaces/{id}")
