"""Relationship-related types for Trix SDK."""

from datetime import datetime
from typing import TYPE_CHECKING, List, Optional

from pydantic import BaseModel

from .base import BaseResponse
from .enums import RelationshipType

if TYPE_CHECKING:
    from .memory import Memory


class Relationship(BaseResponse):
    """Relationship between memories."""

    id: str
    source_id: str
    target_id: str
    relationship_type: RelationshipType
    description: Optional[str] = None
    weight: float = 1.0
    strength: Optional[float] = None
    bidirectional: bool = False
    created_at: datetime
    updated_at: datetime
    reinforcement_count: int = 0


class RelationshipCreate(BaseModel):
    """Request to create a relationship."""

    relationship_type: RelationshipType
    description: Optional[str] = None
    weight: Optional[float] = 1.0
    bidirectional: Optional[bool] = False


class RelationshipUpdate(BaseModel):
    """Request to update a relationship."""

    weight: Optional[float] = None
    description: Optional[str] = None


class RelationshipList(BaseResponse):
    """List of relationships."""

    data: List[Relationship]


class RelationshipTypeInfo(BaseModel):
    """Relationship type info."""

    name: str
    count: int
    description: Optional[str] = None


class RelationshipTypesResult(BaseResponse):
    """Result of getting relationship types."""

    types: List[RelationshipTypeInfo]


class RelatedMemory(BaseModel):
    """A related memory with relationship info."""

    memory: "Memory"
    relationship: Relationship
    score: float


class RelatedMemoriesResult(BaseResponse):
    """Result of getting related memories."""

    memory_id: str
    related: List[RelatedMemory]


class ReinforceGroupResult(BaseResponse):
    """Result of reinforcing a group of relationships."""

    reinforced: int
    failed: int


# Import Memory for forward reference resolution
from .memory import Memory  # noqa: E402, F811

RelatedMemory.model_rebuild()
