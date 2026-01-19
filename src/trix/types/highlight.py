"""Highlight-related types for Trix SDK."""

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from .base import BaseResponse
from .enums import ExtractionType


class Highlight(BaseResponse):
    """Highlighted text within a memory."""

    id: str
    memory_id: str
    text: str
    note: Optional[str] = None
    importance: Optional[int] = None
    tags: List[str] = Field(default_factory=list)
    color: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class HighlightCreate(BaseModel):
    """Request to create a highlight."""

    text: str
    note: Optional[str] = None
    importance: Optional[int] = None
    tags: Optional[List[str]] = None
    color: Optional[str] = None


class HighlightUpdate(BaseModel):
    """Request to update a highlight."""

    text: Optional[str] = None
    note: Optional[str] = None
    importance: Optional[int] = None
    tags: Optional[List[str]] = None
    color: Optional[str] = None


class HighlightList(BaseResponse):
    """List of highlights."""

    data: List[Highlight]


class ExtractedHighlights(BaseResponse):
    """Automatically extracted highlights."""

    memory_id: str
    extraction_type: ExtractionType
    highlights: List[Dict[str, Any]]


class HighlightWithScore(Highlight):
    """Highlight with search score."""

    score: float


class HighlightSearchResult(BaseResponse):
    """Highlight search result."""

    highlights: List[HighlightWithScore]


class HighlightTypeInfo(BaseModel):
    """Highlight type info."""

    name: str
    count: int
    color: Optional[str] = None


class HighlightTypesResult(BaseResponse):
    """Result of getting highlight types."""

    types: List[HighlightTypeInfo]


class HighlightLinkResult(BaseResponse):
    """Result of linking a highlight to a memory."""

    highlight_id: str
    memory_id: str
    linked: bool
