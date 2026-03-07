"""Note-related types for Trix SDK (ADR-065)."""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel

from .base import BaseResponse


class NoteBlock(BaseResponse):
    """A content block within a note."""

    id: str
    note_id: str
    block_type: str
    content: Optional[Dict[str, Any]] = None
    sort_order: str
    parent_block_id: Optional[str] = None
    created_at: str
    updated_at: str


class NoteCollaborator(BaseResponse):
    """A collaborator on a note."""

    id: str
    note_id: str
    actor_type: str
    actor_id: str
    permission: str = "read"
    created_at: str


class Note(BaseResponse):
    """Note object - a block-based document or canvas."""

    id: str
    account_id: str
    space_id: Optional[str] = None
    created_by: str
    title: Optional[str] = None
    icon: Optional[str] = None
    cover_image_url: Optional[str] = None
    note_type: str = "document"
    parent_note_id: Optional[str] = None
    is_pinned: bool = False
    is_archived: bool = False
    tags: List[str] = []
    properties: Dict[str, Any] = {}
    visibility: str = "private"
    version: int = 1
    blocks: Optional[List[NoteBlock]] = None
    collaborators: Optional[List[NoteCollaborator]] = None
    created_at: str
    updated_at: str


class NoteCreate(BaseModel):
    """Request to create a note."""

    title: Optional[str] = None
    note_type: Optional[str] = None
    visibility: Optional[str] = None
    space_id: Optional[str] = None
    parent_note_id: Optional[str] = None
    icon: Optional[str] = None
    tags: Optional[List[str]] = None
    blocks: Optional[List[Dict[str, Any]]] = None


class NoteUpdate(BaseModel):
    """Request to update a note."""

    version: int
    title: Optional[str] = None
    icon: Optional[str] = None
    visibility: Optional[str] = None
    is_pinned: Optional[bool] = None
    is_archived: Optional[bool] = None
    tags: Optional[List[str]] = None


class NoteList(BaseResponse):
    """List of notes with pagination."""

    notes: List[Note]
    total: int = 0
    limit: int = 20
    offset: int = 0


class NoteBlockCreate(BaseModel):
    """Request to add a block to a note."""

    block_type: str
    content: Optional[Dict[str, Any]] = None
    sort_order: Optional[str] = None
    after_block_id: Optional[str] = None
    parent_block_id: Optional[str] = None


class NoteBlockUpdate(BaseModel):
    """Request to update a note block."""

    content: Optional[Dict[str, Any]] = None
    block_type: Optional[str] = None
    sort_order: Optional[str] = None


class NoteCollaboratorCreate(BaseModel):
    """Request to add a collaborator to a note."""

    actor_type: str
    actor_id: str
    permission: Optional[str] = None


# =============================================================================
# Links (Phase 3)
# =============================================================================


class NoteLink(BaseResponse):
    """A link between two notes."""

    id: str
    source_note_id: str
    source_block_id: Optional[str] = None
    target_note_id: str
    target_block_id: Optional[str] = None
    link_type: str = "reference"
    target_title: Optional[str] = None
    target_note_type: Optional[str] = None
    source_title: Optional[str] = None
    source_note_type: Optional[str] = None
    created_at: str


class NoteLinkCreate(BaseModel):
    """Request to create a note link."""

    target_note_id: str
    source_block_id: Optional[str] = None
    target_block_id: Optional[str] = None
    link_type: Optional[str] = None


# =============================================================================
# Memories (Phase 3)
# =============================================================================


class NoteMemoryLink(BaseResponse):
    """A link between a note and a memory."""

    note_id: str
    memory_id: str
    block_id: Optional[str] = None
    link_type: str = "manual"
    relevance_score: Optional[float] = None
    created_at: str


class NoteMemoryLinkCreate(BaseModel):
    """Request to link a memory to a note."""

    memory_id: str
    block_id: Optional[str] = None
    link_type: Optional[str] = None
    relevance_score: Optional[float] = None


class NoteMemoryList(BaseResponse):
    """List of note-memory links with pagination."""

    memories: List[NoteMemoryLink]
    total: int
    limit: int = 50
    offset: int = 0
