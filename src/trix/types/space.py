"""Space-related types for Trix SDK."""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

from .base import BaseResponse


class Space(BaseResponse):
    """Organizational space for memories."""

    id: str
    name: str
    slug: str
    description: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class SpaceCreate(BaseModel):
    """Request to create a space."""

    name: str
    slug: Optional[str] = None
    description: Optional[str] = None


class SpaceUpdate(BaseModel):
    """Request to update a space."""

    name: Optional[str] = None
    slug: Optional[str] = None
    description: Optional[str] = None


class SpaceList(BaseResponse):
    """List of spaces."""

    data: List[Space]
