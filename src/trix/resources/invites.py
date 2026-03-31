"""Invites resource for Trix SDK."""

from typing import Any, Dict, Optional
from urllib.parse import quote

from .base import BaseAsyncResource, BaseSyncResource
from ..types.invite import (
    InviteAccept,
    InviteAcceptResult,
    InviteCreate,
    InviteCreateResult,
    InviteList,
    InviteRevokeResult,
)
from ..utils.security import validate_id


class InvitesResource(BaseSyncResource):
    """Resource for managing account invitations.

    Example:
        >>> result = client.invites.create(
        ...     email="user@example.com",
        ...     role="member",
        ... )
        >>> print(result.invite.token)
    """

    def create(
        self,
        email: str,
        role: str,
        expires_in_days: Optional[int] = None,
    ) -> InviteCreateResult:
        """Create a new invitation."""
        data = InviteCreate(
            email=email, role=role, expires_in_days=expires_in_days,
        )
        response = self._request(
            "POST", "/accounts/invites", json=data.model_dump(exclude_none=True)
        )
        return InviteCreateResult.model_validate(response)

    def list(
        self,
        status: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> InviteList:
        """List invitations for the current account."""
        params: Dict[str, Any] = {"limit": limit, "offset": offset}
        if status is not None:
            params["status"] = status
        response = self._request("GET", "/accounts/invites", params=params)
        return InviteList.model_validate(response)

    def revoke(self, invite_id: str) -> InviteRevokeResult:
        """Revoke a pending invitation."""
        validate_id(invite_id, "invite")
        response = self._request(
            "DELETE", f"/accounts/invites/{invite_id}"
        )
        return InviteRevokeResult.model_validate(response)

    def accept(
        self,
        token: str,
        name: Optional[str] = None,
        password: Optional[str] = None,
    ) -> InviteAcceptResult:
        """Accept an invitation using its token."""
        data = InviteAccept(name=name, password=password)
        body = data.model_dump(exclude_none=True)
        response = self._request(
            "POST",
            f"/accounts/invites/{quote(token, safe='')}/accept",
            json=body if body else None,
        )
        return InviteAcceptResult.model_validate(response)


class AsyncInvitesResource(BaseAsyncResource):
    """Async resource for managing account invitations."""

    async def create(
        self,
        email: str,
        role: str,
        expires_in_days: Optional[int] = None,
    ) -> InviteCreateResult:
        """Create a new invitation (async)."""
        data = InviteCreate(
            email=email, role=role, expires_in_days=expires_in_days,
        )
        response = await self._request(
            "POST", "/accounts/invites", json=data.model_dump(exclude_none=True)
        )
        return InviteCreateResult.model_validate(response)

    async def list(
        self,
        status: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> InviteList:
        """List invitations for the current account (async)."""
        params: Dict[str, Any] = {"limit": limit, "offset": offset}
        if status is not None:
            params["status"] = status
        response = await self._request("GET", "/accounts/invites", params=params)
        return InviteList.model_validate(response)

    async def revoke(self, invite_id: str) -> InviteRevokeResult:
        """Revoke a pending invitation (async)."""
        validate_id(invite_id, "invite")
        response = await self._request(
            "DELETE", f"/accounts/invites/{invite_id}"
        )
        return InviteRevokeResult.model_validate(response)

    async def accept(
        self,
        token: str,
        name: Optional[str] = None,
        password: Optional[str] = None,
    ) -> InviteAcceptResult:
        """Accept an invitation using its token (async)."""
        data = InviteAccept(name=name, password=password)
        body = data.model_dump(exclude_none=True)
        response = await self._request(
            "POST",
            f"/accounts/invites/{quote(token, safe='')}/accept",
            json=body if body else None,
        )
        return InviteAcceptResult.model_validate(response)
