"""Enrichment-related types for Trix SDK."""

from datetime import datetime
from typing import Any, Dict, List, Optional

from .base import BaseResponse
from .enums import EnrichmentStatus


class Enrichment(BaseResponse):
    """Enrichment object for a memory."""

    type: str
    status: EnrichmentStatus
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    processed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime


class EnrichmentList(BaseResponse):
    """List of enrichments."""

    data: List[Enrichment]


class EnrichmentResult(BaseResponse):
    """Result of triggering enrichments."""

    memory_id: str
    triggered: List[str]
    job_ids: Optional[List[str]] = None
    status: str
