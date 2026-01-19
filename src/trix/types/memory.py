"""Memory-related types for Trix SDK."""

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from .base import BaseResponse
from .enums import MemoryType, OriginType, SourceType


class MemoryOptions(BaseModel):
    """Options for memory creation."""

    transcribe_audio: Optional[bool] = None
    language: Optional[str] = None
    skip_embedding: Optional[bool] = None


class Memory(BaseResponse):
    """Memory object."""

    id: str
    content: str
    type: MemoryType = MemoryType.TEXT
    tags: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    priority: Optional[int] = None
    space_id: Optional[str] = None
    embedding: Optional[List[float]] = None
    created_at: datetime
    updated_at: datetime
    access_count: int = 0
    last_accessed_at: Optional[datetime] = None
    transcript: Optional[str] = None
    audio_url: Optional[str] = None
    session_id: Optional[str] = None
    origin_type: Optional[OriginType] = None
    source_type: Optional[SourceType] = None
    source_id: Optional[str] = None
    source_metadata: Dict[str, Any] = Field(default_factory=dict)
    is_pinned: bool = False
    protection_level: Optional[str] = None
    is_deleted: bool = False
    deleted_at: Optional[datetime] = None
    quality_score: Optional[float] = None


class MemoryCreate(BaseModel):
    """Request to create a memory."""

    content: str
    type: Optional[MemoryType] = MemoryType.TEXT
    tags: Optional[List[str]] = None
    metadata: Optional[Dict[str, Any]] = None
    priority: Optional[int] = None
    space_id: Optional[str] = None
    options: Optional[MemoryOptions] = None
    session_id: Optional[str] = None
    origin_type: Optional[OriginType] = None
    source_type: Optional[SourceType] = None
    source_id: Optional[str] = None
    source_metadata: Optional[Dict[str, Any]] = None
    resource_ids: Optional[List[str]] = None
    is_pinned: Optional[bool] = None
    protection_level: Optional[str] = None


class MemoryUpdate(BaseModel):
    """Request to update a memory."""

    content: Optional[str] = None
    tags: Optional[List[str]] = None
    metadata: Optional[Dict[str, Any]] = None
    priority: Optional[int] = None
    origin_type: Optional[OriginType] = None
    source_type: Optional[SourceType] = None
    source_id: Optional[str] = None
    source_metadata: Optional[Dict[str, Any]] = None
    is_pinned: Optional[bool] = None
    protection_level: Optional[str] = None


class MemoryList(BaseResponse):
    """List of memories with pagination."""

    data: List[Memory]
    total: int
    limit: int
    offset: int


class MemoryConfig(BaseResponse):
    """Memory system configuration."""

    max_content_length: int
    supported_types: List[str]
    embedding_model: str
    embedding_dimensions: int


class MemoryStats(BaseResponse):
    """Memory statistics."""

    total: int
    by_type: Optional[Dict[str, int]] = None
    by_tag: Optional[Dict[str, int]] = None
    timeline: Optional[List[Dict[str, Any]]] = None
    avg_content_length: Optional[float] = None
    total_size: Optional[int] = None
