"""Image operations mixin for memories resource.

Provides image upload, visual search, and image processing operations.
"""

from pathlib import Path
from typing import Any, BinaryIO, Dict, List, Optional, Union

from ...types import (
    AutoTagResult,
    BatchAutoTagResult,
    DuplicateCheckResult,
    ImageClusterResult,
    Memory,
    QuerySuggestionsResult,
    VisualSearchResults,
)
from ...utils.file_handling import build_multipart_data, prepare_file_upload
from ...utils.security import validate_id


class ImageOperationsMixin:
    """Mixin providing image operations for sync memories resource."""

    _client: Any  # Type hint for the client

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
        """Create a memory from an image file."""
        with prepare_file_upload(
            image_file,
            default_filename="image",
            filename_override=filename,
            content_type_override=content_type,
            type_hint="image",
        ) as (file_handle, fname, ctype):
            data = build_multipart_data(
                base_data={"type": "image"},
                tags=tags,
                metadata=metadata,
                space_id=space_id,
                content=description,
            )
            files: Dict[str, Any] = {"file": (fname, file_handle, ctype)}
            response = self._client._request_multipart("POST", "/memories", data=data, files=files)
            return Memory.model_validate(response)

    def get_image(self, id: str) -> bytes:
        """Get original image content for an image memory."""
        validate_id(id, "memory")
        return self._client._request_raw("GET", f"/memories/{id}/image")

    def get_thumbnail(self, id: str) -> bytes:
        """Get thumbnail image for an image memory."""
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
        """Search for visually similar images by uploading a query image."""
        with prepare_file_upload(
            image,
            default_filename="query",
            filename_override=filename,
            content_type_override=content_type,
            type_hint="image",
        ) as (file_handle, fname, ctype):
            data: Dict[str, Any] = {"limit": str(limit)}
            if threshold is not None:
                data["threshold"] = str(threshold)
            if space_id:
                data["space_id"] = space_id

            files: Dict[str, Any] = {"file": (fname, file_handle, ctype)}
            response = self._client._request_multipart(
                "POST", "/memories/search/visual", data=data, files=files
            )
            return VisualSearchResults.model_validate(response)

    def search_by_text(
        self,
        query: str,
        limit: int = 10,
        threshold: Optional[float] = None,
        space_id: Optional[str] = None,
    ) -> VisualSearchResults:
        """Search for images using a text query (multi-modal text-to-image search)."""
        body: Dict[str, Any] = {"query": query, "limit": limit}
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
        """Find visually similar images to a given memory."""
        validate_id(id, "memory")
        params: Dict[str, Any] = {"type": type, "limit": limit}
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
        """Check if an image has duplicates in the memory store."""
        with prepare_file_upload(
            image,
            default_filename="check",
            filename_override=filename,
            content_type_override=content_type,
            type_hint="image",
        ) as (file_handle, fname, ctype):
            data: Dict[str, Any] = {"threshold": str(threshold)}
            if space_id:
                data["space_id"] = space_id

            files: Dict[str, Any] = {"file": (fname, file_handle, ctype)}
            response = self._client._request_multipart(
                "POST", "/memories/check-duplicates", data=data, files=files
            )
            return DuplicateCheckResult.model_validate(response)

    def cluster_images(
        self,
        space_id: Optional[str] = None,
        num_clusters: int = 10,
        algorithm: str = "kmeans",
    ) -> ImageClusterResult:
        """Cluster images by visual similarity."""
        body: Dict[str, Any] = {"num_clusters": num_clusters, "algorithm": algorithm}
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
        """Generate automatic tags for a single image."""
        validate_id(image_id, "image")
        body: Dict[str, Any] = {"apply": apply, "min_confidence": min_confidence}
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
        """Generate automatic tags for multiple images."""
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
        """Get suggested search queries based on image content."""
        params: Dict[str, Any] = {"limit": limit}
        if space_id:
            params["space_id"] = space_id

        response = self._client._request("GET", "/memories/images/suggest-queries", params=params)
        return QuerySuggestionsResult.model_validate(response)


class AsyncImageOperationsMixin:
    """Mixin providing image operations for async memories resource."""

    _client: Any  # Type hint for the client

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
        """Create a memory from an image file (async)."""
        with prepare_file_upload(
            image_file,
            default_filename="image",
            filename_override=filename,
            content_type_override=content_type,
            type_hint="image",
        ) as (file_handle, fname, ctype):
            data = build_multipart_data(
                base_data={"type": "image"},
                tags=tags,
                metadata=metadata,
                space_id=space_id,
                content=description,
            )
            files: Dict[str, Any] = {"file": (fname, file_handle, ctype)}
            response = await self._client._request_multipart(
                "POST", "/memories", data=data, files=files
            )
            return Memory.model_validate(response)

    async def get_image(self, id: str) -> bytes:
        """Get original image content for an image memory (async)."""
        validate_id(id, "memory")
        return await self._client._request_raw("GET", f"/memories/{id}/image")

    async def get_thumbnail(self, id: str) -> bytes:
        """Get thumbnail image for an image memory (async)."""
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
        """Search for visually similar images by uploading a query image (async)."""
        with prepare_file_upload(
            image,
            default_filename="query",
            filename_override=filename,
            content_type_override=content_type,
            type_hint="image",
        ) as (file_handle, fname, ctype):
            data: Dict[str, Any] = {"limit": str(limit)}
            if threshold is not None:
                data["threshold"] = str(threshold)
            if space_id:
                data["space_id"] = space_id

            files: Dict[str, Any] = {"file": (fname, file_handle, ctype)}
            response = await self._client._request_multipart(
                "POST", "/memories/search/visual", data=data, files=files
            )
            return VisualSearchResults.model_validate(response)

    async def search_by_text(
        self,
        query: str,
        limit: int = 10,
        threshold: Optional[float] = None,
        space_id: Optional[str] = None,
    ) -> VisualSearchResults:
        """Search for images using a text query (async)."""
        body: Dict[str, Any] = {"query": query, "limit": limit}
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
        """Find visually similar images to a given memory (async)."""
        validate_id(id, "memory")
        params: Dict[str, Any] = {"type": type, "limit": limit}
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
        """Check if an image has duplicates in the memory store (async)."""
        with prepare_file_upload(
            image,
            default_filename="check",
            filename_override=filename,
            content_type_override=content_type,
            type_hint="image",
        ) as (file_handle, fname, ctype):
            data: Dict[str, Any] = {"threshold": str(threshold)}
            if space_id:
                data["space_id"] = space_id

            files: Dict[str, Any] = {"file": (fname, file_handle, ctype)}
            response = await self._client._request_multipart(
                "POST", "/memories/check-duplicates", data=data, files=files
            )
            return DuplicateCheckResult.model_validate(response)

    async def cluster_images(
        self,
        space_id: Optional[str] = None,
        num_clusters: int = 10,
        algorithm: str = "kmeans",
    ) -> ImageClusterResult:
        """Cluster images by visual similarity (async)."""
        body: Dict[str, Any] = {"num_clusters": num_clusters, "algorithm": algorithm}
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
        """Generate automatic tags for a single image (async)."""
        validate_id(image_id, "image")
        body: Dict[str, Any] = {"apply": apply, "min_confidence": min_confidence}
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
        """Generate automatic tags for multiple images (async)."""
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
        """Get suggested search queries based on image content (async)."""
        params: Dict[str, Any] = {"limit": limit}
        if space_id:
            params["space_id"] = space_id

        response = await self._client._request(
            "GET", "/memories/images/suggest-queries", params=params
        )
        return QuerySuggestionsResult.model_validate(response)
