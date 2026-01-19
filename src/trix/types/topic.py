"""Topic-related types for Trix SDK."""

from typing import TYPE_CHECKING, List

from pydantic import BaseModel

from .base import BaseResponse

if TYPE_CHECKING:
    from .memory import Memory


class Topic(BaseModel):
    """Extracted topic from a memory."""

    name: str
    relevance: float
    category: str


class TopicList(BaseResponse):
    """List of topics extracted from a memory."""

    memory_id: str
    topics: List[Topic]


class TopicSearchResult(BaseResponse):
    """Result of searching by topic."""

    topic: str
    memories: List["Memory"]


# Rebuild model for forward references
from .memory import Memory  # noqa: E402, F811

TopicSearchResult.model_rebuild()
