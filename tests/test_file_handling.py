"""Tests for file handling utilities."""

import io
import json
import tempfile
from pathlib import Path


from trix.utils.file_handling import (
    FileHandle,
    build_multipart_data,
    infer_content_type,
    prepare_file_upload,
)


class TestInferContentType:
    """Tests for content type inference from file extensions."""

    def test_image_extensions(self):
        """Test common image extensions."""
        assert infer_content_type("photo.jpg") == "image/jpeg"
        assert infer_content_type("photo.jpeg") == "image/jpeg"
        assert infer_content_type("image.png") == "image/png"
        assert infer_content_type("anim.gif") == "image/gif"
        assert infer_content_type("photo.webp") == "image/webp"

    def test_audio_extensions(self):
        """Test common audio extensions."""
        assert infer_content_type("song.mp3") == "audio/mpeg"
        assert infer_content_type("clip.wav") == "audio/wav"
        assert infer_content_type("track.flac") == "audio/flac"
        assert infer_content_type("voice.ogg") == "audio/ogg"

    def test_video_extensions(self):
        """Test common video extensions."""
        assert infer_content_type("movie.mov") == "video/quicktime"
        assert infer_content_type("clip.avi") == "video/x-msvideo"
        assert infer_content_type("video.mkv") == "video/x-matroska"

    def test_unknown_extension_returns_default(self):
        """Test unknown extension returns default content type."""
        assert infer_content_type("file.xyz") == "application/octet-stream"
        assert infer_content_type("file.xyz", default="text/plain") == "text/plain"

    def test_none_filename_returns_default(self):
        """Test None filename returns default."""
        assert infer_content_type(None) == "application/octet-stream"

    def test_type_hint_image(self):
        """Test type_hint='image' uses image mapping."""
        assert infer_content_type("file.png", type_hint="image") == "image/png"
        # Unknown image ext falls back to image/jpeg
        assert infer_content_type("file.xyz", type_hint="image") == "image/jpeg"

    def test_type_hint_audio(self):
        """Test type_hint='audio' uses audio mapping."""
        assert infer_content_type("file.mp3", type_hint="audio") == "audio/mpeg"
        assert infer_content_type("file.xyz", type_hint="audio") == "audio/mpeg"

    def test_type_hint_video(self):
        """Test type_hint='video' uses video mapping."""
        assert infer_content_type("file.mov", type_hint="video") == "video/quicktime"
        assert infer_content_type("file.xyz", type_hint="video") == "video/mp4"

    def test_case_insensitive(self):
        """Test extension matching is case-insensitive."""
        assert infer_content_type("PHOTO.JPG") == "image/jpeg"
        assert infer_content_type("Song.MP3") == "audio/mpeg"


class TestFileHandle:
    """Tests for FileHandle context manager."""

    def test_with_file_path(self):
        """Test FileHandle with a file path string."""
        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as tmp:
            tmp.write(b"hello world")
            tmp_path = tmp.name

        with FileHandle(tmp_path) as (handle, filename):
            content = handle.read()
            assert content == b"hello world"
            assert filename == Path(tmp_path).name

        Path(tmp_path).unlink()

    def test_with_path_object(self):
        """Test FileHandle with a Path object."""
        with tempfile.NamedTemporaryFile(suffix=".dat", delete=False) as tmp:
            tmp.write(b"path object data")
            tmp_path = Path(tmp.name)

        with FileHandle(tmp_path) as (handle, filename):
            assert handle.read() == b"path object data"
            assert filename == tmp_path.name

        tmp_path.unlink()

    def test_with_bytes(self):
        """Test FileHandle with raw bytes."""
        data = b"raw byte content"
        with FileHandle(data, default_filename="upload.bin") as (handle, filename):
            assert handle.read() == b"raw byte content"
            assert filename == "upload.bin"

    def test_with_bytesio(self):
        """Test FileHandle with BytesIO object."""
        buf = io.BytesIO(b"buffer content")
        with FileHandle(buf, default_filename="buffer.dat") as (handle, filename):
            assert handle.read() == b"buffer content"
            assert filename == "buffer.dat"
        # BytesIO should NOT be closed by FileHandle
        assert not buf.closed

    def test_filename_override(self):
        """Test filename_override takes precedence."""
        data = b"test"
        with FileHandle(data, default_filename="default.txt", filename_override="custom.pdf") as (
            handle,
            filename,
        ):
            assert filename == "custom.pdf"

    def test_context_manager_cleanup_for_bytes(self):
        """Test BytesIO created from bytes is closed on exit."""
        data = b"test"
        fh = FileHandle(data)
        with fh as (handle, _):
            assert not handle.closed
        assert handle.closed

    def test_context_manager_cleanup_for_file_path(self):
        """Test file opened from path is closed on exit."""
        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as tmp:
            tmp.write(b"test")
            tmp_path = tmp.name

        fh = FileHandle(tmp_path)
        with fh as (handle, _):
            assert not handle.closed
        assert handle.closed

        Path(tmp_path).unlink()

    def test_external_handle_not_closed(self):
        """Test externally-provided file handle is not closed."""
        buf = io.BytesIO(b"external")
        fh = FileHandle(buf)
        with fh as (handle, _):
            pass
        assert not buf.closed


class TestPrepareFileUpload:
    """Tests for prepare_file_upload context manager."""

    def test_infers_content_type(self):
        """Test content type is inferred from filename."""
        data = b"image data"
        with prepare_file_upload(data, default_filename="photo.jpg") as (handle, name, ct):
            assert ct == "image/jpeg"
            assert name == "photo.jpg"

    def test_content_type_override(self):
        """Test content_type_override takes precedence."""
        data = b"data"
        with prepare_file_upload(
            data, default_filename="file.bin", content_type_override="text/csv"
        ) as (_, _, ct):
            assert ct == "text/csv"

    def test_type_hint_used(self):
        """Test type_hint is passed through to inference."""
        data = b"data"
        with prepare_file_upload(data, default_filename="file.xyz", type_hint="audio") as (
            _,
            _,
            ct,
        ):
            assert ct == "audio/mpeg"


class TestBuildMultipartData:
    """Tests for build_multipart_data function."""

    def test_empty_call(self):
        """Test calling with no arguments returns empty dict."""
        result = build_multipart_data()
        assert result == {}

    def test_base_data_copied(self):
        """Test base_data is copied, not mutated."""
        base = {"key": "value"}
        result = build_multipart_data(base_data=base, space_id="sp_1")
        assert result == {"key": "value", "space_id": "sp_1"}
        assert "space_id" not in base

    def test_tags_joined(self):
        """Test tags are joined with commas."""
        result = build_multipart_data(tags=["a", "b", "c"])
        assert result["tags"] == "a,b,c"

    def test_metadata_json_encoded(self):
        """Test metadata is JSON-encoded."""
        meta = {"source": "test", "count": 5}
        result = build_multipart_data(metadata=meta)
        assert json.loads(result["metadata"]) == meta

    def test_space_id_included(self):
        """Test space_id is included."""
        result = build_multipart_data(space_id="sp_abc")
        assert result["space_id"] == "sp_abc"

    def test_extra_fields(self):
        """Test extra keyword arguments are included."""
        result = build_multipart_data(title="My File", description="A test")
        assert result["title"] == "My File"
        assert result["description"] == "A test"

    def test_none_extra_fields_excluded(self):
        """Test None extra fields are excluded."""
        result = build_multipart_data(title="present", subtitle=None)
        assert "title" in result
        assert "subtitle" not in result

    def test_bool_extra_fields_converted(self):
        """Test boolean extra fields are converted to strings."""
        result = build_multipart_data(public=True, draft=False)
        assert result["public"] == "true"
        assert result["draft"] == "false"

    def test_numeric_extra_fields_converted(self):
        """Test numeric extra fields are converted to strings."""
        result = build_multipart_data(count=42)
        assert result["count"] == "42"
