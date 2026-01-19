"""Resource-related types for Trix SDK."""

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from .base import BaseResponse, Pagination
from .enums import ResourceRelationshipType


class Resource(BaseResponse):
    """Resource object - represents a project, topic, or other grouping for memories."""

    id: str
    name: str
    type: str = "project"
    description: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime
    updated_at: datetime


class ResourceCreate(BaseModel):
    """Request to create a resource."""

    name: str
    type: Optional[str] = "project"
    description: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class ResourceUpdate(BaseModel):
    """Request to update a resource."""

    name: Optional[str] = None
    type: Optional[str] = None
    description: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class ResourceList(BaseResponse):
    """List of resources with pagination."""

    data: List[Resource]
    pagination: Pagination


class MemoryResource(BaseResponse):
    """Memory-resource link."""

    memory_id: str
    resource_id: str
    relationship_type: ResourceRelationshipType = ResourceRelationshipType.RELATED
    created_at: datetime
    resource: Optional[Resource] = None


class MemoryResourceList(BaseResponse):
    """List of memory-resource links."""

    data: List[MemoryResource]


class MemoryResourceLinkResult(BaseResponse):
    """Result of linking a resource to a memory."""

    memory_id: str
    resource_id: str
    relationship_type: ResourceRelationshipType
    linked: bool


class MemoryResourceUnlinkResult(BaseResponse):
    """Result of unlinking a resource from a memory."""

    memory_id: str
    resource_id: str
    unlinked: bool
