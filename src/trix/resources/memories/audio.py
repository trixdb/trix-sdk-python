"""Audio operations mixin for memories resource.

Provides audio upload, transcription, and streaming operations.
"""

from pathlib import Path
from typing import Any, AsyncIterator, BinaryIO, Dict, Iterator, List, Optional, Union

from ...types import Memory, Transcript
from ...utils.file_handling import build_multipart_data, prepare_file_upload
from ...utils.security import validate_id
from .base import build_transcribe_body


class AudioOperationsMixin:
    """Mixin providing audio operations for sync memories resource."""

    _client: Any  # Type hint for the client

    def stream_audio(self, id: str) -> bytes:
        """Get audio content for an audio memory."""
        validate_id(id, "memory")
        return self._client._request_raw("GET", f"/memories/{id}/audio")

    def stream_audio_chunks(self, id: str, chunk_size: int = 8192) -> Iterator[bytes]:
        """Stream audio content in chunks for efficient memory usage."""
        validate_id(id, "memory")
        return self._client._request_stream("GET", f"/memories/{id}/audio", chunk_size=chunk_size)

    def create_with_audio(
        self,
        audio_file: Union[BinaryIO, Path, str],
        filename: Optional[str] = None,
        content_type: str = "audio/mpeg",
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        space_id: Optional[str] = None,
        transcribe: bool = True,
        language: Optional[str] = None,
    ) -> Memory:
        """Create a memory from an audio or video file."""
        with prepare_file_upload(
            audio_file,
            default_filename="audio",
            filename_override=filename,
            content_type_override=content_type,
            type_hint="audio",
        ) as (file_handle, fname, ctype):
            data = build_multipart_data(
                base_data={"type": "audio"},
                tags=tags,
                metadata=metadata,
                space_id=space_id,
                transcribe=transcribe,
                language=language,
            )
            files: Dict[str, Any] = {"file": (fname, file_handle, ctype)}
            response = self._client._request_multipart("POST", "/memories", data=data, files=files)
            return Memory.model_validate(response)

    def get_transcript(self, id: str) -> Transcript:
        """Get transcript for an audio memory."""
        validate_id(id, "memory")
        response = self._client._request("GET", f"/memories/{id}/transcript")
        return Transcript.model_validate(response)

    def transcribe(
        self,
        id: str,
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
        """Transcribe or re-transcribe an audio memory with advanced options."""
        validate_id(id, "memory")
        body = build_transcribe_body(
            language=language,
            prompt=prompt,
            provider=provider,
            enable_speaker_diarization=enable_speaker_diarization,
            enable_entity_detection=enable_entity_detection,
            enable_content_safety=enable_content_safety,
            enable_auto_chapters=enable_auto_chapters,
            enable_auto_summarization=enable_auto_summarization,
            speakers_expected=speakers_expected,
        )
        response = self._client._request("POST", f"/memories/{id}/transcribe", json=body)
        return dict(response)


class AsyncAudioOperationsMixin:
    """Mixin providing audio operations for async memories resource."""

    _client: Any  # Type hint for the client

    async def stream_audio(self, id: str) -> bytes:
        """Get audio content for an audio memory (async)."""
        validate_id(id, "memory")
        return await self._client._request_raw("GET", f"/memories/{id}/audio")

    async def stream_audio_chunks(self, id: str, chunk_size: int = 8192) -> AsyncIterator[bytes]:
        """Stream audio content in chunks for efficient memory usage (async)."""
        validate_id(id, "memory")
        stream = self._client._request_stream("GET", f"/memories/{id}/audio", chunk_size=chunk_size)
        async for chunk in stream:
            yield chunk

    async def create_with_audio(
        self,
        audio_file: Union[BinaryIO, Path, str],
        filename: Optional[str] = None,
        content_type: str = "audio/mpeg",
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        space_id: Optional[str] = None,
        transcribe: bool = True,
        language: Optional[str] = None,
    ) -> Memory:
        """Create a memory from an audio or video file (async)."""
        with prepare_file_upload(
            audio_file,
            default_filename="audio",
            filename_override=filename,
            content_type_override=content_type,
            type_hint="audio",
        ) as (file_handle, fname, ctype):
            data = build_multipart_data(
                base_data={"type": "audio"},
                tags=tags,
                metadata=metadata,
                space_id=space_id,
                transcribe=transcribe,
                language=language,
            )
            files: Dict[str, Any] = {"file": (fname, file_handle, ctype)}
            response = await self._client._request_multipart(
                "POST", "/memories", data=data, files=files
            )
            return Memory.model_validate(response)

    async def get_transcript(self, id: str) -> Transcript:
        """Get transcript for an audio memory (async)."""
        validate_id(id, "memory")
        response = await self._client._request("GET", f"/memories/{id}/transcript")
        return Transcript.model_validate(response)

    async def transcribe(
        self,
        id: str,
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
        """Transcribe or re-transcribe an audio memory with advanced options (async)."""
        validate_id(id, "memory")
        body = build_transcribe_body(
            language=language,
            prompt=prompt,
            provider=provider,
            enable_speaker_diarization=enable_speaker_diarization,
            enable_entity_detection=enable_entity_detection,
            enable_content_safety=enable_content_safety,
            enable_auto_chapters=enable_auto_chapters,
            enable_auto_summarization=enable_auto_summarization,
            speakers_expected=speakers_expected,
        )
        response = await self._client._request("POST", f"/memories/{id}/transcribe", json=body)
        return dict(response)
