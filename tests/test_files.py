"""Tests for FilesResource."""

from unittest.mock import Mock

from trix.resources.files import FilesResource

FILE_RESPONSE = {
    "id": "file_123",
    "filename": "photo.jpg",
    "content_type": "image/jpeg",
    "size_bytes": 102400,
    "status": "ready",
    "message_type": "image",
    "width": 1920,
    "height": 1080,
    "created_at": "2025-01-01T00:00:00Z",
}

FILE_LIST_RESPONSE = {
    "files": [FILE_RESPONSE],
    "has_more": False,
    "cursor": None,
}

DELETE_RESPONSE = {"deleted": True, "id": "file_123"}


class TestFilesUploadBase64:
    """Tests for files.upload_base64()."""

    def test_upload_base64(self):
        """Test uploading a file via base64."""
        mock_client = Mock()
        mock_client._request.return_value = FILE_RESPONSE

        resource = FilesResource(mock_client)
        result = resource.upload_base64(
            filename="photo.jpg",
            content_base64="aGVsbG8=",
            content_type="image/jpeg",
        )

        call_args = mock_client._request.call_args
        assert call_args[0] == ("POST", "/files/upload-base64")
        body = call_args[1]["json"]
        assert body["filename"] == "photo.jpg"
        assert body["content_base64"] == "aGVsbG8="
        assert body["content_type"] == "image/jpeg"
        assert result.id == "file_123"
        assert result.filename == "photo.jpg"

    def test_upload_base64_with_conversation(self):
        """Test uploading with conversation and message IDs."""
        mock_client = Mock()
        mock_client._request.return_value = FILE_RESPONSE

        resource = FilesResource(mock_client)
        resource.upload_base64(
            filename="photo.jpg",
            content_base64="aGVsbG8=",
            content_type="image/jpeg",
            conversation_id="conv_123",
            message_id="msg_456",
        )

        call_args = mock_client._request.call_args
        body = call_args[1]["json"]
        assert body["conversation_id"] == "conv_123"
        assert body["message_id"] == "msg_456"


class TestFilesGet:
    """Tests for files.get()."""

    def test_get_file_metadata(self):
        """Test getting file metadata by ID."""
        mock_client = Mock()
        mock_client._request.return_value = FILE_RESPONSE

        resource = FilesResource(mock_client)
        result = resource.get("file_123")

        call_args = mock_client._request.call_args
        assert call_args[0] == ("GET", "/files/file_123")
        assert result.id == "file_123"
        assert result.size_bytes == 102400
        assert result.content_type == "image/jpeg"


class TestFilesList:
    """Tests for files.list()."""

    def test_list_files(self):
        """Test listing files in a conversation."""
        mock_client = Mock()
        mock_client._request.return_value = FILE_LIST_RESPONSE

        resource = FilesResource(mock_client)
        result = resource.list("conv_123")

        call_args = mock_client._request.call_args
        assert call_args[0] == ("GET", "/files/conversation/conv_123")
        assert len(result.files) == 1
        assert result.files[0].id == "file_123"
        assert result.has_more is False

    def test_list_files_with_filters(self):
        """Test listing files with type filter and pagination."""
        mock_client = Mock()
        mock_client._request.return_value = FILE_LIST_RESPONSE

        resource = FilesResource(mock_client)
        resource.list("conv_123", type="image", limit=10, cursor="abc")

        call_args = mock_client._request.call_args
        params = call_args[1]["params"]
        assert params["type"] == "image"
        assert params["limit"] == 10
        assert params["cursor"] == "abc"


class TestFilesDelete:
    """Tests for files.delete()."""

    def test_delete_file(self):
        """Test soft-deleting a file."""
        mock_client = Mock()
        mock_client._request.return_value = DELETE_RESPONSE

        resource = FilesResource(mock_client)
        result = resource.delete("file_123")

        call_args = mock_client._request.call_args
        assert call_args[0] == ("DELETE", "/files/file_123")
        assert result["deleted"] is True
