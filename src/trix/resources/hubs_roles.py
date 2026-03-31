"""Hub role management and conversation role overrides (ADR-080 Phase 6)."""

from typing import Any, Dict, List, Optional

from .base import BaseAsyncResource, BaseSyncResource
from ..types.hub import (
    ConvRoleOverride,
    ConvRoleOverrideList,
    CreateRoleParams,
    HubCustomRole,
    HubCustomRoleList,
    UpdateRoleParams,
)
from ..utils.security import validate_id


class HubRolesMixin:
    """Shared docstrings and validation for hub role operations."""


class HubRolesResource(BaseSyncResource):
    """Sync resource for hub roles and conversation role overrides.

    Example:
        >>> roles = client.hub_roles.list_roles("hub-123")
        >>> client.hub_roles.create_role("hub-123", name="Moderator")
    """

    def list_roles(self, hub_id: str) -> List[HubCustomRole]:
        """List all custom roles for a hub."""
        validate_id(hub_id, "hub")
        response = self._request("GET", f"/hubs/{hub_id}/roles")
        result = HubCustomRoleList.model_validate(response)
        return result.data

    def create_role(
        self,
        hub_id: str,
        *,
        name: str,
        color: Optional[str] = None,
        icon: Optional[str] = None,
        position: Optional[int] = None,
        permissions: Optional[Dict[str, str]] = None,
    ) -> HubCustomRole:
        """Create a custom role for a hub."""
        validate_id(hub_id, "hub")
        data = CreateRoleParams(
            name=name,
            color=color,
            icon=icon,
            position=position,
            permissions=permissions,
        )
        response = self._request(
            "POST", f"/hubs/{hub_id}/roles", json=data.model_dump(exclude_none=True)
        )
        return HubCustomRole.model_validate(response)

    def update_role(
        self,
        hub_id: str,
        role_id: str,
        **kwargs: Any,
    ) -> HubCustomRole:
        """Update a custom role's properties."""
        validate_id(hub_id, "hub")
        validate_id(role_id, "role")
        data = UpdateRoleParams(**kwargs)
        response = self._request(
            "PATCH",
            f"/hubs/{hub_id}/roles/{role_id}",
            json=data.model_dump(exclude_none=True),
        )
        return HubCustomRole.model_validate(response)

    def delete_role(self, hub_id: str, role_id: str) -> None:
        """Delete a custom role from a hub."""
        validate_id(hub_id, "hub")
        validate_id(role_id, "role")
        self._request("DELETE", f"/hubs/{hub_id}/roles/{role_id}")

    def reorder_roles(self, hub_id: str, role_ids: List[str]) -> None:
        """Reorder roles for a hub."""
        validate_id(hub_id, "hub")
        self._request("PUT", f"/hubs/{hub_id}/roles/reorder", json={"role_ids": role_ids})

    def assign_role(self, hub_id: str, role_id: str, user_id: str) -> None:
        """Assign a role to a hub member."""
        validate_id(hub_id, "hub")
        validate_id(role_id, "role")
        self._request("POST", f"/hubs/{hub_id}/roles/{role_id}/assign", json={"user_id": user_id})

    def remove_role(self, hub_id: str, role_id: str, user_id: str) -> None:
        """Remove a role from a hub member."""
        validate_id(hub_id, "hub")
        validate_id(role_id, "role")
        self._request("DELETE", f"/hubs/{hub_id}/roles/{role_id}/members/{user_id}")

    def list_role_overrides(self, conversation_id: str) -> List[ConvRoleOverride]:
        """List per-role permission overrides for a conversation."""
        validate_id(conversation_id, "conversation")
        response = self._request("GET", f"/conversations/{conversation_id}/role-overrides")
        result = ConvRoleOverrideList.model_validate(response)
        return result.data

    def upsert_role_override(
        self, conversation_id: str, role_id: str, permissions: Dict[str, str]
    ) -> ConvRoleOverride:
        """Set per-role permission overrides for a conversation."""
        validate_id(conversation_id, "conversation")
        validate_id(role_id, "role")
        response = self._request(
            "PUT",
            f"/conversations/{conversation_id}/role-overrides/{role_id}",
            json={"permissions": permissions},
        )
        return ConvRoleOverride.model_validate(response)

    def delete_role_override(self, conversation_id: str, role_id: str) -> None:
        """Delete a per-role permission override for a conversation."""
        validate_id(conversation_id, "conversation")
        validate_id(role_id, "role")
        self._request("DELETE", f"/conversations/{conversation_id}/role-overrides/{role_id}")


class AsyncHubRolesResource(BaseAsyncResource):
    """Async resource for hub roles and conversation role overrides."""

    async def list_roles(self, hub_id: str) -> List[HubCustomRole]:
        """List all custom roles for a hub (async)."""
        validate_id(hub_id, "hub")
        response = await self._request("GET", f"/hubs/{hub_id}/roles")
        result = HubCustomRoleList.model_validate(response)
        return result.data

    async def create_role(
        self,
        hub_id: str,
        *,
        name: str,
        color: Optional[str] = None,
        icon: Optional[str] = None,
        position: Optional[int] = None,
        permissions: Optional[Dict[str, str]] = None,
    ) -> HubCustomRole:
        """Create a custom role for a hub (async)."""
        validate_id(hub_id, "hub")
        data = CreateRoleParams(
            name=name,
            color=color,
            icon=icon,
            position=position,
            permissions=permissions,
        )
        response = await self._request(
            "POST", f"/hubs/{hub_id}/roles", json=data.model_dump(exclude_none=True)
        )
        return HubCustomRole.model_validate(response)

    async def update_role(
        self,
        hub_id: str,
        role_id: str,
        **kwargs: Any,
    ) -> HubCustomRole:
        """Update a custom role's properties (async)."""
        validate_id(hub_id, "hub")
        validate_id(role_id, "role")
        data = UpdateRoleParams(**kwargs)
        response = await self._request(
            "PATCH",
            f"/hubs/{hub_id}/roles/{role_id}",
            json=data.model_dump(exclude_none=True),
        )
        return HubCustomRole.model_validate(response)

    async def delete_role(self, hub_id: str, role_id: str) -> None:
        """Delete a custom role from a hub (async)."""
        validate_id(hub_id, "hub")
        validate_id(role_id, "role")
        await self._request("DELETE", f"/hubs/{hub_id}/roles/{role_id}")

    async def reorder_roles(self, hub_id: str, role_ids: List[str]) -> None:
        """Reorder roles for a hub (async)."""
        validate_id(hub_id, "hub")
        await self._request("PUT", f"/hubs/{hub_id}/roles/reorder", json={"role_ids": role_ids})

    async def assign_role(self, hub_id: str, role_id: str, user_id: str) -> None:
        """Assign a role to a hub member (async)."""
        validate_id(hub_id, "hub")
        validate_id(role_id, "role")
        await self._request(
            "POST", f"/hubs/{hub_id}/roles/{role_id}/assign", json={"user_id": user_id}
        )

    async def remove_role(self, hub_id: str, role_id: str, user_id: str) -> None:
        """Remove a role from a hub member (async)."""
        validate_id(hub_id, "hub")
        validate_id(role_id, "role")
        await self._request("DELETE", f"/hubs/{hub_id}/roles/{role_id}/members/{user_id}")

    async def list_role_overrides(self, conversation_id: str) -> List[ConvRoleOverride]:
        """List per-role permission overrides for a conversation (async)."""
        validate_id(conversation_id, "conversation")
        response = await self._request("GET", f"/conversations/{conversation_id}/role-overrides")
        result = ConvRoleOverrideList.model_validate(response)
        return result.data

    async def upsert_role_override(
        self, conversation_id: str, role_id: str, permissions: Dict[str, str]
    ) -> ConvRoleOverride:
        """Set per-role permission overrides for a conversation (async)."""
        validate_id(conversation_id, "conversation")
        validate_id(role_id, "role")
        response = await self._request(
            "PUT",
            f"/conversations/{conversation_id}/role-overrides/{role_id}",
            json={"permissions": permissions},
        )
        return ConvRoleOverride.model_validate(response)

    async def delete_role_override(self, conversation_id: str, role_id: str) -> None:
        """Delete a per-role permission override for a conversation (async)."""
        validate_id(conversation_id, "conversation")
        validate_id(role_id, "role")
        await self._request("DELETE", f"/conversations/{conversation_id}/role-overrides/{role_id}")
