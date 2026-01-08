"""Search resource for Trix SDK."""

from typing import Any, Dict, List, Optional

from .base import BaseAsyncResource, BaseSyncResource, validate_ids
from ..types import (
    EmbedAllResponse,
    EmbeddingResponse,
    SearchConfig,
    SearchResults,
)
from ..utils.security import validate_id


def _build_similar_params(limit: int, threshold: Optional[float]) -> Dict[str, Any]:
    """Build similar search params."""
    params: Dict[str, Any] = {"limit": limit}
    if threshold is not None:
        params["threshold"] = str(threshold)
    return params


class SearchResource(BaseSyncResource):
    """Resource for search and embeddings.

    This resource provides similarity search and embedding generation
    capabilities for memories.

    Example:
        >>> # Find similar memories
        >>> results = client.search.similar(
        ...     memory_id="mem_123",
        ...     limit=20,
        ...     threshold=0.7
        ... )
        >>>
        >>> # Get search configuration
        >>> config = client.search.get_config()
    """

    def similar(
        self, memory_id: str, limit: int = 10, threshold: Optional[float] = None
    ) -> SearchResults:
        """Find memories similar to a given memory.

        Args:
            memory_id: Reference memory ID
            limit: Maximum number of results
            threshold: Minimum similarity threshold

        Returns:
            Search results with similarity scores

        Example:
            >>> results = client.search.similar(
            ...     memory_id="mem_123",
            ...     limit=20,
            ...     threshold=0.7
            ... )
        """
        validate_id(memory_id, "memory")
        params = _build_similar_params(limit, threshold)
        response = self._request("GET", f"/search/similar/{memory_id}", params=params)
        return SearchResults.model_validate(response)

    def embed(self, memory_ids: List[str]) -> EmbeddingResponse:
        """Generate embeddings for specific memories.

        Args:
            memory_ids: List of memory IDs to embed

        Returns:
            Embeddings response

        Example:
            >>> embeddings = client.search.embed(["mem_123", "mem_456"])
        """
        validate_ids(memory_ids, "memory")
        response = self._request("POST", "/search/embed", json={"memory_ids": memory_ids})
        return EmbeddingResponse.model_validate(response)

    def embed_all(self, batch_size: int = 100) -> EmbedAllResponse:
        """Generate embeddings for all memories in batches.

        Args:
            batch_size: Number of memories to process per batch

        Returns:
            Batch embedding response

        Example:
            >>> result = client.search.embed_all(batch_size=500)
        """
        params = {"batch_size": batch_size}
        response = self._request("POST", "/search/embed-all", params=params)
        return EmbedAllResponse.model_validate(response)

    def get_config(self) -> SearchConfig:
        """Get search system configuration.

        Returns:
            Search configuration

        Example:
            >>> config = client.search.get_config()
            >>> print(config.max_limit)
        """
        response = self._request("GET", "/search/config")
        return SearchConfig.model_validate(response)

    def query(
        self,
        query: str,
        limit: int = 10,
        threshold: Optional[float] = None,
        cluster_scale: Optional[str] = None,
        space_id: Optional[str] = None,
        tags: Optional[List[str]] = None,
    ) -> SearchResults:
        """Search memories with semantic query.

        Args:
            query: Search query text
            limit: Maximum number of results
            threshold: Minimum similarity threshold
            cluster_scale: Filter by cluster scale ("fine", "medium", "coarse")
            space_id: Filter by space
            tags: Filter by tags

        Returns:
            Search results with similarity scores

        Example:
            >>> # Basic search
            >>> results = client.search.query("project deadlines")
            >>>
            >>> # Search within coarse clusters
            >>> results = client.search.query(
            ...     "project deadlines",
            ...     cluster_scale="coarse",
            ...     limit=20
            ... )
        """
        params: Dict[str, Any] = {"q": query, "limit": limit}
        if threshold is not None:
            params["threshold"] = str(threshold)
        if cluster_scale:
            params["cluster_scale"] = cluster_scale
        if space_id:
            params["space_id"] = space_id
        if tags:
            params["tags"] = ",".join(tags)

        response = self._request("GET", "/search", params=params)
        return SearchResults.model_validate(response)

    def by_topic(
        self,
        topic: str,
        limit: int = 10,
        space_id: Optional[str] = None,
    ) -> SearchResults:
        """Search memories by topic.

        Args:
            topic: Topic name to search for
            limit: Maximum number of results
            space_id: Filter by space

        Returns:
            Search results for memories matching the topic

        Example:
            >>> results = client.search.by_topic("machine learning")
            >>> for result in results.data:
            ...     print(result.memory.content)
        """
        params: Dict[str, Any] = {"topic": topic, "limit": limit}
        if space_id:
            params["space_id"] = space_id

        response = self._request("GET", "/search/topic", params=params)
        return SearchResults.model_validate(response)


class AsyncSearchResource(BaseAsyncResource):
    """Async resource for search and embeddings.

    Example:
        >>> results = await client.search.similar("mem_123", limit=20)
        >>> config = await client.search.get_config()
    """

    async def similar(
        self, memory_id: str, limit: int = 10, threshold: Optional[float] = None
    ) -> SearchResults:
        """Find memories similar to a given memory (async).

        Args:
            memory_id: Reference memory ID
            limit: Maximum number of results
            threshold: Minimum similarity threshold

        Returns:
            Search results with similarity scores
        """
        validate_id(memory_id, "memory")
        params = _build_similar_params(limit, threshold)
        response = await self._request("GET", f"/search/similar/{memory_id}", params=params)
        return SearchResults.model_validate(response)

    async def embed(self, memory_ids: List[str]) -> EmbeddingResponse:
        """Generate embeddings for specific memories (async).

        Args:
            memory_ids: List of memory IDs to embed

        Returns:
            Embeddings response
        """
        validate_ids(memory_ids, "memory")
        response = await self._request("POST", "/search/embed", json={"memory_ids": memory_ids})
        return EmbeddingResponse.model_validate(response)

    async def embed_all(self, batch_size: int = 100) -> EmbedAllResponse:
        """Generate embeddings for all memories in batches (async).

        Args:
            batch_size: Number of memories to process per batch

        Returns:
            Batch embedding response
        """
        params = {"batch_size": batch_size}
        response = await self._request("POST", "/search/embed-all", params=params)
        return EmbedAllResponse.model_validate(response)

    async def get_config(self) -> SearchConfig:
        """Get search system configuration (async).

        Returns:
            Search configuration
        """
        response = await self._request("GET", "/search/config")
        return SearchConfig.model_validate(response)

    async def query(
        self,
        query: str,
        limit: int = 10,
        threshold: Optional[float] = None,
        cluster_scale: Optional[str] = None,
        space_id: Optional[str] = None,
        tags: Optional[List[str]] = None,
    ) -> SearchResults:
        """Search memories with semantic query (async).

        Args:
            query: Search query text
            limit: Maximum number of results
            threshold: Minimum similarity threshold
            cluster_scale: Filter by cluster scale ("fine", "medium", "coarse")
            space_id: Filter by space
            tags: Filter by tags

        Returns:
            Search results with similarity scores
        """
        params: Dict[str, Any] = {"q": query, "limit": limit}
        if threshold is not None:
            params["threshold"] = str(threshold)
        if cluster_scale:
            params["cluster_scale"] = cluster_scale
        if space_id:
            params["space_id"] = space_id
        if tags:
            params["tags"] = ",".join(tags)

        response = await self._request("GET", "/search", params=params)
        return SearchResults.model_validate(response)

    async def by_topic(
        self,
        topic: str,
        limit: int = 10,
        space_id: Optional[str] = None,
    ) -> SearchResults:
        """Search memories by topic (async).

        Args:
            topic: Topic name to search for
            limit: Maximum number of results
            space_id: Filter by space

        Returns:
            Search results for memories matching the topic
        """
        params: Dict[str, Any] = {"topic": topic, "limit": limit}
        if space_id:
            params["space_id"] = space_id

        response = await self._request("GET", "/search/topic", params=params)
        return SearchResults.model_validate(response)
