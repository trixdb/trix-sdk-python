"""Resource linking operations mixin for memories.

Provides operations to link and unlink resources to memories.
"""

from typing import Any, Dict, Optional

from ...utils.security import validate_id


class ResourceLinksMixin:
    """Mixin providing resource linking operations for sync memories resource."""

    _client: Any  # Type hint for the client

    def link_resource(
        self,
        id: str,
        resource_id: str,
        relationship_type: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Link a resource to a memory."""
        validate_id(id, "memory")
        validate_id(resource_id, "resource")

        body: Dict[str, Any] = {"resource_id": resource_id}
        if relationship_type:
            body["relationship_type"] = relationship_type

        return self._client._request("POST", f"/memories/{id}/resources", json=body)

    def get_resources(self, id: str) -> Dict[str, Any]:
        """Get resources linked to a memory."""
        validate_id(id, "memory")
        return self._client._request("GET", f"/memories/{id}/resources")

    def unlink_resource(self, id: str, resource_id: str) -> Dict[str, Any]:
        """Unlink a resource from a memory."""
        validate_id(id, "memory")
        validate_id(resource_id, "resource")
        return self._client._request("DELETE", f"/memories/{id}/resources/{resource_id}")


class AsyncResourceLinksMixin:
    """Mixin providing resource linking operations for async memories resource."""

    _client: Any  # Type hint for the client

    async def link_resource(
        self,
        id: str,
        resource_id: str,
        relationship_type: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Link a resource to a memory (async)."""
        validate_id(id, "memory")
        validate_id(resource_id, "resource")

        body: Dict[str, Any] = {"resource_id": resource_id}
        if relationship_type:
            body["relationship_type"] = relationship_type

        return await self._client._request("POST", f"/memories/{id}/resources", json=body)

    async def get_resources(self, id: str) -> Dict[str, Any]:
        """Get resources linked to a memory (async)."""
        validate_id(id, "memory")
        return await self._client._request("GET", f"/memories/{id}/resources")

    async def unlink_resource(self, id: str, resource_id: str) -> Dict[str, Any]:
        """Unlink a resource from a memory (async)."""
        validate_id(id, "memory")
        validate_id(resource_id, "resource")
        return await self._client._request("DELETE", f"/memories/{id}/resources/{resource_id}")
