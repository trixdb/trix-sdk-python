"""Persona-related types for Trix SDK."""

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel

from .base import BaseResponse


class PersonaGoal(BaseModel):
    """A persona goal."""

    text: str
    status: str = "pending"
    priority: int = 5


class PersonaSpace(BaseModel):
    """Persona space membership."""

    space_id: str
    role: str = "member"
    can_create_memories: bool = True
    can_delete_memories: bool = False
    granted_at: Optional[datetime] = None


class Persona(BaseResponse):
    """Named identity with purpose and multi-space access."""

    id: str
    name: str
    slug: str
    avatar_url: Optional[str] = None
    purpose: Optional[str] = None
    system_prompt: Optional[str] = None
    goals: List[PersonaGoal] = []
    settings: Dict[str, Any] = {}
    metadata: Dict[str, Any] = {}
    is_default: bool = False
    can_create_spaces: bool = False
    spaces: Optional[List[PersonaSpace]] = None
    space_count: Optional[int] = None
    created_at: datetime
    updated_at: datetime


class PersonaCreate(BaseModel):
    """Request to create a persona."""

    name: str
    slug: Optional[str] = None
    avatar_url: Optional[str] = None
    purpose: Optional[str] = None
    system_prompt: Optional[str] = None
    goals: Optional[List[PersonaGoal]] = None
    settings: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None
    is_default: Optional[bool] = None
    can_create_spaces: Optional[bool] = None


class PersonaUpdate(BaseModel):
    """Request to update a persona."""

    name: Optional[str] = None
    slug: Optional[str] = None
    avatar_url: Optional[str] = None
    purpose: Optional[str] = None
    system_prompt: Optional[str] = None
    goals: Optional[List[PersonaGoal]] = None
    settings: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None
    is_default: Optional[bool] = None
    can_create_spaces: Optional[bool] = None


class PersonaAddSpace(BaseModel):
    """Request to add a space to a persona."""

    space_id: str
    role: str = "member"
    can_create_memories: bool = True
    can_delete_memories: bool = False


class PersonaList(BaseResponse):
    """List of personas."""

    data: List[Persona]
