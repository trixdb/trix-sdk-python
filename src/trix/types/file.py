"""File type definitions for Trix SDK (ADR-068 Phase 4)."""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel

from .base import BaseResponse


class ChatFile(BaseResponse):
    """Chat file record."""

    id: str
    filename: str
    content_type: Optional[str] = None
    size_bytes: Optional[int] = None
    status: Optional[str] = None
    message_type: Optional[str] = None
    width: Optional[int] = None
    height: Optional[int] = None
    duration_ms: Optional[int] = None
    has_thumbnail: Optional[bool] = None
    checksum_sha256: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    download_url: Optional[str] = None
    thumbnail_url: Optional[str] = None
    created_at: Optional[str] = None


class FileDownloadInfo(BaseResponse):
    """File download info with signed URL."""

    url: str
    thumbnail_url: Optional[str] = None
    expires_in: int
    filename: str
    content_type: str
    size_bytes: int


class FileQuota(BaseResponse):
    """Storage quota for an account."""

    total_bytes: int
    file_count: int
    max_bytes: int
    max_file_size: int
    usage_percent: int


class FileListResult(BaseResponse):
    """File list response with pagination."""

    files: List[ChatFile]
    has_more: bool
    cursor: Optional[str] = None


class FileUploadBase64(BaseModel):
    """Request model for base64 file upload."""

    filename: str
    content_base64: str
    content_type: str
    conversation_id: Optional[str] = None
    message_id: Optional[str] = None
