"""Entity-related types for Trix SDK."""

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import Field

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


class EntityList(BaseResponse):
    """List of entities with pagination."""

    data: List[Entity]
    total: int = 0
    limit: int = 10
    offset: int = 0


class EntityMergeResult(BaseResponse):
    """Result of entity merge."""

    merged_entity: Entity
    deleted_id: str


class EntityFactsResult(BaseResponse):
    """Result of getting entity facts."""

    entity_id: str
    facts: List[Fact]
