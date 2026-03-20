"""Async notes resource tests (ADR-065)."""

from unittest.mock import patch

import pytest

from trix import AsyncTrix
from trix.types.note import Note, NoteBlock, NoteList

NOW = "2026-03-20T00:00:00Z"

NOTE_DATA = {
    "id": "note-1",
    "account_id": "acc-1",
    "created_by": "user-1",
    "title": "Test Note",
    "note_type": "document",
    "visibility": "private",
    "version": 1,
    "blocks": [],
    "created_at": NOW,
    "updated_at": NOW,
}

BLOCK_DATA = {
    "id": "block-1",
    "note_id": "note-1",
    "block_type": "paragraph",
    "content": {"text": "Hello"},
    "sort_order": "a0",
    "created_at": NOW,
    "updated_at": NOW,
}


class TestAsyncNotesCreate:
    @pytest.mark.asyncio
    async def test_create(self):
        with patch.object(AsyncTrix, "_request") as mock_request:
            mock_request.return_value = NOTE_DATA
            client = AsyncTrix(api_key="test_key")

            note = await client.notes.create(title="Test Note")

            assert isinstance(note, Note)
            assert note.id == "note-1"
            assert note.title == "Test Note"
            call_args = mock_request.call_args
            assert call_args[0][0] == "POST"
            assert call_args[0][1] == "/notes"
            await client.close()


class TestAsyncNotesList:
    @pytest.mark.asyncio
    async def test_list(self):
        with patch.object(AsyncTrix, "_request") as mock_request:
            mock_request.return_value = {
                "notes": [NOTE_DATA],
                "pagination": {"total": 1},
            }
            client = AsyncTrix(api_key="test_key")

            result = await client.notes.list()

            assert isinstance(result, NoteList)
            await client.close()


class TestAsyncNotesGet:
    @pytest.mark.asyncio
    async def test_get(self):
        with patch.object(AsyncTrix, "_request") as mock_request:
            mock_request.return_value = NOTE_DATA
            client = AsyncTrix(api_key="test_key")

            note = await client.notes.get("note-1")

            assert isinstance(note, Note)
            assert note.id == "note-1"
            call_args = mock_request.call_args
            assert call_args[0] == ("GET", "/notes/note-1")
            await client.close()


class TestAsyncNotesUpdate:
    @pytest.mark.asyncio
    async def test_update(self):
        with patch.object(AsyncTrix, "_request") as mock_request:
            mock_request.return_value = {**NOTE_DATA, "title": "Updated"}
            client = AsyncTrix(api_key="test_key")

            note = await client.notes.update("note-1", version=1, title="Updated")

            assert note.title == "Updated"
            call_args = mock_request.call_args
            assert call_args[0] == ("PATCH", "/notes/note-1")
            await client.close()


class TestAsyncNotesDelete:
    @pytest.mark.asyncio
    async def test_delete(self):
        with patch.object(AsyncTrix, "_request") as mock_request:
            mock_request.return_value = None
            client = AsyncTrix(api_key="test_key")

            await client.notes.delete("note-1")

            call_args = mock_request.call_args
            assert call_args[0] == ("DELETE", "/notes/note-1")
            await client.close()


class TestAsyncNotesBlocks:
    @pytest.mark.asyncio
    async def test_add_block(self):
        with patch.object(AsyncTrix, "_request") as mock_request:
            mock_request.return_value = BLOCK_DATA
            client = AsyncTrix(api_key="test_key")

            block = await client.notes.add_block(
                "note-1", block_type="paragraph", content={"text": "Hello"}
            )

            assert isinstance(block, NoteBlock)
            assert block.id == "block-1"
            call_args = mock_request.call_args
            assert call_args[0] == ("POST", "/notes/note-1/blocks")
            await client.close()


class TestAsyncNotesDailyAndTemplates:
    @pytest.mark.asyncio
    async def test_get_daily(self):
        with patch.object(AsyncTrix, "_request") as mock_request:
            mock_request.return_value = NOTE_DATA
            client = AsyncTrix(api_key="test_key")

            note = await client.notes.get_daily("2026-03-20")

            assert isinstance(note, Note)
            call_args = mock_request.call_args
            assert call_args[0] == ("GET", "/notes/daily/2026-03-20")
            await client.close()

    @pytest.mark.asyncio
    async def test_list_templates(self):
        with patch.object(AsyncTrix, "_request") as mock_request:
            mock_request.return_value = {"notes": [], "pagination": {"total": 0}}
            client = AsyncTrix(api_key="test_key")

            result = await client.notes.list_templates()

            assert isinstance(result, NoteList)
            call_args = mock_request.call_args
            assert call_args[0] == ("GET", "/notes/templates")
            await client.close()
