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
    BulkResult,
    Memory,
    MemoryConfig,
    MemoryCreate,
    MemoryList,
    MemoryOptions,
    MemoryType,
    MemoryUpdate,
    SearchMode,
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

        Returns:
            Created memory object

        Example:
            >>> memory = client.memories.create(
            ...     content="Important information",
            ...     tags=["work", "important"],
            ...     metadata={"source": "meeting"}
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

        Returns:
            List of memories with pagination info

        Example:
            >>> results = client.memories.list(
            ...     q="important",
            ...     mode=SearchMode.HYBRID,
            ...     tags=["work"]
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
