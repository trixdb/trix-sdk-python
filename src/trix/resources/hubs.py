"""Hubs and conversation members resource for Trix SDK (ADR-079)."""

from typing import Any, Dict, List, Optional

from .base import BaseAsyncResource, BaseSyncResource
from ..types.hub import (
    AddConversationMemberParams,
    AddHubMemberParams,
    ConversationMember,
    ConversationMemberList,
    HubMember,
    HubMemberList,
    UpdateConversationMemberParams,
    UpdateHubMemberParams,
)
from ..utils.security import validate_id


class HubsResource(BaseSyncResource):
    """Resource for managing hub and conversation members.

    Example:
        >>> members = client.hubs.list_members("hub-123")
        >>> client.hubs.add_member("hub-123", user_id="user-456")
    """

    def list_members(self, hub_id: str) -> List[HubMember]:
        """List all members of a hub."""
        validate_id(hub_id, "hub")
        response = self._request("GET", f"/hubs/{hub_id}/members")
        result = HubMemberList.model_validate(response)
        return result.data

    def add_member(
        self,
        hub_id: str,
        user_id: str,
        role: str = "member",
        permissions: Optional[Dict[str, Any]] = None,
    ) -> HubMember:
        """Add a member to a hub."""
        validate_id(hub_id, "hub")
        data = AddHubMemberParams(user_id=user_id, role=role, permissions=permissions)
        response = self._request(
            "POST", f"/hubs/{hub_id}/members", json=data.model_dump(exclude_none=True)
        )
        return HubMember.model_validate(response)

    def update_member(
        self,
        hub_id: str,
        user_id: str,
        role: Optional[str] = None,
        permissions: Optional[Dict[str, Any]] = None,
    ) -> HubMember:
        """Update a hub member."""
        validate_id(hub_id, "hub")
        validate_id(user_id, "user")
        data = UpdateHubMemberParams(role=role, permissions=permissions)
        response = self._request(
            "PATCH",
            f"/hubs/{hub_id}/members/{user_id}",
            json=data.model_dump(exclude_none=True),
        )
        return HubMember.model_validate(response)

    def remove_member(self, hub_id: str, user_id: str) -> None:
        """Remove a member from a hub."""
        validate_id(hub_id, "hub")
        validate_id(user_id, "user")
        self._request("DELETE", f"/hubs/{hub_id}/members/{user_id}")

    def list_conversation_members(self, conversation_id: str) -> List[ConversationMember]:
        """List all members of a conversation."""
        validate_id(conversation_id, "conversation")
        response = self._request("GET", f"/conversations/{conversation_id}/members")
        result = ConversationMemberList.model_validate(response)
        return result.data

    def add_conversation_member(
        self,
        conversation_id: str,
        user_id: str,
        role: Optional[str] = None,
        permissions: Optional[Dict[str, Any]] = None,
        is_agent: Optional[bool] = None,
        autonomy: Optional[str] = None,
        trigger_mode: Optional[str] = None,
    ) -> ConversationMember:
        """Add a member to a conversation."""
        validate_id(conversation_id, "conversation")
        data = AddConversationMemberParams(
            user_id=user_id,
            role=role,
            permissions=permissions,
            is_agent=is_agent,
            autonomy=autonomy,
            trigger_mode=trigger_mode,
        )
        response = self._request(
            "POST",
            f"/conversations/{conversation_id}/members",
            json=data.model_dump(exclude_none=True),
        )
        return ConversationMember.model_validate(response)

    def update_conversation_member(
        self,
        conversation_id: str,
        user_id: str,
        role: Optional[str] = None,
        permissions: Optional[Dict[str, Any]] = None,
        autonomy: Optional[str] = None,
        trigger_mode: Optional[str] = None,
    ) -> ConversationMember:
        """Update a conversation member."""
        validate_id(conversation_id, "conversation")
        validate_id(user_id, "user")
        data = UpdateConversationMemberParams(
            role=role,
            permissions=permissions,
            autonomy=autonomy,
            trigger_mode=trigger_mode,
        )
        response = self._request(
            "PATCH",
            f"/conversations/{conversation_id}/members/{user_id}",
            json=data.model_dump(exclude_none=True),
        )
        return ConversationMember.model_validate(response)

    def remove_conversation_member(self, conversation_id: str, user_id: str) -> None:
        """Remove a member from a conversation."""
        validate_id(conversation_id, "conversation")
        validate_id(user_id, "user")
        self._request("DELETE", f"/conversations/{conversation_id}/members/{user_id}")


class AsyncHubsResource(BaseAsyncResource):
    """Async resource for managing hub and conversation members."""

    async def list_members(self, hub_id: str) -> List[HubMember]:
        """List all members of a hub (async)."""
        validate_id(hub_id, "hub")
        response = await self._request("GET", f"/hubs/{hub_id}/members")
        result = HubMemberList.model_validate(response)
        return result.data

    async def add_member(
        self,
        hub_id: str,
        user_id: str,
        role: str = "member",
        permissions: Optional[Dict[str, Any]] = None,
    ) -> HubMember:
        """Add a member to a hub (async)."""
        validate_id(hub_id, "hub")
        data = AddHubMemberParams(user_id=user_id, role=role, permissions=permissions)
        response = await self._request(
            "POST", f"/hubs/{hub_id}/members", json=data.model_dump(exclude_none=True)
        )
        return HubMember.model_validate(response)

    async def update_member(
        self,
        hub_id: str,
        user_id: str,
        role: Optional[str] = None,
        permissions: Optional[Dict[str, Any]] = None,
    ) -> HubMember:
        """Update a hub member (async)."""
        validate_id(hub_id, "hub")
        validate_id(user_id, "user")
        data = UpdateHubMemberParams(role=role, permissions=permissions)
        response = await self._request(
            "PATCH",
            f"/hubs/{hub_id}/members/{user_id}",
            json=data.model_dump(exclude_none=True),
        )
        return HubMember.model_validate(response)

    async def remove_member(self, hub_id: str, user_id: str) -> None:
        """Remove a member from a hub (async)."""
        validate_id(hub_id, "hub")
        validate_id(user_id, "user")
        await self._request("DELETE", f"/hubs/{hub_id}/members/{user_id}")

    async def list_conversation_members(self, conversation_id: str) -> List[ConversationMember]:
        """List all members of a conversation (async)."""
        validate_id(conversation_id, "conversation")
        response = await self._request("GET", f"/conversations/{conversation_id}/members")
        result = ConversationMemberList.model_validate(response)
        return result.data

    async def add_conversation_member(
        self,
        conversation_id: str,
        user_id: str,
        role: Optional[str] = None,
        permissions: Optional[Dict[str, Any]] = None,
        is_agent: Optional[bool] = None,
        autonomy: Optional[str] = None,
        trigger_mode: Optional[str] = None,
    ) -> ConversationMember:
        """Add a member to a conversation (async)."""
        validate_id(conversation_id, "conversation")
        data = AddConversationMemberParams(
            user_id=user_id,
            role=role,
            permissions=permissions,
            is_agent=is_agent,
            autonomy=autonomy,
            trigger_mode=trigger_mode,
        )
        response = await self._request(
            "POST",
            f"/conversations/{conversation_id}/members",
            json=data.model_dump(exclude_none=True),
        )
        return ConversationMember.model_validate(response)

    async def update_conversation_member(
        self,
        conversation_id: str,
        user_id: str,
        role: Optional[str] = None,
        permissions: Optional[Dict[str, Any]] = None,
        autonomy: Optional[str] = None,
        trigger_mode: Optional[str] = None,
    ) -> ConversationMember:
        """Update a conversation member (async)."""
        validate_id(conversation_id, "conversation")
        validate_id(user_id, "user")
        data = UpdateConversationMemberParams(
            role=role,
            permissions=permissions,
            autonomy=autonomy,
            trigger_mode=trigger_mode,
        )
        response = await self._request(
            "PATCH",
            f"/conversations/{conversation_id}/members/{user_id}",
            json=data.model_dump(exclude_none=True),
        )
        return ConversationMember.model_validate(response)

    async def remove_conversation_member(self, conversation_id: str, user_id: str) -> None:
        """Remove a member from a conversation (async)."""
        validate_id(conversation_id, "conversation")
        validate_id(user_id, "user")
        await self._request("DELETE", f"/conversations/{conversation_id}/members/{user_id}")
