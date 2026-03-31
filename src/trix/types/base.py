"""Base models and common types for Trix SDK."""

from typing import Any, Dict, Generic, List, Optional, TypeVar

from pydantic import BaseModel, ConfigDict, Field

T = TypeVar("T")


class BaseResponse(BaseModel):
    """Base response model."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)


class Pagination(BaseModel):
    """Pagination metadata for list responses."""

    total: int
    page: int
    limit: int
    has_more: bool
    cursor: Optional[str] = None


class PaginatedResponse(BaseResponse, Generic[T]):
    """Generic paginated response wrapper."""

    data: List[T]
    pagination: Pagination


class BulkResult(BaseResponse):
    """Result of a bulk operation."""

    success: int
    failed: int
    errors: List[Dict[str, Any]] = Field(default_factory=list)

    @property
    def total(self) -> int:
        """Total number of items in the bulk operation."""
        return self.success + self.failed

    @property
    def success_rate(self) -> float:
        """Success rate as a decimal (0.0 to 1.0)."""
        if self.total == 0:
            return 0.0
        return self.success / self.total
