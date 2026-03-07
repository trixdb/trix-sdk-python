"""Notes resource for Trix SDK (ADR-065)."""

from typing import Any, Dict, List, Optional

from .base import BaseSyncResource
from ..types.note import (
    Note,
    NoteBlock,
    NoteBlockCreate,
    NoteBlockUpdate,
    NoteCollaborator,
    NoteCollaboratorCreate,
    NoteCreate,
    NoteList,
    NoteUpdate,
)
from ..utils.security import validate_id


class NotesResource(BaseSyncResource):
    """Resource for managing notes and canvas documents.

    Example:
        >>> note = client.notes.create(title="Meeting Notes")
        >>> client.notes.add_block(note.id, block_type="paragraph",
        ...     content={"text": "Discussion points..."})
    """

    def create(
        self,
        title: Optional[str] = None,
        note_type: Optional[str] = None,
        visibility: Optional[str] = None,
        space_id: Optional[str] = None,
        parent_note_id: Optional[str] = None,
        icon: Optional[str] = None,
        tags: Optional[List[str]] = None,
        blocks: Optional[List[Dict[str, Any]]] = None,
    ) -> Note:
        """Create a new note."""
        data = NoteCreate(
            title=title,
            note_type=note_type,
            visibility=visibility,
            space_id=space_id,
            parent_note_id=parent_note_id,
            icon=icon,
            tags=tags,
            blocks=blocks,
        )
        response = self._request("POST", "/notes", json=data.model_dump(exclude_none=True))
        return Note.model_validate(response)

    def list(
        self,
        space_id: Optional[str] = None,
        note_type: Optional[str] = None,
        visibility: Optional[str] = None,
        parent_note_id: Optional[str] = None,
        is_pinned: Optional[bool] = None,
        is_archived: Optional[bool] = None,
        tags: Optional[str] = None,
        q: Optional[str] = None,
        limit: int = 20,
        offset: int = 0,
    ) -> NoteList:
        """List notes with optional filtering."""
        params: Dict[str, Any] = {"limit": limit, "offset": offset}
        if space_id is not None:
            params["spaceId"] = space_id
        if note_type is not None:
            params["noteType"] = note_type
        if visibility is not None:
            params["visibility"] = visibility
        if parent_note_id is not None:
            params["parentNoteId"] = parent_note_id
        if is_pinned is not None:
            params["isPinned"] = is_pinned
        if is_archived is not None:
            params["isArchived"] = is_archived
        if tags is not None:
            params["tags"] = tags
        if q is not None:
            params["q"] = q
        response = self._request("GET", "/notes", params=params)
        return NoteList.model_validate(response)

    def get(self, note_id: str) -> Note:
        """Get a note by ID including its blocks."""
        validate_id(note_id, "note")
        response = self._request("GET", f"/notes/{note_id}")
        return Note.model_validate(response)

    def update(
        self,
        note_id: str,
        version: int,
        title: Optional[str] = None,
        icon: Optional[str] = None,
        visibility: Optional[str] = None,
        is_pinned: Optional[bool] = None,
        is_archived: Optional[bool] = None,
        tags: Optional[List[str]] = None,
    ) -> Note:
        """Update a note. Requires current version for optimistic locking."""
        validate_id(note_id, "note")
        data = NoteUpdate(
            version=version,
            title=title,
            icon=icon,
            visibility=visibility,
            is_pinned=is_pinned,
            is_archived=is_archived,
            tags=tags,
        )
        response = self._request(
            "PATCH", f"/notes/{note_id}", json=data.model_dump(exclude_none=True)
        )
        return Note.model_validate(response)

    def delete(self, note_id: str) -> None:
        """Soft-delete a note."""
        validate_id(note_id, "note")
        self._request("DELETE", f"/notes/{note_id}")

    def add_block(
        self,
        note_id: str,
        block_type: str,
        content: Optional[Dict[str, Any]] = None,
        sort_order: Optional[str] = None,
        after_block_id: Optional[str] = None,
        parent_block_id: Optional[str] = None,
    ) -> NoteBlock:
        """Add a content block to a note."""
        validate_id(note_id, "note")
        data = NoteBlockCreate(
            block_type=block_type,
            content=content,
            sort_order=sort_order,
            after_block_id=after_block_id,
            parent_block_id=parent_block_id,
        )
        response = self._request(
            "POST", f"/notes/{note_id}/blocks", json=data.model_dump(exclude_none=True)
        )
        return NoteBlock.model_validate(response)

    def update_block(
        self,
        note_id: str,
        block_id: str,
        content: Optional[Dict[str, Any]] = None,
        block_type: Optional[str] = None,
        sort_order: Optional[str] = None,
    ) -> NoteBlock:
        """Update a block in a note."""
        validate_id(note_id, "note")
        validate_id(block_id, "block")
        data = NoteBlockUpdate(
            content=content,
            block_type=block_type,
            sort_order=sort_order,
        )
        response = self._request(
            "PATCH",
            f"/notes/{note_id}/blocks/{block_id}",
            json=data.model_dump(exclude_none=True),
        )
        return NoteBlock.model_validate(response)

    def delete_block(self, note_id: str, block_id: str) -> None:
        """Delete a block from a note."""
        validate_id(note_id, "note")
        validate_id(block_id, "block")
        self._request("DELETE", f"/notes/{note_id}/blocks/{block_id}")

    def add_collaborator(
        self,
        note_id: str,
        actor_type: str,
        actor_id: str,
        permission: Optional[str] = None,
    ) -> NoteCollaborator:
        """Add a collaborator to a note."""
        validate_id(note_id, "note")
        data = NoteCollaboratorCreate(
            actor_type=actor_type,
            actor_id=actor_id,
            permission=permission,
        )
        response = self._request(
            "POST",
            f"/notes/{note_id}/collaborators",
            json=data.model_dump(exclude_none=True),
        )
        return NoteCollaborator.model_validate(response)

    def list_collaborators(self, note_id: str) -> List[NoteCollaborator]:
        """List collaborators on a note."""
        validate_id(note_id, "note")
        response = self._request("GET", f"/notes/{note_id}/collaborators")
        return [NoteCollaborator.model_validate(c) for c in response]

    def remove_collaborator(self, note_id: str, collaborator_id: str) -> None:
        """Remove a collaborator from a note."""
        validate_id(note_id, "note")
        validate_id(collaborator_id, "collaborator")
        self._request("DELETE", f"/notes/{note_id}/collaborators/{collaborator_id}")
