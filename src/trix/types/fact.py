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


class FactCreate(BaseModel):
    """Request to create a fact."""

    subject: str
    predicate: str
    object: str
    subject_type: Optional[FactNodeType] = None
    object_type: Optional[FactNodeType] = None
    confidence: Optional[float] = 1.0
    source: Optional[FactSource] = None
    valid_from: Optional[datetime] = None
    valid_to: Optional[datetime] = None
    metadata: Optional[Dict[str, Any]] = None
    space_id: Optional[str] = None


class FactUpdate(BaseModel):
    """Request to update a fact."""

    subject: Optional[str] = None
    predicate: Optional[str] = None
    object: Optional[str] = None
    subject_type: Optional[FactNodeType] = None
    object_type: Optional[FactNodeType] = None
    confidence: Optional[float] = None
    valid_from: Optional[datetime] = None
    valid_to: Optional[datetime] = None
    metadata: Optional[Dict[str, Any]] = None


class FactList(BaseResponse):
    """List of facts with pagination."""

    data: List[Fact]
    total: int = 0
    limit: int = 10
    offset: int = 0


class ScoredFact(Fact):
    """Fact with relevance score."""

    score: float


class FactQueryResult(BaseResponse):
    """Result of fact query."""

    data: List[ScoredFact]


class ExtractedFact(BaseModel):
    """A fact extracted from memory content."""

    subject: str
    predicate: str
    object: str
    confidence: float


class FactExtractionResult(BaseResponse):
    """Result of fact extraction from a memory."""

    memory_id: str
    facts: List[ExtractedFact]
    saved: bool = False


class FactVerificationResult(BaseResponse):
    """Result of fact verification."""

    fact_id: str
    verified: bool
    confidence: float
    supporting_memories: List[str] = Field(default_factory=list)
    contradicting_memories: List[str] = Field(default_factory=list)
