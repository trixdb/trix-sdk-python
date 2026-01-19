"""File handling utilities for Trix SDK.

Provides reusable utilities for handling file uploads, content type inference,
and file input normalization across different resource modules.
"""

import io
from contextlib import contextmanager
from pathlib import Path
from typing import Any, BinaryIO, Dict, Iterator, Optional, Tuple, Union


# Content type mappings for common file extensions
IMAGE_CONTENT_TYPES = {
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png": "image/png",
    ".gif": "image/gif",
    ".webp": "image/webp",
    ".bmp": "image/bmp",
    ".tiff": "image/tiff",
    ".tif": "image/tiff",
}

AUDIO_CONTENT_TYPES = {
    ".mp3": "audio/mpeg",
    ".mp4": "audio/mp4",
    ".m4a": "audio/mp4",
    ".wav": "audio/wav",
    ".webm": "audio/webm",
    ".ogg": "audio/ogg",
    ".flac": "audio/flac",
    ".aac": "audio/aac",
}

VIDEO_CONTENT_TYPES = {
    ".mp4": "video/mp4",
    ".webm": "video/webm",
    ".mov": "video/quicktime",
    ".avi": "video/x-msvideo",
    ".mkv": "video/x-matroska",
    ".flv": "video/x-flv",
    ".mpeg": "video/mpeg",
}


def infer_content_type(
    filename: Optional[str],
    default: str = "application/octet-stream",
    type_hint: Optional[str] = None,
) -> str:
    """Infer content type from filename extension.

    Args:
        filename: Filename to extract extension from
        default: Default content type if extension not recognized
        type_hint: Hint for type category ("image", "audio", "video")

    Returns:
        Inferred MIME type string
    """
    if not filename:
        return default

    ext = Path(filename).suffix.lower()

    # Check based on type hint first
    if type_hint == "image":
        return IMAGE_CONTENT_TYPES.get(ext, "image/jpeg")
    elif type_hint == "audio":
        return AUDIO_CONTENT_TYPES.get(ext, "audio/mpeg")
    elif type_hint == "video":
        return VIDEO_CONTENT_TYPES.get(ext, "video/mp4")

    # Check all mappings
    if ext in IMAGE_CONTENT_TYPES:
        return IMAGE_CONTENT_TYPES[ext]
    if ext in AUDIO_CONTENT_TYPES:
        return AUDIO_CONTENT_TYPES[ext]
    if ext in VIDEO_CONTENT_TYPES:
        return VIDEO_CONTENT_TYPES[ext]

    return default


class FileHandle:
    """Context manager for handling various file input types.

    Normalizes different input types (path, bytes, file object) into
    a consistent file handle interface with automatic cleanup.
    """

    def __init__(
        self,
        file_input: Union[BinaryIO, Path, str, bytes],
        default_filename: str = "file",
        filename_override: Optional[str] = None,
    ) -> None:
        """Initialize file handle.

        Args:
            file_input: File as path, bytes, or file object
            default_filename: Default filename if none can be extracted
            filename_override: Override the filename
        """
        self._input = file_input
        self._default_filename = default_filename
        self._filename_override = filename_override
        self._handle: Optional[BinaryIO] = None
        self._should_close = False

    @property
    def filename(self) -> str:
        """Get the filename for this file."""
        if self._filename_override:
            return self._filename_override

        if isinstance(self._input, (str, Path)):
            return Path(self._input).name
        return self._default_filename

    def __enter__(self) -> Tuple[BinaryIO, str]:
        """Enter context and return file handle and filename."""
        if isinstance(self._input, bytes):
            self._handle = io.BytesIO(self._input)
            self._should_close = True
        elif isinstance(self._input, (str, Path)):
            self._handle = open(Path(self._input), "rb")
            self._should_close = True
        else:
            self._handle = self._input
            self._should_close = False

        return self._handle, self.filename

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Exit context and cleanup."""
        if self._should_close and self._handle:
            self._handle.close()


@contextmanager
def prepare_file_upload(
    file_input: Union[BinaryIO, Path, str, bytes],
    default_filename: str = "file",
    filename_override: Optional[str] = None,
    content_type_override: Optional[str] = None,
    type_hint: Optional[str] = None,
) -> Iterator[Tuple[BinaryIO, str, str]]:
    """Prepare a file for upload with automatic content type inference.

    Context manager that handles file opening, content type inference,
    and cleanup.

    Args:
        file_input: File as path, bytes, or file object
        default_filename: Default filename if none can be extracted
        filename_override: Override the filename
        content_type_override: Override the content type
        type_hint: Hint for content type inference ("image", "audio", "video")

    Yields:
        Tuple of (file_handle, filename, content_type)

    Example:
        >>> with prepare_file_upload("photo.jpg", type_hint="image") as (fh, name, ct):
        ...     files = {"file": (name, fh, ct)}
        ...     response = client.upload(files=files)
    """
    with FileHandle(file_input, default_filename, filename_override) as (handle, filename):
        if content_type_override:
            content_type = content_type_override
        else:
            content_type = infer_content_type(filename, type_hint=type_hint)
        yield handle, filename, content_type


def build_multipart_data(
    base_data: Optional[Dict[str, Any]] = None,
    tags: Optional[list] = None,
    metadata: Optional[Dict[str, Any]] = None,
    space_id: Optional[str] = None,
    **extra_fields: Any,
) -> Dict[str, Any]:
    """Build form data for multipart uploads.

    Args:
        base_data: Base data dictionary to extend
        tags: List of tags to join with commas
        metadata: Metadata dict to JSON encode
        space_id: Space ID
        **extra_fields: Additional fields to include

    Returns:
        Dictionary suitable for multipart form data
    """
    import json

    data: Dict[str, Any] = base_data.copy() if base_data else {}

    if tags:
        data["tags"] = ",".join(tags)
    if metadata:
        data["metadata"] = json.dumps(metadata)
    if space_id:
        data["space_id"] = space_id

    for key, value in extra_fields.items():
        if value is not None:
            if isinstance(value, bool):
                data[key] = "true" if value else "false"
            else:
                data[key] = str(value) if not isinstance(value, str) else value

    return data
