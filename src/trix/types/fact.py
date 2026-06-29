"""Fact-related types for Trix SDK."""

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from .base import BaseResponse
from .enums import FactNodeType, FactSourceMethod


class FactSource(BaseModel):
    """Source attribution for a fact."""

    memory_id: Optional[str] = None
    session_id: Optional[str] = None
    method: Optional[FactSourceMethod] = None


class Fact(BaseResponse):
    """Fact object - represents a knowledge graph triple (Subject-Predicate-Object)."""

    id: str
    subject: str
    predicate: str
    object: str
    subject_type: Optional[FactNodeType] = None
    object_type: Optional[FactNodeType] = None
    confidence: float
    source: Optional[FactSource] = None
    valid_from: Optional[datetime] = None
    valid_to: Optional[datetime] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
    space_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class FactList(BaseResponse):
    """List of facts with pagination."""

    data: List[Fact]
    total: int = 0
    limit: int = 10
    offset: int = 0


class MemoryFactCreate(BaseModel):
    """Request body to attach a fact to a memory (``POST /memories/:id/facts``).

    The memory-scoped fact endpoint takes free-form ``content`` plus an
    ``importance`` score (1-10), not the Subject-Predicate-Object triple shape.
    """

    content: str
    importance: int
    category: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class MemoryFactsResult(BaseResponse):
    """Facts attached to a single memory (``GET /memories/:id/facts``)."""

    memory_id: str
    facts: List[Fact]
    total: int = 0
