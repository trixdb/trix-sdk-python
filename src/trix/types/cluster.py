"""Cluster-related types for Trix SDK."""

from datetime import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Optional

from pydantic import BaseModel, Field

from .base import BaseResponse

if TYPE_CHECKING:
    from .memory import Memory


class Cluster(BaseResponse):
    """Cluster of related memories."""

    id: str
    name: str
    description: Optional[str] = None
    color: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
    memory_count: int = 0
    scale: Optional[str] = None
    memories: Optional[List["Memory"]] = None
    created_at: datetime
    updated_at: datetime


class ClusterCreate(BaseModel):
    """Request to create a cluster."""

    name: str
    description: Optional[str] = None
    color: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class ClusterUpdate(BaseModel):
    """Request to update a cluster."""

    name: Optional[str] = None
    description: Optional[str] = None
    color: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class ClusterList(BaseResponse):
    """List of clusters with pagination."""

    data: List[Cluster]
    cursor: Optional[str] = None


class ClusterMembership(BaseResponse):
    """Memory membership in a cluster."""

    cluster_id: str
    memory_id: str
    confidence: float = 1.0
    added_at: datetime


class ClusterStats(BaseResponse):
    """Cluster statistics."""

    total: int
    avg_size: float
    avg_quality: float
    by_space: Optional[Dict[str, int]] = None


class ClusterQuality(BaseResponse):
    """Cluster quality metrics."""

    cluster_id: str
    coherence: float
    separation: float
    silhouette_score: float
    outlier_count: int


class ClusterTopic(BaseModel):
    """A topic in a cluster."""

    label: str
    score: float
    keywords: List[str]


class ClusterTopics(BaseResponse):
    """Cluster topics."""

    cluster_id: str
    topics: List[ClusterTopic]


class IncrementalClusterResult(BaseResponse):
    """Result of incremental clustering."""

    job_id: str
    status: str
    estimated_memories: int


# Rebuild model for forward references
from .memory import Memory  # noqa: E402, F811

Cluster.model_rebuild()
