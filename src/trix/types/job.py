"""Job-related types for Trix SDK."""

from datetime import datetime
from typing import Any, Dict, List, Optional

from .base import BaseResponse
from .enums import JobStatus


class Job(BaseResponse):
    """Background job."""

    id: str
    queue: str
    name: str
    data: Dict[str, Any]
    status: JobStatus
    progress: Optional[int] = None
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    created_at: datetime
    processed_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None


class JobStats(BaseResponse):
    """Job queue statistics."""

    queue: str
    waiting: int
    active: int
    completed: int
    failed: int
    delayed: int


class JobList(BaseResponse):
    """List of jobs."""

    data: List[Job]
