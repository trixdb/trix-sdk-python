"""Entity-related types for Trix SDK."""

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from .base import BaseResponse
from .fact import Fact


class Entity(BaseResponse):
    """Entity object - represents a named entity."""

    id: str
    name: str
    type: str
    aliases: List[str] = Field(default_factory=list)
    description: Optional[str] = None
    properties: Dict[str, Any] = Field(default_factory=dict)
    memory_ids: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    space_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class EntityCreate(BaseModel):
    """Request to create an entity."""

    name: str
    type: str
    aliases: Optional[List[str]] = None
    description: Optional[str] = None
    properties: Optional[Dict[str, Any]] = None
    memory_ids: Optional[List[str]] = None
    metadata: Optional[Dict[str, Any]] = None
    space_id: Optional[str] = None


class EntityUpdate(BaseModel):
    """Request to update an entity."""

    name: Optional[str] = None
    type: Optional[str] = None
    aliases: Optional[List[str]] = None
    description: Optional[str] = None
    properties: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None


class EntityList(BaseResponse):
    """List of entities with pagination."""

    data: List[Entity]
    total: int = 0
    limit: int = 10
    offset: int = 0


class ScoredEntity(Entity):
    """Entity with relevance score."""

    score: float


class EntitySearchResult(BaseResponse):
    """Result of entity search."""

    data: List[ScoredEntity]


class EntityResolutionResult(BaseResponse):
    """Result of entity resolution."""

    text: str
    entity: Optional[Entity] = None
    confidence: float
    alternatives: List[Dict[str, Any]] = Field(default_factory=list)


class EntityMergeResult(BaseResponse):
    """Result of entity merge."""

    merged_entity: Entity
    deleted_id: str


class EntityMemoryLinkResult(BaseResponse):
    """Result of entity-memory link."""

    entity_id: str
    memory_id: str
    linked: bool


class ExtractedEntity(BaseModel):
    """An entity extracted from memory content."""

    name: str
    type: str
    confidence: float
    span_start: Optional[int] = None
    span_end: Optional[int] = None


class EntityExtractionResult(BaseResponse):
    """Result of entity extraction from a memory."""

    memory_id: str
    entities: List[ExtractedEntity]
    saved: bool = False
    linked: bool = False


class EntityTypeInfo(BaseModel):
    """Entity type with count."""

    name: str
    count: int


class EntityTypesResult(BaseResponse):
    """Result of getting entity types."""

    types: List[EntityTypeInfo]


class EntityFactsResult(BaseResponse):
    """Result of getting entity facts."""

    entity_id: str
    facts: List[Fact]
