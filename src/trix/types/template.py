"""Template-related types for Trix SDK."""

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel

from .base import BaseResponse


class TemplateCreate(BaseModel):
    """Request to create a template."""

    name: str
    description: Optional[str] = None
    category: Optional[str] = None
    tags: Optional[List[str]] = None
    system_prompt: Optional[str] = None
    tools: Optional[List[Dict[str, Any]]] = None
    settings: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None


class TemplateUpdate(BaseModel):
    """Request to update a template."""

    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    tags: Optional[List[str]] = None
    system_prompt: Optional[str] = None
    tools: Optional[List[Dict[str, Any]]] = None
    settings: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None
    status: Optional[str] = None


class Template(BaseResponse):
    """Template object - a reusable bot/agent configuration."""

    id: str
    account_id: str
    name: str
    slug: str
    description: Optional[str] = None
    category: Optional[str] = None
    tags: List[str] = []
    system_prompt: Optional[str] = None
    tools: List[Dict[str, Any]] = []
    settings: Dict[str, Any] = {}
    metadata: Dict[str, Any] = {}
    status: str = "active"
    is_public: bool = False
    install_count: int = 0
    rating: Optional[float] = None
    review_count: int = 0
    author_id: Optional[str] = None
    author_name: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class TemplateList(BaseResponse):
    """List of templates with pagination."""

    templates: List[Template]
    total: int = 0
    limit: int = 20
    offset: int = 0


class TemplateReview(BaseResponse):
    """A review of a marketplace template."""

    id: str
    template_id: str
    account_id: str
    rating: int
    comment: Optional[str] = None
    created_at: datetime


class TemplateReviewCreate(BaseModel):
    """Request to review a template."""

    rating: int
    comment: Optional[str] = None


class TemplateInstallResult(BaseResponse):
    """Result of installing a template."""

    bot_id: str
    template_id: str
    message: str
