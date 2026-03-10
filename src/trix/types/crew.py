"""Crew-related types for Trix SDK."""

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel

from .base import BaseResponse


class CrewMember(BaseModel):
    """A bot member within a crew."""

    bot_id: str
    role: Optional[str] = None
    position: int = 0


class CrewCreate(BaseModel):
    """Request to create a crew."""

    name: str
    description: Optional[str] = None
    strategy: Optional[str] = None
    members: Optional[List[CrewMember]] = None
    settings: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None


class CrewUpdate(BaseModel):
    """Request to update a crew."""

    name: Optional[str] = None
    description: Optional[str] = None
    strategy: Optional[str] = None
    members: Optional[List[CrewMember]] = None
    settings: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None
    status: Optional[str] = None


class Crew(BaseResponse):
    """Crew object - a group of bots working together."""

    id: str
    account_id: str
    name: str
    slug: str
    description: Optional[str] = None
    strategy: str = "sequential"
    members: List[CrewMember] = []
    settings: Dict[str, Any] = {}
    metadata: Dict[str, Any] = {}
    status: str = "active"
    created_at: datetime
    updated_at: datetime


class CrewList(BaseResponse):
    """List of crews with pagination."""

    crews: List[Crew]
    total: int = 0
    limit: int = 20
    offset: int = 0
