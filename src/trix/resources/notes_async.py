"""Async notes resource for Trix SDK (ADR-065)."""

from typing import Any, Dict, List, Optional

from .base import BaseAsyncResource
from ..types.note import (
    Note,
    NoteBlock,
    NoteBlockCreate,
    NoteBlockUpdate,
    NoteCollaborator,
    NoteCollaboratorCreate,
    NoteCreate,
    NoteLink,
    NoteLinkCreate,
    NoteList,
    NoteMemoryLink,
    NoteMemoryLinkCreate,
    NoteMemoryList,
    NoteUpdate,
)
from ..utils.security import validate_id


class AsyncNotesResource(BaseAsyncResource):
    """Async resource for managing notes and canvas documents.

    Example:
        >>> note = await client.notes.create(title="Meeting Notes")
        >>> await client.notes.add_block(note.id, block_type="paragraph",
        ...     content={"text": "Discussion points..."})
    """

    async def create(
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
        """Create a new note (async)."""
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
        response = await self._request("POST", "/notes", json=data.model_dump(exclude_none=True))
        return Note.model_validate(response)

    async def list(
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
        """List notes with optional filtering (async)."""
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
        response = await self._request("GET", "/notes", params=params)
        return NoteList.model_validate(response)

    async def get(self, note_id: str) -> Note:
        """Get a note by ID including its blocks (async)."""
        validate_id(note_id, "note")
        response = await self._request("GET", f"/notes/{note_id}")
        return Note.model_validate(response)

    async def update(
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
        """Update a note (async). Requires current version for optimistic locking."""
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
        response = await self._request(
            "PATCH", f"/notes/{note_id}", json=data.model_dump(exclude_none=True)
        )
        return Note.model_validate(response)

    async def delete(self, note_id: str) -> None:
        """Soft-delete a note (async)."""
        validate_id(note_id, "note")
        await self._request("DELETE", f"/notes/{note_id}")

    async def add_block(
        self,
        note_id: str,
        block_type: str,
        content: Optional[Dict[str, Any]] = None,
        sort_order: Optional[str] = None,
        after_block_id: Optional[str] = None,
        parent_block_id: Optional[str] = None,
    ) -> NoteBlock:
        """Add a content block to a note (async)."""
        validate_id(note_id, "note")
        data = NoteBlockCreate(
            block_type=block_type,
            content=content,
            sort_order=sort_order,
            after_block_id=after_block_id,
            parent_block_id=parent_block_id,
        )
        response = await self._request(
            "POST", f"/notes/{note_id}/blocks", json=data.model_dump(exclude_none=True)
        )
        return NoteBlock.model_validate(response)

    async def update_block(
        self,
        note_id: str,
        block_id: str,
        content: Optional[Dict[str, Any]] = None,
        block_type: Optional[str] = None,
        sort_order: Optional[str] = None,
    ) -> NoteBlock:
        """Update a block in a note (async)."""
        validate_id(note_id, "note")
        validate_id(block_id, "block")
        data = NoteBlockUpdate(
            content=content,
            block_type=block_type,
            sort_order=sort_order,
        )
        response = await self._request(
            "PATCH",
            f"/notes/{note_id}/blocks/{block_id}",
            json=data.model_dump(exclude_none=True),
        )
        return NoteBlock.model_validate(response)

    async def delete_block(self, note_id: str, block_id: str) -> None:
        """Delete a block from a note (async)."""
        validate_id(note_id, "note")
        validate_id(block_id, "block")
        await self._request("DELETE", f"/notes/{note_id}/blocks/{block_id}")

    async def add_collaborator(
        self,
        note_id: str,
        actor_type: str,
        actor_id: str,
        permission: Optional[str] = None,
    ) -> NoteCollaborator:
        """Add a collaborator to a note (async)."""
        validate_id(note_id, "note")
        data = NoteCollaboratorCreate(
            actor_type=actor_type,
            actor_id=actor_id,
            permission=permission,
        )
        response = await self._request(
            "POST",
            f"/notes/{note_id}/collaborators",
            json=data.model_dump(exclude_none=True),
        )
        return NoteCollaborator.model_validate(response)

    async def list_collaborators(self, note_id: str) -> List[NoteCollaborator]:
        """List collaborators on a note (async)."""
        validate_id(note_id, "note")
        response = await self._request("GET", f"/notes/{note_id}/collaborators")
        return [NoteCollaborator.model_validate(c) for c in response]

    async def remove_collaborator(self, note_id: str, collaborator_id: str) -> None:
        """Remove a collaborator from a note (async)."""
        validate_id(note_id, "note")
        validate_id(collaborator_id, "collaborator")
        await self._request("DELETE", f"/notes/{note_id}/collaborators/{collaborator_id}")

    async def create_link(
        self,
        note_id: str,
        target_note_id: str,
        source_block_id: Optional[str] = None,
        target_block_id: Optional[str] = None,
        link_type: Optional[str] = None,
    ) -> NoteLink:
        """Create a link from this note to another (async)."""
        validate_id(note_id, "note")
        validate_id(target_note_id, "target_note")
        data = NoteLinkCreate(
            target_note_id=target_note_id,
            source_block_id=source_block_id,
            target_block_id=target_block_id,
            link_type=link_type,
        )
        response = await self._request(
            "POST", f"/notes/{note_id}/links", json=data.model_dump(exclude_none=True)
        )
        return NoteLink.model_validate(response)

    async def get_links(self, note_id: str) -> List[NoteLink]:
        """Get outgoing links from a note (async)."""
        validate_id(note_id, "note")
        response = await self._request("GET", f"/notes/{note_id}/links")
        return [NoteLink.model_validate(link) for link in response]

    async def get_backlinks(self, note_id: str) -> List[NoteLink]:
        """Get backlinks to a note (async)."""
        validate_id(note_id, "note")
        response = await self._request("GET", f"/notes/{note_id}/backlinks")
        return [NoteLink.model_validate(link) for link in response]

    async def remove_link(self, note_id: str, link_id: str) -> None:
        """Remove a link from a note (async)."""
        validate_id(note_id, "note")
        validate_id(link_id, "link")
        await self._request("DELETE", f"/notes/{note_id}/links/{link_id}")

    async def link_memory(
        self,
        note_id: str,
        memory_id: str,
        block_id: Optional[str] = None,
        link_type: Optional[str] = None,
        relevance_score: Optional[float] = None,
    ) -> NoteMemoryLink:
        """Link a memory to a note (async)."""
        validate_id(note_id, "note")
        validate_id(memory_id, "memory")
        data = NoteMemoryLinkCreate(
            memory_id=memory_id,
            block_id=block_id,
            link_type=link_type,
            relevance_score=relevance_score,
        )
        response = await self._request(
            "POST",
            f"/notes/{note_id}/memories",
            json=data.model_dump(exclude_none=True),
        )
        return NoteMemoryLink.model_validate(response)

    async def list_memories(self, note_id: str, limit: int = 50, offset: int = 0) -> NoteMemoryList:
        """List memories linked to a note (async)."""
        validate_id(note_id, "note")
        params: Dict[str, Any] = {"limit": limit, "offset": offset}
        response = await self._request("GET", f"/notes/{note_id}/memories", params=params)
        return NoteMemoryList.model_validate(response)

    async def unlink_memory(self, note_id: str, memory_id: str) -> None:
        """Unlink a memory from a note (async)."""
        validate_id(note_id, "note")
        validate_id(memory_id, "memory")
        await self._request("DELETE", f"/notes/{note_id}/memories/{memory_id}")

    async def get_daily(self, date: str) -> Note:
        """Get or create a daily note for a date (async)."""
        response = await self._request("GET", f"/notes/daily/{date}")
        return Note.model_validate(response)

    async def create_daily(self, date: Optional[str] = None) -> Note:
        """Create today's daily note (async)."""
        data: Dict[str, Any] = {}
        if date is not None:
            data["date"] = date
        response = await self._request("POST", "/notes/daily", json=data)
        return Note.model_validate(response)

    async def list_templates(self, limit: int = 20, offset: int = 0) -> NoteList:
        """List note templates (async)."""
        params: Dict[str, Any] = {"limit": limit, "offset": offset}
        response = await self._request("GET", "/notes/templates", params=params)
        return NoteList.model_validate(response)

    async def create_from_template(
        self,
        template_id: str,
        title: Optional[str] = None,
        space_id: Optional[str] = None,
        visibility: Optional[str] = None,
    ) -> Note:
        """Create a note from a template (async)."""
        validate_id(template_id, "template")
        data: Dict[str, Any] = {}
        if title is not None:
            data["title"] = title
        if space_id is not None:
            data["space_id"] = space_id
        if visibility is not None:
            data["visibility"] = visibility
        response = await self._request("POST", f"/notes/from-template/{template_id}", json=data)
        return Note.model_validate(response)

    async def summarize(self, note_id: str) -> Dict[str, Any]:
        """AI-summarize a note (async)."""
        validate_id(note_id, "note")
        return await self._request("POST", f"/notes/{note_id}/ai/summarize")

    async def extract_tasks(self, note_id: str) -> Dict[str, Any]:
        """AI-extract action items from a note (async)."""
        validate_id(note_id, "note")
        return await self._request("POST", f"/notes/{note_id}/ai/extract-tasks")

    async def suggest_links(self, note_id: str) -> Dict[str, Any]:
        """AI-suggest related notes to link (async)."""
        validate_id(note_id, "note")
        return await self._request("POST", f"/notes/{note_id}/ai/suggest-links")
