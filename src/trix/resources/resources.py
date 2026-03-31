"""Resources API - Manage resources (projects, topics, etc.) and their relationships with memories."""

from typing import Any, Dict, Optional

from ..protocols import AsyncClientProtocol, SyncClientProtocol
from ..types import (
    Resource,
    ResourceCreate,
    ResourceList,
    ResourceUpdate,
)
from ..utils.security import validate_id
from .base import BaseSyncResource, BaseAsyncResource


class ResourcesResource(BaseSyncResource):
    """Synchronous resource for managing resources (projects, topics, etc.)."""

    def __init__(self, client: SyncClientProtocol) -> None:
        """Initialize resources resource with client."""
        super().__init__(client)

    def create(
        self,
        name: str,
        type: Optional[str] = None,
        description: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Resource:
        """Create a new resource.

        Args:
            name: Resource name (required)
            type: Resource type (default: "project")
            description: Optional description
            metadata: Additional metadata

        Returns:
            Created resource object

        Example:
            >>> resource = client.resources.create(
            ...     name="My Project",
            ...     type="project",
            ...     description="Project description"
            ... )
        """
        data = ResourceCreate(
            name=name,
            type=type,
            description=description,
            metadata=metadata,
        )
        response = self._request("POST", "/resources", json=data.model_dump(exclude_none=True))
        return Resource.model_validate(response)

    def list(
        self,
        type: Optional[str] = None,
        search: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
        sort: Optional[str] = None,
        order: Optional[str] = None,
    ) -> ResourceList:
        """List resources with optional filtering and pagination.

        Args:
            type: Filter by resource type
            search: Search query for name/description
            limit: Maximum number of results (default: 50)
            offset: Offset for pagination (default: 0)
            sort: Sort field (created_at, updated_at, name, type)
            order: Sort order (asc, desc)

        Returns:
            Paginated list of resources

        Example:
            >>> result = client.resources.list(
            ...     type="project",
            ...     search="my project",
            ...     sort="name",
            ...     order="asc"
            ... )
        """
        params: Dict[str, Any] = {"limit": limit, "offset": offset}
        if type:
            params["type"] = type
        if search:
            params["search"] = search
        if sort:
            params["sort"] = sort
        if order:
            params["order"] = order

        response = self._request("GET", "/resources", params=params)
        return ResourceList.model_validate(response)

    def get(self, id: str) -> Resource:
        """Get a resource by ID.

        Args:
            id: Resource ID

        Returns:
            Resource object

        Example:
            >>> resource = client.resources.get("res_123456")
        """
        validate_id(id, "resource")
        response = self._request("GET", f"/resources/{id}")
        return Resource.model_validate(response)

    def update(
        self,
        id: str,
        name: Optional[str] = None,
        type: Optional[str] = None,
        description: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Resource:
        """Update a resource.

        Args:
            id: Resource ID
            name: New name
            type: New type
            description: New description
            metadata: New metadata

        Returns:
            Updated resource object

        Example:
            >>> updated = client.resources.update(
            ...     "res_123456",
            ...     name="Updated Name",
            ...     description="New description"
            ... )
        """
        validate_id(id, "resource")
        data = ResourceUpdate(
            name=name,
            type=type,
            description=description,
            metadata=metadata,
        )
        response = self._request(
            "PATCH", f"/resources/{id}", json=data.model_dump(exclude_none=True)
        )
        return Resource.model_validate(response)

    def delete(self, id: str) -> None:
        """Delete a resource.

        Args:
            id: Resource ID

        Example:
            >>> client.resources.delete("res_123456")
        """
        validate_id(id, "resource")
        self._request("DELETE", f"/resources/{id}")

    def get_memories(
        self,
        id: str,
        limit: int = 50,
        offset: int = 0,
    ) -> Dict[str, Any]:
        """Get memories linked to a resource.

        Args:
            id: Resource ID
            limit: Maximum number of results (default: 50)
            offset: Offset for pagination (default: 0)

        Returns:
            Dictionary containing resource_id, data (list of memory links), and pagination info

        Example:
            >>> result = client.resources.get_memories("res_123456", limit=50)
            >>> for memory_link in result["data"]:
            ...     print(memory_link["id"], memory_link["relationship_type"])
        """
        validate_id(id, "resource")
        params: Dict[str, Any] = {"limit": limit, "offset": offset}
        response = self._request("GET", f"/resources/{id}/memories", params=params)
        return response


class AsyncResourcesResource(BaseAsyncResource):
    """Asynchronous resource for managing resources (projects, topics, etc.)."""

    def __init__(self, client: AsyncClientProtocol) -> None:
        """Initialize async resources resource with client."""
        super().__init__(client)

    async def create(
        self,
        name: str,
        type: Optional[str] = None,
        description: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Resource:
        """Create a new resource.

        Args:
            name: Resource name (required)
            type: Resource type (default: "project")
            description: Optional description
            metadata: Additional metadata

        Returns:
            Created resource object

        Example:
            >>> resource = await client.resources.create(
            ...     name="My Project",
            ...     type="project",
            ...     description="Project description"
            ... )
        """
        data = ResourceCreate(
            name=name,
            type=type,
            description=description,
            metadata=metadata,
        )
        response = await self._request(
            "POST", "/resources", json=data.model_dump(exclude_none=True)
        )
        return Resource.model_validate(response)

    async def list(
        self,
        type: Optional[str] = None,
        search: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
        sort: Optional[str] = None,
        order: Optional[str] = None,
    ) -> ResourceList:
        """List resources with optional filtering and pagination.

        Args:
            type: Filter by resource type
            search: Search query for name/description
            limit: Maximum number of results (default: 50)
            offset: Offset for pagination (default: 0)
            sort: Sort field (created_at, updated_at, name, type)
            order: Sort order (asc, desc)

        Returns:
            Paginated list of resources

        Example:
            >>> result = await client.resources.list(
            ...     type="project",
            ...     search="my project",
            ...     sort="name",
            ...     order="asc"
            ... )
        """
        params: Dict[str, Any] = {"limit": limit, "offset": offset}
        if type:
            params["type"] = type
        if search:
            params["search"] = search
        if sort:
            params["sort"] = sort
        if order:
            params["order"] = order

        response = await self._request("GET", "/resources", params=params)
        return ResourceList.model_validate(response)

    async def get(self, id: str) -> Resource:
        """Get a resource by ID.

        Args:
            id: Resource ID

        Returns:
            Resource object

        Example:
            >>> resource = await client.resources.get("res_123456")
        """
        validate_id(id, "resource")
        response = await self._request("GET", f"/resources/{id}")
        return Resource.model_validate(response)

    async def update(
        self,
        id: str,
        name: Optional[str] = None,
        type: Optional[str] = None,
        description: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Resource:
        """Update a resource.

        Args:
            id: Resource ID
            name: New name
            type: New type
            description: New description
            metadata: New metadata

        Returns:
            Updated resource object

        Example:
            >>> updated = await client.resources.update(
            ...     "res_123456",
            ...     name="Updated Name",
            ...     description="New description"
            ... )
        """
        validate_id(id, "resource")
        data = ResourceUpdate(
            name=name,
            type=type,
            description=description,
            metadata=metadata,
        )
        response = await self._request(
            "PATCH", f"/resources/{id}", json=data.model_dump(exclude_none=True)
        )
        return Resource.model_validate(response)

    async def delete(self, id: str) -> None:
        """Delete a resource.

        Args:
            id: Resource ID

        Example:
            >>> await client.resources.delete("res_123456")
        """
        validate_id(id, "resource")
        await self._request("DELETE", f"/resources/{id}")

    async def get_memories(
        self,
        id: str,
        limit: int = 50,
        offset: int = 0,
    ) -> Dict[str, Any]:
        """Get memories linked to a resource.

        Args:
            id: Resource ID
            limit: Maximum number of results (default: 50)
            offset: Offset for pagination (default: 0)

        Returns:
            Dictionary containing resource_id, data (list of memory links), and pagination info

        Example:
            >>> result = await client.resources.get_memories("res_123456", limit=50)
            >>> for memory_link in result["data"]:
            ...     print(memory_link["id"], memory_link["relationship_type"])
        """
        validate_id(id, "resource")
        params: Dict[str, Any] = {"limit": limit, "offset": offset}
        response = await self._request("GET", f"/resources/{id}/memories", params=params)
        return response
