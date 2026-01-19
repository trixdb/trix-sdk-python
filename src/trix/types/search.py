"""Search-related types for Trix SDK."""

from typing import List, Optional

from .base import BaseResponse
from .memory import Memory


class SearchResult(BaseResponse):
    """Search result with similarity score."""

    memory: Memory
    score: float
    highlights: Optional[List[str]] = None


class SearchResults(BaseResponse):
    """List of search results."""

    data: List[SearchResult]
    query: Optional[str] = None


class SearchConfig(BaseResponse):
    """Search system configuration."""

    default_limit: int
    max_limit: int
    min_similarity_threshold: float


class EmbeddingResponse(BaseResponse):
    """Embedding generation response."""

    memory_ids: List[str]
    embeddings: List[List[float]]


class EmbedAllResponse(BaseResponse):
    """Batch embedding response."""

    total_processed: int
    batch_size: int
    status: str
