"""Skill-related types for Trix SDK."""

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel

from .base import BaseResponse


class Skill(BaseResponse):
    """A reusable instruction package."""

    id: str
    name: str
    slug: Optional[str] = None
    description: Optional[str] = None
    content: Optional[str] = None
    version: Optional[str] = None
    status: Optional[str] = None
    author_id: Optional[str] = None
    is_published: Optional[bool] = None
    install_count: Optional[int] = None
    tags: Optional[List[str]] = None
    metadata: Optional[Dict[str, Any]] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class SkillCreate(BaseModel):
    """Request to create a skill."""

    name: str
    description: Optional[str] = None
    content: Optional[str] = None
    tags: Optional[List[str]] = None
    metadata: Optional[Dict[str, Any]] = None


class SkillUpdate(BaseModel):
    """Request to update a skill."""

    name: Optional[str] = None
    description: Optional[str] = None
    content: Optional[str] = None
    tags: Optional[List[str]] = None
    metadata: Optional[Dict[str, Any]] = None


class SkillList(BaseResponse):
    """List of skills."""

    skills: List[Skill]


class BotSkillAttachment(BaseResponse):
    """A bot-skill attachment record."""

    skill_id: str
    bot_id: str
    enabled: Optional[bool] = None
    priority: Optional[int] = None
    config: Optional[Dict[str, Any]] = None
    created_at: Optional[datetime] = None
