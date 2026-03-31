"""Tests for Notes resource."""

from unittest.mock import Mock

from trix.resources.notes import NotesResource

NOTE_RESPONSE = {
    "id": "note_123",
    "account_id": "acc_1",
    "created_by": "user_1",
    "title": "Meeting Notes",
    "note_type": "document",
    "visibility": "private",
    "version": 1,
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z",
}

BLOCK_RESPONSE = {
    "id": "block_456",
    "note_id": "note_123",
    "block_type": "paragraph",
    "content": {"text": "Discussion points..."},
    "sort_order": "a0",
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z",
}


class TestNotesResource:
    """Tests for NotesResource (sync)."""

    def test_create_note(self):
        """Test creating a note."""
        mock_client = Mock()
        mock_client._request.return_value = NOTE_RESPONSE

        resource = NotesResource(mock_client)
        result = resource.create(title="Meeting Notes", note_type="document")

        call_args = mock_client._request.call_args
        assert call_args[0] == ("POST", "/notes")
        assert result.id == "note_123"
        assert result.title == "Meeting Notes"

    def test_list_notes(self):
        """Test listing notes."""
        mock_client = Mock()
        mock_client._request.return_value = {
            "notes": [NOTE_RESPONSE],
            "total": 1,
            "limit": 20,
            "offset": 0,
        }

        resource = NotesResource(mock_client)
        result = resource.list()

        call_args = mock_client._request.call_args
        assert call_args[0] == ("GET", "/notes")
        assert len(result.notes) == 1

    def test_list_notes_with_filter(self):
        """Test listing notes filtered by type."""
        mock_client = Mock()
        mock_client._request.return_value = {
            "notes": [],
            "total": 0,
            "limit": 20,
            "offset": 0,
        }

        resource = NotesResource(mock_client)
        resource.list(note_type="document")

        call_args = mock_client._request.call_args
        assert call_args[1]["params"]["noteType"] == "document"

    def test_get_note(self):
        """Test getting a note by ID."""
        mock_client = Mock()
        mock_client._request.return_value = NOTE_RESPONSE

        resource = NotesResource(mock_client)
        result = resource.get("note_123")

        call_args = mock_client._request.call_args
        assert call_args[0] == ("GET", "/notes/note_123")
        assert result.id == "note_123"

    def test_update_note(self):
        """Test updating a note."""
        mock_client = Mock()
        mock_client._request.return_value = {
            **NOTE_RESPONSE,
            "title": "Updated Notes",
            "version": 2,
        }

        resource = NotesResource(mock_client)
        result = resource.update("note_123", version=1, title="Updated Notes")

        call_args = mock_client._request.call_args
        assert call_args[0] == ("PATCH", "/notes/note_123")
        assert result.title == "Updated Notes"

    def test_delete_note(self):
        """Test deleting a note."""
        mock_client = Mock()
        mock_client._request.return_value = None

        resource = NotesResource(mock_client)
        resource.delete("note_123")

        call_args = mock_client._request.call_args
        assert call_args[0] == ("DELETE", "/notes/note_123")

    def test_add_block(self):
        """Test adding a block to a note."""
        mock_client = Mock()
        mock_client._request.return_value = BLOCK_RESPONSE

        resource = NotesResource(mock_client)
        result = resource.add_block(
            "note_123",
            block_type="paragraph",
            content={"text": "Discussion points..."},
        )

        call_args = mock_client._request.call_args
        assert call_args[0] == ("POST", "/notes/note_123/blocks")
        assert result.block_type == "paragraph"

    def test_update_block(self):
        """Test updating a block in a note."""
        mock_client = Mock()
        mock_client._request.return_value = {
            **BLOCK_RESPONSE,
            "content": {"text": "Updated content"},
        }

        resource = NotesResource(mock_client)
        resource.update_block("note_123", "block_456", content={"text": "Updated content"})

        call_args = mock_client._request.call_args
        assert call_args[0] == ("PATCH", "/notes/note_123/blocks/block_456")

    def test_delete_block(self):
        """Test deleting a block from a note."""
        mock_client = Mock()
        mock_client._request.return_value = None

        resource = NotesResource(mock_client)
        resource.delete_block("note_123", "block_456")

        call_args = mock_client._request.call_args
        assert call_args[0] == ("DELETE", "/notes/note_123/blocks/block_456")

    def test_create_link(self):
        """Test creating a link between notes."""
        mock_client = Mock()
        mock_client._request.return_value = {
            "id": "link_789",
            "source_note_id": "note_123",
            "target_note_id": "note_456",
            "link_type": "reference",
            "created_at": "2024-01-01T00:00:00Z",
        }

        resource = NotesResource(mock_client)
        resource.create_link("note_123", target_note_id="note_456")

        call_args = mock_client._request.call_args
        assert call_args[0] == ("POST", "/notes/note_123/links")

    def test_get_daily(self):
        """Test getting a daily note."""
        mock_client = Mock()
        mock_client._request.return_value = NOTE_RESPONSE

        resource = NotesResource(mock_client)
        result = resource.get_daily("2024-01-15")

        call_args = mock_client._request.call_args
        assert call_args[0] == ("GET", "/notes/daily/2024-01-15")
        assert result.id == "note_123"
