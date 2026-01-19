"""Image-related types for Trix SDK."""

from typing import TYPE_CHECKING, Any, Dict, List, Optional

from pydantic import BaseModel, Field

from .base import BaseResponse

if TYPE_CHECKING:
    from .memory import Memory


class VisualSearchResult(BaseResponse):
    """Result of visual similarity search."""

    memory: "Memory"
    score: float
    distance: Optional[float] = None


class VisualSearchResults(BaseResponse):
    """List of visual search results."""

    data: List[VisualSearchResult]
    query_type: Optional[str] = None


class ImageCluster(BaseModel):
    """A cluster of visually similar images."""

    cluster_id: int
    representative_id: Optional[str] = None
    memory_ids: List[str]
    size: int
    centroid: Optional[List[float]] = None


class ImageClusterResult(BaseResponse):
    """Result of image clustering operation."""

    clusters: List[ImageCluster]
    total_images: int
    num_clusters: int
    silhouette_score: Optional[float] = None


class ImageTag(BaseModel):
    """Auto-generated tag for an image."""

    name: str
    confidence: float
    category: Optional[str] = None


class AutoTagResult(BaseResponse):
    """Result of auto-tagging an image."""

    image_id: str
    tags: List[ImageTag]
    applied: bool = False


class BatchAutoTagResult(BaseResponse):
    """Result of batch auto-tagging images."""

    results: List[AutoTagResult]
    success: int
    failed: int


class DuplicateCheckResult(BaseResponse):
    """Result of duplicate image check."""

    is_duplicate: bool
    duplicates: List[Dict[str, Any]] = Field(default_factory=list)
    threshold: float = 0.95


class QuerySuggestion(BaseModel):
    """A suggested search query."""

    query: str
    type: str
    count: Optional[int] = None


class QuerySuggestionsResult(BaseResponse):
    """Result of query suggestions."""

    suggestions: List[QuerySuggestion]


# Rebuild model for forward references
from .memory import Memory  # noqa: E402, F811

VisualSearchResult.model_rebuild()
VisualSearchResults.model_rebuild()
