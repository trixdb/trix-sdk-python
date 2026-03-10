"""Hub and conversation member types for Trix SDK (ADR-079)."""

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel

from .base import BaseResponse


class HubMember(BaseResponse):
    """A hub member."""

    id: str
    hub_id: str
    user_id: str
    role: str
    permissions: Optional[Dict[str, Any]] = None
    name: Optional[str] = None
    email: Optional[str] = None
    avatar: Optional[str] = None
    status: Optional[str] = None
    joined_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class ConversationMember(BaseResponse):
    """A conversation member."""

    id: str
    conversation_id: str
    user_id: str
    role: str
    permissions: Optional[Dict[str, Any]] = None
    is_agent: bool = False
    autonomy: Optional[str] = None
    trigger_mode: Optional[str] = None
    name: Optional[str] = None
    email: Optional[str] = None
    avatar: Optional[str] = None
    status: Optional[str] = None
    joined_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class AddHubMemberParams(BaseModel):
    """Request to add a member to a hub."""

    user_id: str
    role: str = "member"
    permissions: Optional[Dict[str, Any]] = None


class UpdateHubMemberParams(BaseModel):
    """Request to update a hub member."""

    role: Optional[str] = None
    permissions: Optional[Dict[str, Any]] = None


class AddConversationMemberParams(BaseModel):
    """Request to add a member to a conversation."""

    user_id: str
    role: Optional[str] = None
    permissions: Optional[Dict[str, Any]] = None
    is_agent: Optional[bool] = None
    autonomy: Optional[str] = None
    trigger_mode: Optional[str] = None


class UpdateConversationMemberParams(BaseModel):
    """Request to update a conversation member."""

    role: Optional[str] = None
    permissions: Optional[Dict[str, Any]] = None
    autonomy: Optional[str] = None
    trigger_mode: Optional[str] = None


class HubMemberList(BaseResponse):
    """List of hub members."""

    data: List[HubMember]


class ConversationMemberList(BaseResponse):
    """List of conversation members."""

    data: List[ConversationMember]


class HubCustomRole(BaseResponse):
    """A custom hub role."""

    id: str
    hub_id: str
    name: str
    color: Optional[str] = None
    icon: Optional[str] = None
    position: int = 0
    permissions: Dict[str, str] = {}
    is_default: bool = False


class CreateRoleParams(BaseModel):
    """Request to create a custom role."""

    name: str
    color: Optional[str] = None
    icon: Optional[str] = None
    position: Optional[int] = None
    permissions: Optional[Dict[str, str]] = None


class UpdateRoleParams(BaseModel):
    """Request to update a custom role."""

    name: Optional[str] = None
    color: Optional[str] = None
    icon: Optional[str] = None
    position: Optional[int] = None
    permissions: Optional[Dict[str, str]] = None


class HubCustomRoleList(BaseResponse):
    """List of custom hub roles."""

    data: List[HubCustomRole]


class ConvRoleOverride(BaseResponse):
    """A conversation-level role permission override."""

    id: str
    conversation_id: str
    role_id: str
    permissions: Dict[str, str] = {}


class ConvRoleOverrideList(BaseResponse):
    """List of conversation role overrides."""

    data: List[ConvRoleOverride]
