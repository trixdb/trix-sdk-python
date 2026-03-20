"""Invite-related types for Trix SDK."""

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel

from .base import BaseResponse


class Invite(BaseResponse):
    """An account invitation."""

    id: str
    email: str
    role: str
    token: Optional[str] = None
    expires_at: datetime
    accepted_at: Optional[datetime] = None
    created_at: datetime
    invited_by: str
    invited_by_email: Optional[str] = None
    invited_by_name: Optional[str] = None


class InviteCreate(BaseModel):
    """Request to create an invitation."""

    email: str
    role: str
    expires_in_days: Optional[int] = None


class InviteList(BaseResponse):
    """List of invitations with pagination."""

    invites: List[Invite]
    pagination: Optional[Dict[str, Any]] = None


class InviteAccept(BaseModel):
    """Request to accept an invitation."""

    name: Optional[str] = None
    password: Optional[str] = None


class InviteAcceptResult(BaseResponse):
    """Result of accepting an invitation."""

    message: str
    user: Dict[str, Any]
    account: Dict[str, Any]
    token: Optional[str] = None


class InviteRevokeResult(BaseResponse):
    """Result of revoking an invitation."""

    message: str
    id: str


class InviteCreateResult(BaseResponse):
    """Result of creating an invitation."""

    message: str
    invite: Invite
