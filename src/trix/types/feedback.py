"""Feedback-related types for Trix SDK."""

from typing import List, Optional

from pydantic import BaseModel

from .base import BaseResponse


class FeedbackResult(BaseResponse):
    """Result object in feedback."""

    memory_id: str
    score: float
    rank: int


class FeedbackSubmit(BaseModel):
    """Submit detailed feedback."""

    query_context: str
    results: List[FeedbackResult]
    boost_amount: Optional[float] = None
    create_relationships: Optional[bool] = True


class FeedbackResponse(BaseResponse):
    """Feedback submission response."""

    relationships_created: int
    memories_boosted: int
