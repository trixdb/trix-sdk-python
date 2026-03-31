"""Files resource for chat file management (ADR-068 Phase 4).

Example:
    # Upload a file
    file = client.files.upload(open("photo.jpg", "rb"), filename="photo.jpg")

    # Get download URL
    info = client.files.get_download_url(file.id)
    print(info.url)

    # List files in conversation
    result = client.files.list("conv-uuid", type="image")
"""

from pathlib import Path
from typing import Any, BinaryIO, Dict, Optional, Union

from ..types.file import (
    ChatFile,
    FileDownloadInfo,
    FileListResult,
    FileQuota,
    FileUploadBase64,
)
from ..utils.file_handling import prepare_file_upload
from ..utils.security import validate_id
from .base import BaseAsyncResource, BaseSyncResource


class FilesResource(BaseSyncResource):
    """Synchronous files resource."""

    def upload(
        self,
        file: Union[BinaryIO, Path, str],
        filename: Optional[str] = None,
        content_type: Optional[str] = None,
        conversation_id: Optional[str] = None,
        message_id: Optional[str] = None,
    ) -> ChatFile:
        """Upload a file via multipart form data."""
        with prepare_file_upload(
            file,
            default_filename="file",
            filename_override=filename,
            content_type_override=content_type,
        ) as (file_handle, fname, ctype):
            data: Dict[str, Any] = {}
            if conversation_id:
                data["conversation_id"] = conversation_id
            if message_id:
                data["message_id"] = message_id
            files: Dict[str, Any] = {"file": (fname, file_handle, ctype)}
            response = self._client._request_multipart(
                "POST", "/files/upload", data=data, files=files
            )
            return ChatFile.model_validate(response)

    def upload_base64(
        self,
        filename: str,
        content_base64: str,
        content_type: str,
        conversation_id: Optional[str] = None,
        message_id: Optional[str] = None,
    ) -> ChatFile:
        """Upload a file via base64-encoded JSON body."""
        body = FileUploadBase64(
            filename=filename,
            content_base64=content_base64,
            content_type=content_type,
            conversation_id=conversation_id,
            message_id=message_id,
        )
        response = self._request(
            "POST", "/files/upload-base64", json=body.model_dump(exclude_none=True)
        )
        return ChatFile.model_validate(response)

    def get(self, file_id: str) -> ChatFile:
        """Get file metadata by ID."""
        validate_id(file_id, "file")
        response = self._request("GET", f"/files/{file_id}")
        return ChatFile.model_validate(response)

    def get_download_url(self, file_id: str) -> FileDownloadInfo:
        """Get a signed download URL (1hr TTL)."""
        validate_id(file_id, "file")
        response = self._request("GET", f"/files/{file_id}/url")
        return FileDownloadInfo.model_validate(response)

    def delete(self, file_id: str) -> Dict[str, Any]:
        """Soft-delete a file. Releases storage quota."""
        validate_id(file_id, "file")
        return self._request("DELETE", f"/files/{file_id}")

    def list(
        self,
        conversation_id: str,
        type: Optional[str] = None,
        limit: Optional[int] = None,
        cursor: Optional[str] = None,
    ) -> FileListResult:
        """List files in a conversation."""
        validate_id(conversation_id, "conversation")
        params: Dict[str, Any] = {}
        if type:
            params["type"] = type
        if limit:
            params["limit"] = limit
        if cursor:
            params["cursor"] = cursor
        response = self._request(
            "GET", f"/files/conversation/{conversation_id}", params=params
        )
        return FileListResult.model_validate(response)

    def get_quota(self) -> FileQuota:
        """Get current storage quota usage."""
        response = self._request("GET", "/files/quota")
        return FileQuota.model_validate(response)


class AsyncFilesResource(BaseAsyncResource):
    """Asynchronous files resource."""

    async def upload_base64(
        self,
        filename: str,
        content_base64: str,
        content_type: str,
        conversation_id: Optional[str] = None,
        message_id: Optional[str] = None,
    ) -> ChatFile:
        """Upload a file via base64-encoded JSON body."""
        body = FileUploadBase64(
            filename=filename,
            content_base64=content_base64,
            content_type=content_type,
            conversation_id=conversation_id,
            message_id=message_id,
        )
        response = await self._request(
            "POST", "/files/upload-base64", json=body.model_dump(exclude_none=True)
        )
        return ChatFile.model_validate(response)

    async def get(self, file_id: str) -> ChatFile:
        """Get file metadata by ID."""
        validate_id(file_id, "file")
        response = await self._request("GET", f"/files/{file_id}")
        return ChatFile.model_validate(response)

    async def get_download_url(self, file_id: str) -> FileDownloadInfo:
        """Get a signed download URL (1hr TTL)."""
        validate_id(file_id, "file")
        response = await self._request("GET", f"/files/{file_id}/url")
        return FileDownloadInfo.model_validate(response)

    async def delete(self, file_id: str) -> Dict[str, Any]:
        """Soft-delete a file."""
        validate_id(file_id, "file")
        return await self._request("DELETE", f"/files/{file_id}")

    async def list(
        self,
        conversation_id: str,
        type: Optional[str] = None,
        limit: Optional[int] = None,
        cursor: Optional[str] = None,
    ) -> FileListResult:
        """List files in a conversation."""
        validate_id(conversation_id, "conversation")
        params: Dict[str, Any] = {}
        if type:
            params["type"] = type
        if limit:
            params["limit"] = limit
        if cursor:
            params["cursor"] = cursor
        response = await self._request(
            "GET", f"/files/conversation/{conversation_id}", params=params
        )
        return FileListResult.model_validate(response)

    async def get_quota(self) -> FileQuota:
        """Get current storage quota usage."""
        response = await self._request("GET", "/files/quota")
        return FileQuota.model_validate(response)
