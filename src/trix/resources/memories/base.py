"""Base memory operations mixin.

Provides core CRUD operations for memories that are shared between
sync and async implementations.
"""

from typing import Any, Dict, List, Optional

from ...types import (
    BulkResult,
    Memory,
    MemoryConfig,
    MemoryCreate,
    MemoryList,
    MemoryOptions,
    MemoryStats,
    MemoryType,
    MemoryUpdate,
    SearchMode,
    Topic,
)
from ...utils.security import validate_id


def build_list_params(
    q: Optional[str] = None,
    mode: Optional[SearchMode] = None,
    limit: int = 100,
    offset: int = 0,
    tags: Optional[List[str]] = None,
    space_id: Optional[str] = None,
    pinned: Optional[bool] = None,
    protected: Optional[bool] = None,
    min_quality: Optional[float] = None,
    include_deleted: bool = False,
    session_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Build query parameters for list operation."""
    params: Dict[str, Any] = {"limit": limit, "offset": offset}
    if q:
        params["q"] = q
    if mode:
        params["mode"] = mode.value
    if tags:
        params["tags"] = ",".join(tags)
    if space_id:
        params["space_id"] = space_id
    if pinned is not None:
        params["pinned"] = "true" if pinned else "false"
    if protected is not None:
        params["protected"] = "true" if protected else "false"
    if min_quality is not None:
        params["min_quality"] = str(min_quality)
    if include_deleted:
        params["include_deleted"] = "true"
    if session_id:
        params["session_id"] = session_id
    return params


def build_iter_params(
    q: Optional[str] = None,
    mode: Optional[SearchMode] = None,
    tags: Optional[List[str]] = None,
    space_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Build query parameters for iteration."""
    params: Dict[str, Any] = {}
    if q:
        params["q"] = q
    if mode:
        params["mode"] = mode.value
    if tags:
        params["tags"] = ",".join(tags)
    if space_id:
        params["space_id"] = space_id
    return params


def build_create_data(
    content: str,
    type: Optional[MemoryType] = None,
    tags: Optional[List[str]] = None,
    metadata: Optional[Dict[str, Any]] = None,
    priority: Optional[int] = None,
    space_id: Optional[str] = None,
    options: Optional[Dict[str, Any]] = None,
    is_pinned: bool = False,
    protection_level: str = "none",
    session_id: Optional[str] = None,
) -> MemoryCreate:
    """Build MemoryCreate data object."""
    return MemoryCreate(
        content=content,
        type=type or MemoryType.TEXT,
        tags=tags,
        metadata=metadata,
        priority=priority,
        space_id=space_id,
        options=MemoryOptions(**options) if options else None,
        is_pinned=is_pinned if is_pinned else None,
        protection_level=protection_level if protection_level != "none" else None,
        session_id=session_id,
    )


def build_update_data(
    content: Optional[str] = None,
    tags: Optional[List[str]] = None,
    metadata: Optional[Dict[str, Any]] = None,
    priority: Optional[int] = None,
) -> MemoryUpdate:
    """Build MemoryUpdate data object."""
    return MemoryUpdate(
        content=content,
        tags=tags,
        metadata=metadata,
        priority=priority,
    )


def build_stats_params(
    space_id: Optional[str] = None,
    created_after: Optional[str] = None,
    created_before: Optional[str] = None,
    include_type_distribution: bool = False,
    include_tag_distribution: bool = False,
    include_timeline: bool = False,
    timeline_granularity: Optional[str] = None,
) -> Dict[str, Any]:
    """Build query parameters for stats operation."""
    params: Dict[str, Any] = {}
    if space_id:
        params["space_id"] = space_id
    if created_after:
        params["created_after"] = created_after
    if created_before:
        params["created_before"] = created_before
    if include_type_distribution:
        params["include_type_distribution"] = "true"
    if include_tag_distribution:
        params["include_tag_distribution"] = "true"
    if include_timeline:
        params["include_timeline"] = "true"
    if timeline_granularity:
        params["timeline_granularity"] = timeline_granularity
    return params


def build_topics_params(
    refresh: bool = False,
    min_relevance: Optional[float] = None,
    categories: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """Build query parameters for topics operation."""
    params: Dict[str, Any] = {}
    if refresh:
        params["refresh"] = "true"
    if min_relevance is not None:
        params["min_relevance"] = str(min_relevance)
    if categories:
        params["categories"] = ",".join(categories)
    return params


def build_transcribe_body(
    language: Optional[str] = None,
    prompt: Optional[str] = None,
    provider: Optional[str] = None,
    enable_speaker_diarization: Optional[bool] = None,
    enable_entity_detection: Optional[bool] = None,
    enable_content_safety: Optional[bool] = None,
    enable_auto_chapters: Optional[bool] = None,
    enable_auto_summarization: Optional[bool] = None,
    speakers_expected: Optional[int] = None,
) -> Dict[str, Any]:
    """Build request body for transcribe operation."""
    body: Dict[str, Any] = {}
    if language:
        body["language"] = language
    if prompt:
        body["prompt"] = prompt
    if provider:
        body["provider"] = provider
    if enable_speaker_diarization is not None:
        body["enableSpeakerDiarization"] = enable_speaker_diarization
    if enable_entity_detection is not None:
        body["enableEntityDetection"] = enable_entity_detection
    if enable_content_safety is not None:
        body["enableContentSafety"] = enable_content_safety
    if enable_auto_chapters is not None:
        body["enableAutoChapters"] = enable_auto_chapters
    if enable_auto_summarization is not None:
        body["enableAutoSummarization"] = enable_auto_summarization
    if speakers_expected is not None:
        body["speakersExpected"] = speakers_expected
    return body


def validate_bulk_updates(updates: List[Dict[str, Any]]) -> None:
    """Validate bulk update requests."""
    for i, update in enumerate(updates):
        if "id" not in update:
            raise ValueError(f"Update at index {i} is missing an 'id'")
        validate_id(update["id"], f"memory[{i}]")


def validate_bulk_ids(ids: List[str]) -> None:
    """Validate list of memory IDs."""
    for i, item_id in enumerate(ids):
        validate_id(item_id, f"memory[{i}]")


def validate_protection_level(level: str) -> None:
    """Validate protection level value."""
    if level not in ("none", "soft", "hard"):
        raise ValueError(f"Invalid protection level: {level}. Must be 'none', 'soft', or 'hard'")
