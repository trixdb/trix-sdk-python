"""Memories resource for Trix SDK."""

import json
from pathlib import Path
from typing import (
    TYPE_CHECKING,
    Any,
    AsyncIterator,
    BinaryIO,
    Dict,
    Iterator,
    List,
    Optional,
    Union,
)

from ..protocols import AsyncClientProtocol, SyncClientProtocol
from ..types import (
    AutoTagResult,
    BatchAutoTagResult,
    BulkResult,
    DuplicateCheckResult,
    ImageClusterResult,
    Memory,
    MemoryConfig,
    MemoryCreate,
    MemoryList,
    MemoryOptions,
    MemoryType,
    MemoryUpdate,
    QuerySuggestionsResult,
    SearchMode,
    VisualSearchResults,
)
from ..utils.pagination import AsyncPaginator, SyncPaginator
from ..utils.security import validate_id

if TYPE_CHECKING:
    from ..types import MemoryStats


class MemoriesResource:
    """Resource for managing memories."""

    def __init__(self, client: SyncClientProtocol) -> None:
        """Initialize memories resource with client."""
        self._client = client

    def create(
        self,
        content: str,
        type: Optional[MemoryType] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        priority: Optional[int] = None,
        space_id: Optional[str] = None,
        options: Optional[Dict[str, Any]] = None,
        is_pinned: bool = False,
        protection_level: str = "none",
    ) -> Memory:
        """
        Create a new memory.

        Args:
            content: The content of the memory
            type: Type of memory (text, markdown, url, audio)
            tags: List of tags for categorization
            metadata: Additional metadata
            priority: Priority level for the memory
            space_id: ID of the space to add memory to
            options: Additional options (transcribe_audio, language, skip_embedding)
            is_pinned: Whether to pin the memory (prevents decay)
            protection_level: Protection level ("none", "soft", "hard")

        Returns:
            Created memory object

        Example:
            >>> memory = client.memories.create(
            ...     content="Important information",
            ...     tags=["work", "important"],
            ...     metadata={"source": "meeting"},
            ...     is_pinned=True,
            ...     protection_level="soft"
            ... )
        """
        data = MemoryCreate(
            content=content,
            type=type or MemoryType.TEXT,
            tags=tags,
            metadata=metadata,
            priority=priority,
            space_id=space_id,
            options=MemoryOptions(**options) if options else None,
            is_pinned=is_pinned if is_pinned else None,
            protection_level=protection_level if protection_level != "none" else None,
        )
        response = self._client._request(
            "POST", "/memories", json=data.model_dump(exclude_none=True)
        )
        return Memory.model_validate(response)

    def list(
        self,
        q: Optional[str] = None,
        mode: Optional[SearchMode] = None,
        limit: int = 100,
        offset: int = 0,
        tags: Optional[List[str]] = None,
        space_id: Optional[str] = None,
        pinned: Optional[bool] = None,
        protected: Optional[bool] = None,
        min_quality: Optional[float] = None,
        include_deleted: bool = False,
    ) -> MemoryList:
        """
        List memories with optional filtering.

        Args:
            q: Search query
            mode: Search mode (semantic, keyword, hybrid)
            limit: Maximum number of results
            offset: Offset for pagination
            tags: Filter by tags
            space_id: Filter by space
            pinned: Filter by pinned status (True=only pinned, False=only unpinned)
            protected: Filter by protection status (True=any protection, False=none)
            min_quality: Minimum quality score (0-1)
            include_deleted: Include soft-deleted memories

        Returns:
            List of memories with pagination info

        Example:
            >>> results = client.memories.list(
            ...     q="important",
            ...     mode=SearchMode.HYBRID,
            ...     tags=["work"],
            ...     pinned=True,
            ...     min_quality=0.5
            ... )
        """
        params: Dict[str, Any] = {"limit": limit, "offset": offset}
        if q:
            params["q"] = q
        if mode:
            params["mode"] = mode.value
        if tags:
            params["tags"] = ",".join(tags)
        if space_id:
            params["space_id"] = space_id
        if pinned is not None:
            params["pinned"] = "true" if pinned else "false"
        if protected is not None:
            params["protected"] = "true" if protected else "false"
        if min_quality is not None:
            params["min_quality"] = str(min_quality)
        if include_deleted:
            params["include_deleted"] = "true"

        response = self._client._request("GET", "/memories", params=params)
        return MemoryList.model_validate(response)

    def iter(
        self,
        q: Optional[str] = None,
        mode: Optional[SearchMode] = None,
        tags: Optional[List[str]] = None,
        space_id: Optional[str] = None,
        page_size: int = 100,
        max_items: Optional[int] = None,
    ) -> Iterator[Memory]:
        """
        Iterate through all memories with automatic pagination.

        Args:
            q: Search query
            mode: Search mode
            tags: Filter by tags
            space_id: Filter by space
            page_size: Number of items per page
            max_items: Maximum total items to fetch

        Yields:
            Memory objects

        Example:
            >>> for memory in client.memories.iter(tags=["work"]):
            ...     print(memory.content)
        """
        params: Dict[str, Any] = {}
        if q:
            params["q"] = q
        if mode:
            params["mode"] = mode.value
        if tags:
            params["tags"] = ",".join(tags)
        if space_id:
            params["space_id"] = space_id

        paginator = SyncPaginator(
            self.list,
            initial_params=params,
            limit=page_size,
            max_items=max_items,
        )
        for item in paginator:
            yield Memory.model_validate(item)

    def get(self, id: str) -> Memory:
        """
        Get a memory by ID.

        Args:
            id: Memory ID

        Returns:
            Memory object

        Example:
            >>> memory = client.memories.get("mem_123")
        """
        validate_id(id, "memory")
        response = self._client._request("GET", f"/memories/{id}")
        return Memory.model_validate(response)

    def update(
        self,
        id: str,
        content: Optional[str] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        priority: Optional[int] = None,
    ) -> Memory:
        """
        Update a memory.

        Args:
            id: Memory ID
            content: New content
            tags: New tags
            metadata: New metadata
            priority: New priority

        Returns:
            Updated memory object

        Example:
            >>> memory = client.memories.update(
            ...     "mem_123",
            ...     tags=["updated", "important"]
            ... )
        """
        validate_id(id, "memory")
        data = MemoryUpdate(
            content=content,
            tags=tags,
            metadata=metadata,
            priority=priority,
        )
        response = self._client._request(
            "PATCH", f"/memories/{id}", json=data.model_dump(exclude_none=True)
        )
        return Memory.model_validate(response)

    def delete(self, id: str) -> None:
        """
        Delete a memory.

        Args:
            id: Memory ID

        Example:
            >>> client.memories.delete("mem_123")
        """
        validate_id(id, "memory")
        self._client._request("DELETE", f"/memories/{id}")

    def bulk_create(self, memories: List[MemoryCreate]) -> BulkResult:
        """
        Create multiple memories at once.

        Args:
            memories: List of memory creation requests

        Returns:
            Bulk operation result with success/failure counts

        Example:
            >>> result = client.memories.bulk_create([
            ...     MemoryCreate(content="First memory"),
            ...     MemoryCreate(content="Second memory"),
            ... ])
            >>> print(f"Created {result.success} memories, {result.failed} failed")
        """
        data = [m.model_dump(exclude_none=True) for m in memories]
        response = self._client._request("POST", "/memories/bulk", json={"memories": data})
        return BulkResult.model_validate(response)

    def bulk_update(self, updates: List[Dict[str, Any]]) -> BulkResult:
        """
        Update multiple memories at once.

        Args:
            updates: List of update objects with 'id' and update fields

        Returns:
            Bulk operation result with success/failure counts

        Example:
            >>> result = client.memories.bulk_update([
            ...     {"id": "mem_123", "tags": ["updated"]},
            ...     {"id": "mem_456", "priority": 5},
            ... ])
            >>> print(f"Updated {result.success} memories, {result.failed} failed")
        """
        # Validate all IDs before making the request
        for i, update in enumerate(updates):
            if "id" not in update:
                raise ValueError(f"Update at index {i} is missing an 'id'")
            validate_id(update["id"], f"memory[{i}]")
        response = self._client._request("PATCH", "/memories/bulk", json={"updates": updates})
        return BulkResult.model_validate(response)

    def bulk_delete(self, ids: List[str]) -> BulkResult:
        """
        Delete multiple memories at once.

        Args:
            ids: List of memory IDs to delete

        Returns:
            Bulk operation result with success/failure counts

        Example:
            >>> result = client.memories.bulk_delete(["mem_123", "mem_456"])
            >>> print(f"Deleted {result.success} memories, {result.failed} failed")
        """
        # Validate all IDs before making the request
        for i, item_id in enumerate(ids):
            validate_id(item_id, f"memory[{i}]")
        response = self._client._request("DELETE", "/memories/bulk", json={"ids": ids})
        return BulkResult.model_validate(response)

    def get_config(self) -> MemoryConfig:
        """
        Get memory system configuration.

        Returns:
            Memory configuration

        Example:
            >>> config = client.memories.get_config()
            >>> print(config.max_content_length)
        """
        response = self._client._request("GET", "/memories/config")
        return MemoryConfig.model_validate(response)

    def stream_audio(self, id: str) -> bytes:
        """
        Get audio content for an audio memory.

        Args:
            id: Memory ID

        Returns:
            Audio data as bytes

        Example:
            >>> audio_data = client.memories.stream_audio("mem_123")
        """
        validate_id(id, "memory")
        return self._client._request_raw("GET", f"/memories/{id}/audio")

    def stream_audio_chunks(self, id: str, chunk_size: int = 8192) -> Iterator[bytes]:
        """
        Stream audio content in chunks for efficient memory usage.

        Args:
            id: Memory ID
            chunk_size: Size of each chunk in bytes

        Yields:
            Chunks of audio data

        Example:
            >>> with open("audio.mp3", "wb") as f:
            ...     for chunk in client.memories.stream_audio_chunks("mem_123"):
            ...         f.write(chunk)
        """
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
        """
        Create a memory from an audio or video file.

        Supports audio formats: mp3, mp4, m4a, wav, webm, ogg, flac, aac
        Supports video formats: mp4, webm, mov, avi, mkv, flv, mpeg

        For advanced transcription options (speaker diarization, entity detection,
        chapters, etc.), use the transcribe() method after upload.

        Args:
            audio_file: File object, path, or string path to the audio/video file
            filename: Override filename (default: extracted from path or "audio")
            content_type: MIME type (e.g., 'audio/mpeg', 'video/mp4')
            tags: List of tags for categorization
            metadata: Additional metadata
            space_id: ID of the space to add memory to
            transcribe: Whether to transcribe the audio/video automatically
            language: Language code for transcription (e.g., 'en', 'es')

        Returns:
            Created memory object

        Example:
            >>> # Upload audio file
            >>> memory = client.memories.create_with_audio(
            ...     "recording.mp3",
            ...     tags=["meeting", "important"],
            ...     transcribe=True
            ... )
            >>>
            >>> # Upload video file with transcription
            >>> memory = client.memories.create_with_audio(
            ...     "meeting.mp4",
            ...     content_type="video/mp4",
            ...     transcribe=True,
            ...     language="en"
            ... )
        """
        # Handle different input types
        file_handle: BinaryIO
        if isinstance(audio_file, (str, Path)):
            path = Path(audio_file)
            filename = filename or path.name
            file_handle = open(path, "rb")
            should_close = True
        else:
            filename = filename or "audio"
            file_handle = audio_file
            should_close = False

        try:
            # Build form data
            data: Dict[str, Any] = {"type": "audio"}
            if tags:
                data["tags"] = ",".join(tags)
            if metadata:
                data["metadata"] = json.dumps(metadata)
            if space_id:
                data["space_id"] = space_id
            if transcribe:
                data["transcribe"] = "true"
            if language:
                data["language"] = language

            files: Dict[str, Any] = {"file": (filename, file_handle, content_type)}

            response = self._client._request_multipart("POST", "/memories", data=data, files=files)
            return Memory.model_validate(response)
        finally:
            if should_close:
                file_handle.close()

    def get_transcript(self, id: str) -> "Transcript":
        """
        Get transcript for an audio memory.

        Args:
            id: Memory ID

        Returns:
            Full transcript with metadata, segments, entities, and chapters

        Example:
            >>> transcript = client.memories.get_transcript("mem_123")
            >>> print(transcript.text)  # Full transcript text
            >>> print(transcript.summary)  # Auto-generated summary
            >>> for segment in transcript.segments or []:
            ...     print(f"{segment.speaker}: {segment.text}")
        """
        validate_id(id, "memory")
        response = self._client._request("GET", f"/memories/{id}/transcript")
        from ..types import Transcript
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
    ) -> "Job":
        """
        Transcribe or re-transcribe an audio memory with advanced options.

        Args:
            id: Memory ID
            language: Language code for transcription (e.g., 'en', 'es')
            prompt: Context to improve transcription accuracy
            provider: Transcription provider ('assemblyai' or 'openai')
            enable_speaker_diarization: Enable speaker identification and labeling
            enable_entity_detection: Enable entity detection in transcript
            enable_content_safety: Enable content safety labeling
            enable_auto_chapters: Enable automatic chapter generation
            enable_auto_summarization: Enable automatic summarization
            speakers_expected: Expected number of speakers (hint for diarization)

        Returns:
            Job object for tracking transcription progress

        Example:
            >>> # Basic transcription
            >>> job = client.memories.transcribe("mem_123", language="en")
            >>> print(f"Transcription status: {job.status}")
            >>>
            >>> # Advanced transcription with speaker diarization
            >>> job = client.memories.transcribe(
            ...     "mem_123",
            ...     provider="assemblyai",
            ...     enable_speaker_diarization=True,
            ...     speakers_expected=2,
            ...     enable_auto_chapters=True
            ... )
            >>> # Poll for completion or use webhooks
            >>> print(f"Job ID: {job.id}, Progress: {job.progress}%")
        """
        validate_id(id, "memory")
        body: Dict[str, Any] = {}
        if language:
            body["language"] = language
        if prompt:
            body["prompt"] = prompt
        if provider:
            body["provider"] = provider
        if enable_speaker_diarization is not None:
            body["enableSpeakerDiarization"] = enable_speaker_diarization
        if enable_entity_detection is not None:
            body["enableEntityDetection"] = enable_entity_detection
        if enable_content_safety is not None:
            body["enableContentSafety"] = enable_content_safety
        if enable_auto_chapters is not None:
            body["enableAutoChapters"] = enable_auto_chapters
        if enable_auto_summarization is not None:
            body["enableAutoSummarization"] = enable_auto_summarization
        if speakers_expected is not None:
            body["speakersExpected"] = speakers_expected

        response = self._client._request("POST", f"/memories/{id}/transcribe", json=body)
        from ..types import Job
        return Job.model_validate(response)

    def get_stats(
        self,
        space_id: Optional[str] = None,
        created_after: Optional[str] = None,
        created_before: Optional[str] = None,
        include_type_distribution: bool = False,
        include_tag_distribution: bool = False,
        include_timeline: bool = False,
        timeline_granularity: Optional[str] = None,
    ) -> "MemoryStats":
        """
        Get memory statistics.

        Args:
            space_id: Filter by space ID
            created_after: Filter by creation date (ISO format)
            created_before: Filter by creation date (ISO format)
            include_type_distribution: Include type distribution in stats
            include_tag_distribution: Include tag distribution in stats
            include_timeline: Include timeline in stats
            timeline_granularity: Timeline granularity (hour, day, week, month)

        Returns:
            Memory statistics

        Example:
            >>> stats = client.memories.get_stats(include_type_distribution=True)
            >>> print(f"Total memories: {stats.total}")
        """
        from ..types import MemoryStats

        params: Dict[str, Any] = {}
        if space_id:
            params["space_id"] = space_id
        if created_after:
            params["created_after"] = created_after
        if created_before:
            params["created_before"] = created_before
        if include_type_distribution:
            params["include_type_distribution"] = "true"
        if include_tag_distribution:
            params["include_tag_distribution"] = "true"
        if include_timeline:
            params["include_timeline"] = "true"
        if timeline_granularity:
            params["timeline_granularity"] = timeline_granularity

        response = self._client._request("GET", "/memories/stats", params=params)
        return MemoryStats.model_validate(response)

    def link_resource(
        self,
        id: str,
        resource_id: str,
        relationship_type: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Link a resource to a memory.

        Args:
            id: Memory ID
            resource_id: Resource ID to link
            relationship_type: Type of relationship (primary, related, mentioned, derived)

        Returns:
            Dictionary containing memory_id, resource_id, relationship_type, and linked status

        Example:
            >>> result = client.memories.link_resource(
            ...     "mem_123",
            ...     resource_id="res_456",
            ...     relationship_type="primary"
            ... )
            >>> print(f"Linked: {result['linked']}")
        """
        validate_id(id, "memory")
        validate_id(resource_id, "resource")

        body: Dict[str, Any] = {"resource_id": resource_id}
        if relationship_type:
            body["relationship_type"] = relationship_type

        response = self._client._request("POST", f"/memories/{id}/resources", json=body)
        return response

    def get_resources(self, id: str) -> Dict[str, Any]:
        """
        Get resources linked to a memory.

        Args:
            id: Memory ID

        Returns:
            Dictionary containing memory_id and list of linked resources with metadata

        Example:
            >>> result = client.memories.get_resources("mem_123")
            >>> for resource in result["data"]:
            ...     print(resource["name"], resource["relationship_type"])
        """
        validate_id(id, "memory")
        response = self._client._request("GET", f"/memories/{id}/resources")
        return response

    def unlink_resource(self, id: str, resource_id: str) -> Dict[str, Any]:
        """
        Unlink a resource from a memory.

        Args:
            id: Memory ID
            resource_id: Resource ID to unlink

        Returns:
            Dictionary containing memory_id, resource_id, and unlinked status

        Example:
            >>> result = client.memories.unlink_resource("mem_123", "res_456")
            >>> print(f"Unlinked: {result['unlinked']}")
        """
        validate_id(id, "memory")
        validate_id(resource_id, "resource")
        response = self._client._request("DELETE", f"/memories/{id}/resources/{resource_id}")
        return response

    # =========================================================================
    # Memory Pinning & Protection
    # =========================================================================

    def pin(self, id: str) -> Memory:
        """
        Pin a memory to prevent decay.

        Pinned memories are protected from automatic decay and prioritized in searches.

        Args:
            id: Memory ID

        Returns:
            Updated memory object with is_pinned=True

        Example:
            >>> memory = client.memories.pin("mem_123")
            >>> assert memory.is_pinned == True
        """
        validate_id(id, "memory")
        response = self._client._request("POST", f"/memories/{id}/pin")
        return Memory.model_validate(response)

    def unpin(self, id: str) -> Memory:
        """
        Unpin a memory to allow normal decay.

        Args:
            id: Memory ID

        Returns:
            Updated memory object with is_pinned=False

        Example:
            >>> memory = client.memories.unpin("mem_123")
            >>> assert memory.is_pinned == False
        """
        validate_id(id, "memory")
        response = self._client._request("POST", f"/memories/{id}/unpin")
        return Memory.model_validate(response)

    def set_protection_level(
        self,
        id: str,
        level: str,
    ) -> Memory:
        """
        Set memory protection level.

        Protection levels:
        - "none": No protection, normal decay applies
        - "soft": Protected from auto-decay, can be manually deleted
        - "hard": Protected from deletion, requires explicit unprotection

        Args:
            id: Memory ID
            level: Protection level ("none", "soft", "hard")

        Returns:
            Updated memory object

        Example:
            >>> memory = client.memories.set_protection_level("mem_123", "hard")
            >>> print(f"Protection: {memory.protection_level}")
        """
        validate_id(id, "memory")
        if level not in ("none", "soft", "hard"):
            raise ValueError(f"Invalid protection level: {level}. Must be 'none', 'soft', or 'hard'")
        response = self._client._request(
            "POST", f"/memories/{id}/protection", json={"level": level}
        )
        return Memory.model_validate(response)

    def soft_delete(self, id: str) -> Memory:
        """
        Soft delete a memory (can be restored).

        Soft-deleted memories are hidden from normal queries but can be restored.
        Use delete() for permanent deletion.

        Args:
            id: Memory ID

        Returns:
            Updated memory object with is_deleted=True

        Example:
            >>> memory = client.memories.soft_delete("mem_123")
            >>> assert memory.is_deleted == True
        """
        validate_id(id, "memory")
        response = self._client._request("POST", f"/memories/{id}/soft-delete")
        return Memory.model_validate(response)

    def restore(self, id: str) -> Memory:
        """
        Restore a soft-deleted memory.

        Args:
            id: Memory ID

        Returns:
            Restored memory object with is_deleted=False

        Example:
            >>> memory = client.memories.restore("mem_123")
            >>> assert memory.is_deleted == False
        """
        validate_id(id, "memory")
        response = self._client._request("POST", f"/memories/{id}/restore")
        return Memory.model_validate(response)

    def get_quality_score(self, id: str) -> float:
        """
        Get the quality score for a memory.

        Quality scores range from 0-1 and indicate how valuable/useful a memory is.

        Args:
            id: Memory ID

        Returns:
            Quality score (0.0 to 1.0)

        Example:
            >>> score = client.memories.get_quality_score("mem_123")
            >>> print(f"Quality: {score:.2%}")
        """
        validate_id(id, "memory")
        response = self._client._request("GET", f"/memories/{id}/quality")
        return float(response.get("quality_score", 0.0))

    def get_topics(
        self,
        id: str,
        refresh: bool = False,
        min_relevance: Optional[float] = None,
        categories: Optional[List[str]] = None,
    ) -> List["Topic"]:
        """
        Get extracted topics for a memory.

        Args:
            id: Memory ID
            refresh: Force re-extraction of topics
            min_relevance: Minimum relevance score (0-1)
            categories: Filter by specific categories

        Returns:
            List of Topic objects

        Example:
            >>> topics = client.memories.get_topics("mem_123", min_relevance=0.5)
            >>> for topic in topics:
            ...     print(f"{topic.name}: {topic.relevance:.0%}")
        """
        from ..types import Topic

        validate_id(id, "memory")
        params: Dict[str, Any] = {}
        if refresh:
            params["refresh"] = "true"
        if min_relevance is not None:
            params["min_relevance"] = str(min_relevance)
        if categories:
            params["categories"] = ",".join(categories)

        response = self._client._request("GET", f"/memories/{id}/topics", params=params)
        return [Topic.model_validate(t) for t in response.get("topics", [])]

    # =========================================================================
    # Image Support
    # =========================================================================

    def create_with_image(
        self,
        image_file: Union[BinaryIO, Path, str, bytes],
        filename: Optional[str] = None,
        content_type: Optional[str] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        space_id: Optional[str] = None,
        description: Optional[str] = None,
    ) -> Memory:
        """
        Create a memory from an image file.

        Supports image formats: jpg, jpeg, png, gif, webp, bmp, tiff.

        Args:
            image_file: File object, path, string path, or bytes of the image
            filename: Override filename (default: extracted from path or "image")
            content_type: MIME type (e.g., 'image/jpeg', 'image/png').
                         If not provided, will be inferred from filename.
            tags: List of tags for categorization
            metadata: Additional metadata
            space_id: ID of the space to add memory to
            description: Optional text description of the image

        Returns:
            Created memory object

        Example:
            >>> # Upload image file
            >>> memory = client.memories.create_with_image(
            ...     "photo.jpg",
            ...     tags=["vacation", "beach"],
            ...     description="Beach sunset photo"
            ... )
            >>>
            >>> # Upload from bytes
            >>> with open("image.png", "rb") as f:
            ...     image_bytes = f.read()
            >>> memory = client.memories.create_with_image(
            ...     image_bytes,
            ...     filename="image.png",
            ...     content_type="image/png"
            ... )
        """
        # Handle different input types
        file_handle: BinaryIO
        should_close = False

        if isinstance(image_file, bytes):
            import io
            file_handle = io.BytesIO(image_file)
            filename = filename or "image"
        elif isinstance(image_file, (str, Path)):
            path = Path(image_file)
            filename = filename or path.name
            file_handle = open(path, "rb")
            should_close = True
        else:
            filename = filename or "image"
            file_handle = image_file

        # Infer content type from filename if not provided
        if content_type is None:
            ext = Path(filename).suffix.lower() if filename else ""
            content_type_map = {
                ".jpg": "image/jpeg",
                ".jpeg": "image/jpeg",
                ".png": "image/png",
                ".gif": "image/gif",
                ".webp": "image/webp",
                ".bmp": "image/bmp",
                ".tiff": "image/tiff",
                ".tif": "image/tiff",
            }
            content_type = content_type_map.get(ext, "image/jpeg")

        try:
            # Build form data
            data: Dict[str, Any] = {"type": "image"}
            if tags:
                data["tags"] = ",".join(tags)
            if metadata:
                data["metadata"] = json.dumps(metadata)
            if space_id:
                data["space_id"] = space_id
            if description:
                data["content"] = description

            files: Dict[str, Any] = {"file": (filename, file_handle, content_type)}

            response = self._client._request_multipart("POST", "/memories", data=data, files=files)
            return Memory.model_validate(response)
        finally:
            if should_close:
                file_handle.close()

    def get_image(self, id: str) -> bytes:
        """
        Get original image content for an image memory.

        Args:
            id: Memory ID

        Returns:
            Image data as bytes

        Example:
            >>> image_data = client.memories.get_image("mem_123")
            >>> with open("downloaded.jpg", "wb") as f:
            ...     f.write(image_data)
        """
        validate_id(id, "memory")
        return self._client._request_raw("GET", f"/memories/{id}/image")

    def get_thumbnail(self, id: str) -> bytes:
        """
        Get thumbnail image for an image memory.

        Args:
            id: Memory ID

        Returns:
            Thumbnail image data as bytes

        Example:
            >>> thumbnail = client.memories.get_thumbnail("mem_123")
            >>> with open("thumb.jpg", "wb") as f:
            ...     f.write(thumbnail)
        """
        validate_id(id, "memory")
        return self._client._request_raw("GET", f"/memories/{id}/thumbnail")

    def search_visual(
        self,
        image: Union[BinaryIO, Path, str, bytes],
        filename: Optional[str] = None,
        content_type: Optional[str] = None,
        limit: int = 10,
        threshold: Optional[float] = None,
        space_id: Optional[str] = None,
    ) -> VisualSearchResults:
        """
        Search for visually similar images by uploading a query image.

        Args:
            image: Query image as file object, path, string path, or bytes
            filename: Override filename (default: extracted from path or "query")
            content_type: MIME type (e.g., 'image/jpeg'). Inferred if not provided.
            limit: Maximum number of results (default: 10)
            threshold: Minimum similarity threshold (0-1)
            space_id: Filter results by space

        Returns:
            Visual search results with matching memories and scores

        Example:
            >>> results = client.memories.search_visual(
            ...     "query_image.jpg",
            ...     limit=5,
            ...     threshold=0.8
            ... )
            >>> for result in results.data:
            ...     print(f"{result.memory.id}: {result.score:.2f}")
        """
        # Handle different input types
        file_handle: BinaryIO
        should_close = False

        if isinstance(image, bytes):
            import io
            file_handle = io.BytesIO(image)
            filename = filename or "query"
        elif isinstance(image, (str, Path)):
            path = Path(image)
            filename = filename or path.name
            file_handle = open(path, "rb")
            should_close = True
        else:
            filename = filename or "query"
            file_handle = image

        # Infer content type from filename if not provided
        if content_type is None:
            ext = Path(filename).suffix.lower() if filename else ""
            content_type_map = {
                ".jpg": "image/jpeg",
                ".jpeg": "image/jpeg",
                ".png": "image/png",
                ".gif": "image/gif",
                ".webp": "image/webp",
            }
            content_type = content_type_map.get(ext, "image/jpeg")

        try:
            data: Dict[str, Any] = {"limit": str(limit)}
            if threshold is not None:
                data["threshold"] = str(threshold)
            if space_id:
                data["space_id"] = space_id

            files: Dict[str, Any] = {"file": (filename, file_handle, content_type)}

            response = self._client._request_multipart(
                "POST", "/memories/search/visual", data=data, files=files
            )
            return VisualSearchResults.model_validate(response)
        finally:
            if should_close:
                file_handle.close()

    def search_by_text(
        self,
        query: str,
        limit: int = 10,
        threshold: Optional[float] = None,
        space_id: Optional[str] = None,
    ) -> VisualSearchResults:
        """
        Search for images using a text query (multi-modal text-to-image search).

        Args:
            query: Text description to search for
            limit: Maximum number of results (default: 10)
            threshold: Minimum similarity threshold (0-1)
            space_id: Filter results by space

        Returns:
            Visual search results with matching image memories

        Example:
            >>> results = client.memories.search_by_text(
            ...     "sunset on the beach",
            ...     limit=5
            ... )
            >>> for result in results.data:
            ...     print(f"{result.memory.id}: {result.score:.2f}")
        """
        body: Dict[str, Any] = {
            "query": query,
            "limit": limit,
        }
        if threshold is not None:
            body["threshold"] = threshold
        if space_id:
            body["space_id"] = space_id

        response = self._client._request("POST", "/memories/search/text", json=body)
        return VisualSearchResults.model_validate(response)

    def find_similar(
        self,
        id: str,
        type: str = "image",
        limit: int = 10,
        threshold: Optional[float] = None,
    ) -> VisualSearchResults:
        """
        Find visually similar images to a given memory.

        Args:
            id: Memory ID to find similar images for
            type: Similarity type ("image" for visual similarity)
            limit: Maximum number of results (default: 10)
            threshold: Minimum similarity threshold (0-1)

        Returns:
            Visual search results with similar memories

        Example:
            >>> similar = client.memories.find_similar(
            ...     "mem_123",
            ...     type="image",
            ...     limit=5
            ... )
            >>> for result in similar.data:
            ...     print(f"{result.memory.id}: {result.score:.2f}")
        """
        validate_id(id, "memory")
        params: Dict[str, Any] = {
            "type": type,
            "limit": limit,
        }
        if threshold is not None:
            params["threshold"] = threshold

        response = self._client._request("GET", f"/memories/{id}/similar", params=params)
        return VisualSearchResults.model_validate(response)

    def check_duplicates(
        self,
        image: Union[BinaryIO, Path, str, bytes],
        filename: Optional[str] = None,
        content_type: Optional[str] = None,
        threshold: float = 0.95,
        space_id: Optional[str] = None,
    ) -> DuplicateCheckResult:
        """
        Check if an image has duplicates in the memory store.

        Args:
            image: Image to check as file object, path, string path, or bytes
            filename: Override filename (default: extracted from path or "check")
            content_type: MIME type (e.g., 'image/jpeg'). Inferred if not provided.
            threshold: Similarity threshold for duplicate detection (default: 0.95)
            space_id: Filter search within a specific space

        Returns:
            Duplicate check result with is_duplicate flag and matching memories

        Example:
            >>> result = client.memories.check_duplicates(
            ...     "photo.jpg",
            ...     threshold=0.90
            ... )
            >>> if result.is_duplicate:
            ...     print(f"Found {len(result.duplicates)} duplicates")
        """
        # Handle different input types
        file_handle: BinaryIO
        should_close = False

        if isinstance(image, bytes):
            import io
            file_handle = io.BytesIO(image)
            filename = filename or "check"
        elif isinstance(image, (str, Path)):
            path = Path(image)
            filename = filename or path.name
            file_handle = open(path, "rb")
            should_close = True
        else:
            filename = filename or "check"
            file_handle = image

        # Infer content type from filename if not provided
        if content_type is None:
            ext = Path(filename).suffix.lower() if filename else ""
            content_type_map = {
                ".jpg": "image/jpeg",
                ".jpeg": "image/jpeg",
                ".png": "image/png",
                ".gif": "image/gif",
                ".webp": "image/webp",
            }
            content_type = content_type_map.get(ext, "image/jpeg")

        try:
            data: Dict[str, Any] = {"threshold": str(threshold)}
            if space_id:
                data["space_id"] = space_id

            files: Dict[str, Any] = {"file": (filename, file_handle, content_type)}

            response = self._client._request_multipart(
                "POST", "/memories/check-duplicates", data=data, files=files
            )
            return DuplicateCheckResult.model_validate(response)
        finally:
            if should_close:
                file_handle.close()

    def cluster_images(
        self,
        space_id: Optional[str] = None,
        num_clusters: int = 10,
        algorithm: str = "kmeans",
    ) -> ImageClusterResult:
        """
        Cluster images by visual similarity.

        Args:
            space_id: Optional space ID to filter images
            num_clusters: Target number of clusters (default: 10)
            algorithm: Clustering algorithm ("kmeans", "hierarchical")

        Returns:
            Image clustering result with cluster assignments

        Example:
            >>> result = client.memories.cluster_images(
            ...     num_clusters=5,
            ...     algorithm="kmeans"
            ... )
            >>> for cluster in result.clusters:
            ...     print(f"Cluster {cluster.cluster_id}: {cluster.size} images")
        """
        body: Dict[str, Any] = {
            "num_clusters": num_clusters,
            "algorithm": algorithm,
        }
        if space_id:
            body["space_id"] = space_id

        response = self._client._request("POST", "/memories/images/cluster", json=body)
        return ImageClusterResult.model_validate(response)

    def auto_tag(
        self,
        image_id: str,
        apply: bool = False,
        min_confidence: float = 0.5,
    ) -> AutoTagResult:
        """
        Generate automatic tags for a single image.

        Args:
            image_id: Memory ID of the image to tag
            apply: Whether to apply generated tags to the memory (default: False)
            min_confidence: Minimum confidence threshold for tags (default: 0.5)

        Returns:
            Auto-tag result with generated tags

        Example:
            >>> result = client.memories.auto_tag("mem_123", apply=True)
            >>> for tag in result.tags:
            ...     print(f"{tag.name}: {tag.confidence:.2f}")
        """
        validate_id(image_id, "image")
        body: Dict[str, Any] = {
            "apply": apply,
            "min_confidence": min_confidence,
        }

        response = self._client._request(
            "POST", f"/memories/images/{image_id}/auto-tag", json=body
        )
        return AutoTagResult.model_validate(response)

    def batch_auto_tag(
        self,
        image_ids: List[str],
        apply: bool = False,
        min_confidence: float = 0.5,
    ) -> BatchAutoTagResult:
        """
        Generate automatic tags for multiple images.

        Args:
            image_ids: List of memory IDs to auto-tag
            apply: Whether to apply generated tags to memories (default: False)
            min_confidence: Minimum confidence threshold for tags (default: 0.5)

        Returns:
            Batch auto-tag result with individual results

        Example:
            >>> result = client.memories.batch_auto_tag(
            ...     ["mem_123", "mem_456", "mem_789"],
            ...     apply=True
            ... )
            >>> print(f"Successfully tagged {result.success} images")
        """
        for i, image_id in enumerate(image_ids):
            validate_id(image_id, f"image[{i}]")

        body: Dict[str, Any] = {
            "image_ids": image_ids,
            "apply": apply,
            "min_confidence": min_confidence,
        }

        response = self._client._request("POST", "/memories/images/batch-auto-tag", json=body)
        return BatchAutoTagResult.model_validate(response)

    def suggest_queries(
        self,
        space_id: Optional[str] = None,
        limit: int = 20,
    ) -> QuerySuggestionsResult:
        """
        Get suggested search queries based on image content.

        Args:
            space_id: Optional space ID to filter suggestions
            limit: Maximum number of suggestions (default: 20)

        Returns:
            Query suggestions result with suggested queries

        Example:
            >>> suggestions = client.memories.suggest_queries(limit=10)
            >>> for suggestion in suggestions.suggestions:
            ...     print(f"{suggestion.query} ({suggestion.type})")
        """
        params: Dict[str, Any] = {"limit": limit}
        if space_id:
            params["space_id"] = space_id

        response = self._client._request("GET", "/memories/images/suggest-queries", params=params)
        return QuerySuggestionsResult.model_validate(response)


class AsyncMemoriesResource:
    """Async resource for managing memories."""

    def __init__(self, client: AsyncClientProtocol) -> None:
        """Initialize async memories resource with client."""
        self._client = client

    async def create(
        self,
        content: str,
        type: Optional[MemoryType] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        priority: Optional[int] = None,
        space_id: Optional[str] = None,
        options: Optional[Dict[str, Any]] = None,
        is_pinned: bool = False,
        protection_level: str = "none",
    ) -> Memory:
        """Create a new memory (async)."""
        data = MemoryCreate(
            content=content,
            type=type or MemoryType.TEXT,
            tags=tags,
            metadata=metadata,
            priority=priority,
            space_id=space_id,
            options=MemoryOptions(**options) if options else None,
            is_pinned=is_pinned if is_pinned else None,
            protection_level=protection_level if protection_level != "none" else None,
        )
        response = await self._client._request(
            "POST", "/memories", json=data.model_dump(exclude_none=True)
        )
        return Memory.model_validate(response)

    async def list(
        self,
        q: Optional[str] = None,
        mode: Optional[SearchMode] = None,
        limit: int = 100,
        offset: int = 0,
        tags: Optional[List[str]] = None,
        space_id: Optional[str] = None,
        pinned: Optional[bool] = None,
        protected: Optional[bool] = None,
        min_quality: Optional[float] = None,
        include_deleted: bool = False,
    ) -> MemoryList:
        """List memories with optional filtering (async)."""
        params: Dict[str, Any] = {"limit": limit, "offset": offset}
        if q:
            params["q"] = q
        if mode:
            params["mode"] = mode.value
        if tags:
            params["tags"] = ",".join(tags)
        if space_id:
            params["space_id"] = space_id
        if pinned is not None:
            params["pinned"] = "true" if pinned else "false"
        if protected is not None:
            params["protected"] = "true" if protected else "false"
        if min_quality is not None:
            params["min_quality"] = str(min_quality)
        if include_deleted:
            params["include_deleted"] = "true"

        response = await self._client._request("GET", "/memories", params=params)
        return MemoryList.model_validate(response)

    async def iter(
        self,
        q: Optional[str] = None,
        mode: Optional[SearchMode] = None,
        tags: Optional[List[str]] = None,
        space_id: Optional[str] = None,
        page_size: int = 100,
        max_items: Optional[int] = None,
    ) -> AsyncPaginator:
        """
        Get async iterator for all memories with automatic pagination.

        Returns:
            Async paginator that yields Memory objects

        Example:
            >>> async for memory in await client.memories.iter(tags=["work"]):
            ...     print(memory.content)
        """
        params: Dict[str, Any] = {}
        if q:
            params["q"] = q
        if mode:
            params["mode"] = mode.value
        if tags:
            params["tags"] = ",".join(tags)
        if space_id:
            params["space_id"] = space_id

        return AsyncPaginator(
            self.list,
            initial_params=params,
            limit=page_size,
            max_items=max_items,
        )

    async def get(self, id: str) -> Memory:
        """Get a memory by ID (async)."""
        validate_id(id, "memory")
        response = await self._client._request("GET", f"/memories/{id}")
        return Memory.model_validate(response)

    async def update(
        self,
        id: str,
        content: Optional[str] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        priority: Optional[int] = None,
    ) -> Memory:
        """Update a memory (async)."""
        validate_id(id, "memory")
        data = MemoryUpdate(
            content=content,
            tags=tags,
            metadata=metadata,
            priority=priority,
        )
        response = await self._client._request(
            "PATCH", f"/memories/{id}", json=data.model_dump(exclude_none=True)
        )
        return Memory.model_validate(response)

    async def delete(self, id: str) -> None:
        """Delete a memory (async)."""
        validate_id(id, "memory")
        await self._client._request("DELETE", f"/memories/{id}")

    async def bulk_create(self, memories: List[MemoryCreate]) -> BulkResult:
        """Create multiple memories at once (async).

        Returns:
            Bulk operation result with success/failure counts
        """
        data = [m.model_dump(exclude_none=True) for m in memories]
        response = await self._client._request("POST", "/memories/bulk", json={"memories": data})
        return BulkResult.model_validate(response)

    async def bulk_update(self, updates: List[Dict[str, Any]]) -> BulkResult:
        """Update multiple memories at once (async).

        Returns:
            Bulk operation result with success/failure counts
        """
        # Validate all IDs before making the request
        for i, update in enumerate(updates):
            if "id" not in update:
                raise ValueError(f"Update at index {i} is missing an 'id'")
            validate_id(update["id"], f"memory[{i}]")
        response = await self._client._request("PATCH", "/memories/bulk", json={"updates": updates})
        return BulkResult.model_validate(response)

    async def bulk_delete(self, ids: List[str]) -> BulkResult:
        """Delete multiple memories at once (async).

        Returns:
            Bulk operation result with success/failure counts
        """
        # Validate all IDs before making the request
        for i, item_id in enumerate(ids):
            validate_id(item_id, f"memory[{i}]")
        response = await self._client._request("DELETE", "/memories/bulk", json={"ids": ids})
        return BulkResult.model_validate(response)

    async def get_config(self) -> MemoryConfig:
        """Get memory system configuration (async)."""
        response = await self._client._request("GET", "/memories/config")
        return MemoryConfig.model_validate(response)

    async def stream_audio(self, id: str) -> bytes:
        """Get audio content for an audio memory (async)."""
        validate_id(id, "memory")
        return await self._client._request_raw("GET", f"/memories/{id}/audio")

    async def stream_audio_chunks(self, id: str, chunk_size: int = 8192) -> AsyncIterator[bytes]:
        """
        Stream audio content in chunks for efficient memory usage (async).

        Args:
            id: Memory ID
            chunk_size: Size of each chunk in bytes

        Yields:
            Chunks of audio data

        Example:
            >>> async with aiofiles.open("audio.mp3", "wb") as f:
            ...     async for chunk in client.memories.stream_audio_chunks("mem_123"):
            ...         await f.write(chunk)
        """
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
        """
        Create a memory from an audio or video file (async).

        Supports audio formats: mp3, mp4, m4a, wav, webm, ogg, flac, aac
        Supports video formats: mp4, webm, mov, avi, mkv, flv, mpeg

        For advanced transcription options (speaker diarization, entity detection,
        chapters, etc.), use the transcribe() method after upload.

        Args:
            audio_file: File object, path, or string path to the audio/video file
            filename: Override filename (default: extracted from path or "audio")
            content_type: MIME type (e.g., 'audio/mpeg', 'video/mp4')
            tags: List of tags for categorization
            metadata: Additional metadata
            space_id: ID of the space to add memory to
            transcribe: Whether to transcribe the audio/video automatically
            language: Language code for transcription (e.g., 'en', 'es')

        Returns:
            Created memory object

        Example:
            >>> # Upload audio file
            >>> memory = await client.memories.create_with_audio(
            ...     "recording.mp3",
            ...     tags=["meeting", "important"],
            ...     transcribe=True
            ... )
            >>>
            >>> # Upload video file with transcription
            >>> memory = await client.memories.create_with_audio(
            ...     "meeting.mp4",
            ...     content_type="video/mp4",
            ...     transcribe=True,
            ...     language="en"
            ... )
        """
        # Handle different input types
        file_handle: BinaryIO
        if isinstance(audio_file, (str, Path)):
            path = Path(audio_file)
            filename = filename or path.name
            file_handle = open(path, "rb")
            should_close = True
        else:
            filename = filename or "audio"
            file_handle = audio_file
            should_close = False

        try:
            # Build form data
            data: Dict[str, Any] = {"type": "audio"}
            if tags:
                data["tags"] = ",".join(tags)
            if metadata:
                data["metadata"] = json.dumps(metadata)
            if space_id:
                data["space_id"] = space_id
            if transcribe:
                data["transcribe"] = "true"
            if language:
                data["language"] = language

            files: Dict[str, Any] = {"file": (filename, file_handle, content_type)}

            response = await self._client._request_multipart(
                "POST", "/memories", data=data, files=files
            )
            return Memory.model_validate(response)
        finally:
            if should_close:
                file_handle.close()

    async def get_transcript(self, id: str) -> "Transcript":
        """
        Get transcript for an audio memory (async).

        Args:
            id: Memory ID

        Returns:
            Full transcript with metadata, segments, entities, and chapters

        Example:
            >>> transcript = await client.memories.get_transcript("mem_123")
            >>> print(transcript.text)  # Full transcript text
            >>> print(transcript.summary)  # Auto-generated summary
            >>> for segment in transcript.segments or []:
            ...     print(f"{segment.speaker}: {segment.text}")
        """
        validate_id(id, "memory")
        response = await self._client._request("GET", f"/memories/{id}/transcript")
        from ..types import Transcript
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
    ) -> "Job":
        """
        Transcribe or re-transcribe an audio memory with advanced options (async).

        Args:
            id: Memory ID
            language: Language code for transcription (e.g., 'en', 'es')
            prompt: Context to improve transcription accuracy
            provider: Transcription provider ('assemblyai' or 'openai')
            enable_speaker_diarization: Enable speaker identification and labeling
            enable_entity_detection: Enable entity detection in transcript
            enable_content_safety: Enable content safety labeling
            enable_auto_chapters: Enable automatic chapter generation
            enable_auto_summarization: Enable automatic summarization
            speakers_expected: Expected number of speakers (hint for diarization)

        Returns:
            Job object for tracking transcription progress

        Example:
            >>> # Basic transcription
            >>> job = await client.memories.transcribe("mem_123", language="en")
            >>> print(f"Transcription status: {job.status}")
            >>>
            >>> # Advanced transcription with speaker diarization
            >>> job = await client.memories.transcribe(
            ...     "mem_123",
            ...     provider="assemblyai",
            ...     enable_speaker_diarization=True,
            ...     speakers_expected=2,
            ...     enable_auto_chapters=True
            ... )
            >>> # Poll for completion or use webhooks
            >>> print(f"Job ID: {job.id}, Progress: {job.progress}%")
        """
        validate_id(id, "memory")
        body: Dict[str, Any] = {}
        if language:
            body["language"] = language
        if prompt:
            body["prompt"] = prompt
        if provider:
            body["provider"] = provider
        if enable_speaker_diarization is not None:
            body["enableSpeakerDiarization"] = enable_speaker_diarization
        if enable_entity_detection is not None:
            body["enableEntityDetection"] = enable_entity_detection
        if enable_content_safety is not None:
            body["enableContentSafety"] = enable_content_safety
        if enable_auto_chapters is not None:
            body["enableAutoChapters"] = enable_auto_chapters
        if enable_auto_summarization is not None:
            body["enableAutoSummarization"] = enable_auto_summarization
        if speakers_expected is not None:
            body["speakersExpected"] = speakers_expected

        response = await self._client._request("POST", f"/memories/{id}/transcribe", json=body)
        from ..types import Job
        return Job.model_validate(response)

    async def get_stats(
        self,
        space_id: Optional[str] = None,
        created_after: Optional[str] = None,
        created_before: Optional[str] = None,
        include_type_distribution: bool = False,
        include_tag_distribution: bool = False,
        include_timeline: bool = False,
        timeline_granularity: Optional[str] = None,
    ) -> "MemoryStats":
        """Get memory statistics (async)."""
        from ..types import MemoryStats

        params: Dict[str, Any] = {}
        if space_id:
            params["space_id"] = space_id
        if created_after:
            params["created_after"] = created_after
        if created_before:
            params["created_before"] = created_before
        if include_type_distribution:
            params["include_type_distribution"] = "true"
        if include_tag_distribution:
            params["include_tag_distribution"] = "true"
        if include_timeline:
            params["include_timeline"] = "true"
        if timeline_granularity:
            params["timeline_granularity"] = timeline_granularity

        response = await self._client._request("GET", "/memories/stats", params=params)
        return MemoryStats.model_validate(response)

    async def link_resource(
        self,
        id: str,
        resource_id: str,
        relationship_type: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Link a resource to a memory (async).

        Args:
            id: Memory ID
            resource_id: Resource ID to link
            relationship_type: Type of relationship (primary, related, mentioned, derived)

        Returns:
            Dictionary containing memory_id, resource_id, relationship_type, and linked status

        Example:
            >>> result = await client.memories.link_resource(
            ...     "mem_123",
            ...     resource_id="res_456",
            ...     relationship_type="primary"
            ... )
            >>> print(f"Linked: {result['linked']}")
        """
        validate_id(id, "memory")
        validate_id(resource_id, "resource")

        body: Dict[str, Any] = {"resource_id": resource_id}
        if relationship_type:
            body["relationship_type"] = relationship_type

        response = await self._client._request("POST", f"/memories/{id}/resources", json=body)
        return response

    async def get_resources(self, id: str) -> Dict[str, Any]:
        """
        Get resources linked to a memory (async).

        Args:
            id: Memory ID

        Returns:
            Dictionary containing memory_id and list of linked resources with metadata

        Example:
            >>> result = await client.memories.get_resources("mem_123")
            >>> for resource in result["data"]:
            ...     print(resource["name"], resource["relationship_type"])
        """
        validate_id(id, "memory")
        response = await self._client._request("GET", f"/memories/{id}/resources")
        return response

    async def unlink_resource(self, id: str, resource_id: str) -> Dict[str, Any]:
        """
        Unlink a resource from a memory (async).

        Args:
            id: Memory ID
            resource_id: Resource ID to unlink

        Returns:
            Dictionary containing memory_id, resource_id, and unlinked status

        Example:
            >>> result = await client.memories.unlink_resource("mem_123", "res_456")
            >>> print(f"Unlinked: {result['unlinked']}")
        """
        validate_id(id, "memory")
        validate_id(resource_id, "resource")
        response = await self._client._request("DELETE", f"/memories/{id}/resources/{resource_id}")
        return response

    # =========================================================================
    # Memory Pinning & Protection (async)
    # =========================================================================

    async def pin(self, id: str) -> Memory:
        """
        Pin a memory to prevent decay (async).

        Pinned memories are protected from automatic decay and prioritized in searches.

        Args:
            id: Memory ID

        Returns:
            Updated memory object with is_pinned=True

        Example:
            >>> memory = await client.memories.pin("mem_123")
            >>> assert memory.is_pinned == True
        """
        validate_id(id, "memory")
        response = await self._client._request("POST", f"/memories/{id}/pin")
        return Memory.model_validate(response)

    async def unpin(self, id: str) -> Memory:
        """
        Unpin a memory to allow normal decay (async).

        Args:
            id: Memory ID

        Returns:
            Updated memory object with is_pinned=False

        Example:
            >>> memory = await client.memories.unpin("mem_123")
            >>> assert memory.is_pinned == False
        """
        validate_id(id, "memory")
        response = await self._client._request("POST", f"/memories/{id}/unpin")
        return Memory.model_validate(response)

    async def set_protection_level(
        self,
        id: str,
        level: str,
    ) -> Memory:
        """
        Set memory protection level (async).

        Protection levels:
        - "none": No protection, normal decay applies
        - "soft": Protected from auto-decay, can be manually deleted
        - "hard": Protected from deletion, requires explicit unprotection

        Args:
            id: Memory ID
            level: Protection level ("none", "soft", "hard")

        Returns:
            Updated memory object

        Example:
            >>> memory = await client.memories.set_protection_level("mem_123", "hard")
            >>> print(f"Protection: {memory.protection_level}")
        """
        validate_id(id, "memory")
        if level not in ("none", "soft", "hard"):
            raise ValueError(f"Invalid protection level: {level}. Must be 'none', 'soft', or 'hard'")
        response = await self._client._request(
            "POST", f"/memories/{id}/protection", json={"level": level}
        )
        return Memory.model_validate(response)

    async def soft_delete(self, id: str) -> Memory:
        """
        Soft delete a memory (can be restored) (async).

        Soft-deleted memories are hidden from normal queries but can be restored.
        Use delete() for permanent deletion.

        Args:
            id: Memory ID

        Returns:
            Updated memory object with is_deleted=True

        Example:
            >>> memory = await client.memories.soft_delete("mem_123")
            >>> assert memory.is_deleted == True
        """
        validate_id(id, "memory")
        response = await self._client._request("POST", f"/memories/{id}/soft-delete")
        return Memory.model_validate(response)

    async def restore(self, id: str) -> Memory:
        """
        Restore a soft-deleted memory (async).

        Args:
            id: Memory ID

        Returns:
            Restored memory object with is_deleted=False

        Example:
            >>> memory = await client.memories.restore("mem_123")
            >>> assert memory.is_deleted == False
        """
        validate_id(id, "memory")
        response = await self._client._request("POST", f"/memories/{id}/restore")
        return Memory.model_validate(response)

    async def get_quality_score(self, id: str) -> float:
        """
        Get the quality score for a memory (async).

        Quality scores range from 0-1 and indicate how valuable/useful a memory is.

        Args:
            id: Memory ID

        Returns:
            Quality score (0.0 to 1.0)

        Example:
            >>> score = await client.memories.get_quality_score("mem_123")
            >>> print(f"Quality: {score:.2%}")
        """
        validate_id(id, "memory")
        response = await self._client._request("GET", f"/memories/{id}/quality")
        return float(response.get("quality_score", 0.0))

    async def get_topics(
        self,
        id: str,
        refresh: bool = False,
        min_relevance: Optional[float] = None,
        categories: Optional[List[str]] = None,
    ) -> List["Topic"]:
        """
        Get extracted topics for a memory (async).

        Args:
            id: Memory ID
            refresh: Force re-extraction of topics
            min_relevance: Minimum relevance score (0-1)
            categories: Filter by specific categories

        Returns:
            List of Topic objects

        Example:
            >>> topics = await client.memories.get_topics("mem_123", min_relevance=0.5)
            >>> for topic in topics:
            ...     print(f"{topic.name}: {topic.relevance:.0%}")
        """
        from ..types import Topic

        validate_id(id, "memory")
        params: Dict[str, Any] = {}
        if refresh:
            params["refresh"] = "true"
        if min_relevance is not None:
            params["min_relevance"] = str(min_relevance)
        if categories:
            params["categories"] = ",".join(categories)

        response = await self._client._request("GET", f"/memories/{id}/topics", params=params)
        return [Topic.model_validate(t) for t in response.get("topics", [])]

    # =========================================================================
    # Image Support (async)
    # =========================================================================

    async def create_with_image(
        self,
        image_file: Union[BinaryIO, Path, str, bytes],
        filename: Optional[str] = None,
        content_type: Optional[str] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        space_id: Optional[str] = None,
        description: Optional[str] = None,
    ) -> Memory:
        """
        Create a memory from an image file (async).

        Supports image formats: jpg, jpeg, png, gif, webp, bmp, tiff.

        Args:
            image_file: File object, path, string path, or bytes of the image
            filename: Override filename (default: extracted from path or "image")
            content_type: MIME type (e.g., 'image/jpeg', 'image/png').
                         If not provided, will be inferred from filename.
            tags: List of tags for categorization
            metadata: Additional metadata
            space_id: ID of the space to add memory to
            description: Optional text description of the image

        Returns:
            Created memory object

        Example:
            >>> # Upload image file
            >>> memory = await client.memories.create_with_image(
            ...     "photo.jpg",
            ...     tags=["vacation", "beach"],
            ...     description="Beach sunset photo"
            ... )
        """
        # Handle different input types
        file_handle: BinaryIO
        should_close = False

        if isinstance(image_file, bytes):
            import io
            file_handle = io.BytesIO(image_file)
            filename = filename or "image"
        elif isinstance(image_file, (str, Path)):
            path = Path(image_file)
            filename = filename or path.name
            file_handle = open(path, "rb")
            should_close = True
        else:
            filename = filename or "image"
            file_handle = image_file

        # Infer content type from filename if not provided
        if content_type is None:
            ext = Path(filename).suffix.lower() if filename else ""
            content_type_map = {
                ".jpg": "image/jpeg",
                ".jpeg": "image/jpeg",
                ".png": "image/png",
                ".gif": "image/gif",
                ".webp": "image/webp",
                ".bmp": "image/bmp",
                ".tiff": "image/tiff",
                ".tif": "image/tiff",
            }
            content_type = content_type_map.get(ext, "image/jpeg")

        try:
            # Build form data
            data: Dict[str, Any] = {"type": "image"}
            if tags:
                data["tags"] = ",".join(tags)
            if metadata:
                data["metadata"] = json.dumps(metadata)
            if space_id:
                data["space_id"] = space_id
            if description:
                data["content"] = description

            files: Dict[str, Any] = {"file": (filename, file_handle, content_type)}

            response = await self._client._request_multipart(
                "POST", "/memories", data=data, files=files
            )
            return Memory.model_validate(response)
        finally:
            if should_close:
                file_handle.close()

    async def get_image(self, id: str) -> bytes:
        """
        Get original image content for an image memory (async).

        Args:
            id: Memory ID

        Returns:
            Image data as bytes

        Example:
            >>> image_data = await client.memories.get_image("mem_123")
            >>> async with aiofiles.open("downloaded.jpg", "wb") as f:
            ...     await f.write(image_data)
        """
        validate_id(id, "memory")
        return await self._client._request_raw("GET", f"/memories/{id}/image")

    async def get_thumbnail(self, id: str) -> bytes:
        """
        Get thumbnail image for an image memory (async).

        Args:
            id: Memory ID

        Returns:
            Thumbnail image data as bytes

        Example:
            >>> thumbnail = await client.memories.get_thumbnail("mem_123")
            >>> async with aiofiles.open("thumb.jpg", "wb") as f:
            ...     await f.write(thumbnail)
        """
        validate_id(id, "memory")
        return await self._client._request_raw("GET", f"/memories/{id}/thumbnail")

    async def search_visual(
        self,
        image: Union[BinaryIO, Path, str, bytes],
        filename: Optional[str] = None,
        content_type: Optional[str] = None,
        limit: int = 10,
        threshold: Optional[float] = None,
        space_id: Optional[str] = None,
    ) -> VisualSearchResults:
        """
        Search for visually similar images by uploading a query image (async).

        Args:
            image: Query image as file object, path, string path, or bytes
            filename: Override filename (default: extracted from path or "query")
            content_type: MIME type (e.g., 'image/jpeg'). Inferred if not provided.
            limit: Maximum number of results (default: 10)
            threshold: Minimum similarity threshold (0-1)
            space_id: Filter results by space

        Returns:
            Visual search results with matching memories and scores

        Example:
            >>> results = await client.memories.search_visual(
            ...     "query_image.jpg",
            ...     limit=5,
            ...     threshold=0.8
            ... )
            >>> for result in results.data:
            ...     print(f"{result.memory.id}: {result.score:.2f}")
        """
        # Handle different input types
        file_handle: BinaryIO
        should_close = False

        if isinstance(image, bytes):
            import io
            file_handle = io.BytesIO(image)
            filename = filename or "query"
        elif isinstance(image, (str, Path)):
            path = Path(image)
            filename = filename or path.name
            file_handle = open(path, "rb")
            should_close = True
        else:
            filename = filename or "query"
            file_handle = image

        # Infer content type from filename if not provided
        if content_type is None:
            ext = Path(filename).suffix.lower() if filename else ""
            content_type_map = {
                ".jpg": "image/jpeg",
                ".jpeg": "image/jpeg",
                ".png": "image/png",
                ".gif": "image/gif",
                ".webp": "image/webp",
            }
            content_type = content_type_map.get(ext, "image/jpeg")

        try:
            data: Dict[str, Any] = {"limit": str(limit)}
            if threshold is not None:
                data["threshold"] = str(threshold)
            if space_id:
                data["space_id"] = space_id

            files: Dict[str, Any] = {"file": (filename, file_handle, content_type)}

            response = await self._client._request_multipart(
                "POST", "/memories/search/visual", data=data, files=files
            )
            return VisualSearchResults.model_validate(response)
        finally:
            if should_close:
                file_handle.close()

    async def search_by_text(
        self,
        query: str,
        limit: int = 10,
        threshold: Optional[float] = None,
        space_id: Optional[str] = None,
    ) -> VisualSearchResults:
        """
        Search for images using a text query (multi-modal text-to-image search) (async).

        Args:
            query: Text description to search for
            limit: Maximum number of results (default: 10)
            threshold: Minimum similarity threshold (0-1)
            space_id: Filter results by space

        Returns:
            Visual search results with matching image memories

        Example:
            >>> results = await client.memories.search_by_text(
            ...     "sunset on the beach",
            ...     limit=5
            ... )
            >>> for result in results.data:
            ...     print(f"{result.memory.id}: {result.score:.2f}")
        """
        body: Dict[str, Any] = {
            "query": query,
            "limit": limit,
        }
        if threshold is not None:
            body["threshold"] = threshold
        if space_id:
            body["space_id"] = space_id

        response = await self._client._request("POST", "/memories/search/text", json=body)
        return VisualSearchResults.model_validate(response)

    async def find_similar(
        self,
        id: str,
        type: str = "image",
        limit: int = 10,
        threshold: Optional[float] = None,
    ) -> VisualSearchResults:
        """
        Find visually similar images to a given memory (async).

        Args:
            id: Memory ID to find similar images for
            type: Similarity type ("image" for visual similarity)
            limit: Maximum number of results (default: 10)
            threshold: Minimum similarity threshold (0-1)

        Returns:
            Visual search results with similar memories

        Example:
            >>> similar = await client.memories.find_similar(
            ...     "mem_123",
            ...     type="image",
            ...     limit=5
            ... )
            >>> for result in similar.data:
            ...     print(f"{result.memory.id}: {result.score:.2f}")
        """
        validate_id(id, "memory")
        params: Dict[str, Any] = {
            "type": type,
            "limit": limit,
        }
        if threshold is not None:
            params["threshold"] = threshold

        response = await self._client._request("GET", f"/memories/{id}/similar", params=params)
        return VisualSearchResults.model_validate(response)

    async def check_duplicates(
        self,
        image: Union[BinaryIO, Path, str, bytes],
        filename: Optional[str] = None,
        content_type: Optional[str] = None,
        threshold: float = 0.95,
        space_id: Optional[str] = None,
    ) -> DuplicateCheckResult:
        """
        Check if an image has duplicates in the memory store (async).

        Args:
            image: Image to check as file object, path, string path, or bytes
            filename: Override filename (default: extracted from path or "check")
            content_type: MIME type (e.g., 'image/jpeg'). Inferred if not provided.
            threshold: Similarity threshold for duplicate detection (default: 0.95)
            space_id: Filter search within a specific space

        Returns:
            Duplicate check result with is_duplicate flag and matching memories

        Example:
            >>> result = await client.memories.check_duplicates(
            ...     "photo.jpg",
            ...     threshold=0.90
            ... )
            >>> if result.is_duplicate:
            ...     print(f"Found {len(result.duplicates)} duplicates")
        """
        # Handle different input types
        file_handle: BinaryIO
        should_close = False

        if isinstance(image, bytes):
            import io
            file_handle = io.BytesIO(image)
            filename = filename or "check"
        elif isinstance(image, (str, Path)):
            path = Path(image)
            filename = filename or path.name
            file_handle = open(path, "rb")
            should_close = True
        else:
            filename = filename or "check"
            file_handle = image

        # Infer content type from filename if not provided
        if content_type is None:
            ext = Path(filename).suffix.lower() if filename else ""
            content_type_map = {
                ".jpg": "image/jpeg",
                ".jpeg": "image/jpeg",
                ".png": "image/png",
                ".gif": "image/gif",
                ".webp": "image/webp",
            }
            content_type = content_type_map.get(ext, "image/jpeg")

        try:
            data: Dict[str, Any] = {"threshold": str(threshold)}
            if space_id:
                data["space_id"] = space_id

            files: Dict[str, Any] = {"file": (filename, file_handle, content_type)}

            response = await self._client._request_multipart(
                "POST", "/memories/check-duplicates", data=data, files=files
            )
            return DuplicateCheckResult.model_validate(response)
        finally:
            if should_close:
                file_handle.close()

    async def cluster_images(
        self,
        space_id: Optional[str] = None,
        num_clusters: int = 10,
        algorithm: str = "kmeans",
    ) -> ImageClusterResult:
        """
        Cluster images by visual similarity (async).

        Args:
            space_id: Optional space ID to filter images
            num_clusters: Target number of clusters (default: 10)
            algorithm: Clustering algorithm ("kmeans", "hierarchical")

        Returns:
            Image clustering result with cluster assignments

        Example:
            >>> result = await client.memories.cluster_images(
            ...     num_clusters=5,
            ...     algorithm="kmeans"
            ... )
            >>> for cluster in result.clusters:
            ...     print(f"Cluster {cluster.cluster_id}: {cluster.size} images")
        """
        body: Dict[str, Any] = {
            "num_clusters": num_clusters,
            "algorithm": algorithm,
        }
        if space_id:
            body["space_id"] = space_id

        response = await self._client._request("POST", "/memories/images/cluster", json=body)
        return ImageClusterResult.model_validate(response)

    async def auto_tag(
        self,
        image_id: str,
        apply: bool = False,
        min_confidence: float = 0.5,
    ) -> AutoTagResult:
        """
        Generate automatic tags for a single image (async).

        Args:
            image_id: Memory ID of the image to tag
            apply: Whether to apply generated tags to the memory (default: False)
            min_confidence: Minimum confidence threshold for tags (default: 0.5)

        Returns:
            Auto-tag result with generated tags

        Example:
            >>> result = await client.memories.auto_tag("mem_123", apply=True)
            >>> for tag in result.tags:
            ...     print(f"{tag.name}: {tag.confidence:.2f}")
        """
        validate_id(image_id, "image")
        body: Dict[str, Any] = {
            "apply": apply,
            "min_confidence": min_confidence,
        }

        response = await self._client._request(
            "POST", f"/memories/images/{image_id}/auto-tag", json=body
        )
        return AutoTagResult.model_validate(response)

    async def batch_auto_tag(
        self,
        image_ids: List[str],
        apply: bool = False,
        min_confidence: float = 0.5,
    ) -> BatchAutoTagResult:
        """
        Generate automatic tags for multiple images (async).

        Args:
            image_ids: List of memory IDs to auto-tag
            apply: Whether to apply generated tags to memories (default: False)
            min_confidence: Minimum confidence threshold for tags (default: 0.5)

        Returns:
            Batch auto-tag result with individual results

        Example:
            >>> result = await client.memories.batch_auto_tag(
            ...     ["mem_123", "mem_456", "mem_789"],
            ...     apply=True
            ... )
            >>> print(f"Successfully tagged {result.success} images")
        """
        for i, image_id in enumerate(image_ids):
            validate_id(image_id, f"image[{i}]")

        body: Dict[str, Any] = {
            "image_ids": image_ids,
            "apply": apply,
            "min_confidence": min_confidence,
        }

        response = await self._client._request("POST", "/memories/images/batch-auto-tag", json=body)
        return BatchAutoTagResult.model_validate(response)

    async def suggest_queries(
        self,
        space_id: Optional[str] = None,
        limit: int = 20,
    ) -> QuerySuggestionsResult:
        """
        Get suggested search queries based on image content (async).

        Args:
            space_id: Optional space ID to filter suggestions
            limit: Maximum number of suggestions (default: 20)

        Returns:
            Query suggestions result with suggested queries

        Example:
            >>> suggestions = await client.memories.suggest_queries(limit=10)
            >>> for suggestion in suggestions.suggestions:
            ...     print(f"{suggestion.query} ({suggestion.type})")
        """
        params: Dict[str, Any] = {"limit": limit}
        if space_id:
            params["space_id"] = space_id

        response = await self._client._request(
            "GET", "/memories/images/suggest-queries", params=params
        )
        return QuerySuggestionsResult.model_validate(response)
