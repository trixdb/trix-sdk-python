"""Async clusters resource for Trix SDK."""

from typing import TYPE_CHECKING, Any, Dict, List, Optional

from ..protocols import AsyncClientProtocol
from ..types import (
    Cluster,
    ClusterCreate,
    ClusterList,
    ClusterMembership,
    ClusterUpdate,
)
from ..utils.pagination import AsyncPaginator
from ..utils.security import validate_id, validate_limit, validate_threshold

if TYPE_CHECKING:
    from ..types import ClusterQuality, ClusterTopics


class AsyncClustersResource:
    """Async resource for managing clusters."""

    def __init__(self, client: AsyncClientProtocol) -> None:
        """Initialize async clusters resource with client."""
        self._client = client

    async def create(
        self,
        name: str,
        description: Optional[str] = None,
        color: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Cluster:
        """Create a new cluster (async)."""
        data = ClusterCreate(
            name=name,
            description=description,
            color=color,
            metadata=metadata,
        )
        response = await self._client._request(
            "POST", "/clusters", json=data.model_dump(exclude_none=True)
        )
        return Cluster.model_validate(response)

    async def list(
        self,
        q: Optional[str] = None,
        sort: Optional[str] = None,
        limit: int = 100,
        cursor: Optional[str] = None,
        scale: Optional[str] = None,
    ) -> ClusterList:
        """List clusters with optional filtering (async)."""
        params: Dict[str, Any] = {"limit": limit}
        if q:
            params["q"] = q
        if sort:
            params["sort"] = sort
        if cursor:
            params["cursor"] = cursor
        if scale:
            params["scale"] = scale

        response = await self._client._request("GET", "/clusters", params=params)
        return ClusterList.model_validate(response)

    async def iter(
        self,
        q: Optional[str] = None,
        sort: Optional[str] = None,
        page_size: int = 100,
        max_items: Optional[int] = None,
    ) -> AsyncPaginator:
        """Get async iterator for all clusters with automatic pagination."""
        params: Dict[str, Any] = {}
        if q:
            params["q"] = q
        if sort:
            params["sort"] = sort

        return AsyncPaginator(
            self.list,
            initial_params=params,
            limit=page_size,
            max_items=max_items,
        )

    async def get(self, id: str, include_memories: bool = False) -> Cluster:
        """Get a cluster by ID (async)."""
        validate_id(id, "cluster")
        params: Dict[str, Any] = {}
        if include_memories:
            params["include_memories"] = "true"
        response = await self._client._request("GET", f"/clusters/{id}", params=params)
        return Cluster.model_validate(response)

    async def update(
        self,
        id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        color: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Cluster:
        """Update a cluster (async)."""
        validate_id(id, "cluster")
        data = ClusterUpdate(
            name=name,
            description=description,
            color=color,
            metadata=metadata,
        )
        response = await self._client._request(
            "PATCH", f"/clusters/{id}", json=data.model_dump(exclude_none=True)
        )
        return Cluster.model_validate(response)

    async def delete(self, id: str) -> None:
        """Delete a cluster (async)."""
        validate_id(id, "cluster")
        await self._client._request("DELETE", f"/clusters/{id}")

    async def bulk_create(self, clusters: List[ClusterCreate]) -> List[Cluster]:
        """Create multiple clusters at once (async)."""
        data = [c.model_dump(exclude_none=True) for c in clusters]
        response = await self._client._request("POST", "/clusters/bulk", json={"clusters": data})
        return [Cluster.model_validate(c) for c in response.get("data", [])]

    async def bulk_update(self, updates: List[Dict[str, Any]]) -> List[Cluster]:
        """Update multiple clusters at once (async)."""
        for i, update in enumerate(updates):
            if "id" not in update:
                raise ValueError(f"Update at index {i} is missing an 'id'")
            validate_id(update["id"], f"cluster[{i}]")
        response = await self._client._request("PATCH", "/clusters/bulk", json={"updates": updates})
        return [Cluster.model_validate(c) for c in response.get("data", [])]

    async def bulk_delete(self, ids: List[str]) -> None:
        """Delete multiple clusters at once (async)."""
        for i, item_id in enumerate(ids):
            validate_id(item_id, f"cluster[{i}]")
        await self._client._request("DELETE", "/clusters/bulk", json={"ids": ids})

    async def add_memory(
        self, cluster_id: str, memory_id: str, confidence: float = 1.0
    ) -> ClusterMembership:
        """Add a memory to a cluster (async)."""
        validate_id(cluster_id, "cluster")
        validate_id(memory_id, "memory")
        validate_threshold(confidence, param_name="confidence")
        response = await self._client._request(
            "POST",
            f"/clusters/{cluster_id}/memories/{memory_id}",
            json={"confidence": confidence},
        )
        return ClusterMembership.model_validate(response)

    async def remove_memory(self, cluster_id: str, memory_id: str) -> None:
        """Remove a memory from a cluster (async)."""
        validate_id(cluster_id, "cluster")
        validate_id(memory_id, "memory")
        await self._client._request("DELETE", f"/clusters/{cluster_id}/memories/{memory_id}")

    async def expand(
        self, cluster_id: str, limit: int = 10, threshold: float = 0.7
    ) -> List[Dict[str, Any]]:
        """Expand a cluster by finding similar memories (async)."""
        validate_id(cluster_id, "cluster")
        validate_limit(limit, max_limit=100)
        validate_threshold(threshold)
        params = {"limit": limit, "threshold": threshold}
        response = await self._client._request(
            "POST", f"/clusters/{cluster_id}/expand", params=params
        )
        return list(response.get("suggestions", []))

    async def get_quality(self, cluster_id: str) -> "ClusterQuality":
        """Get quality metrics for a cluster (async)."""
        from ..types import ClusterQuality

        validate_id(cluster_id, "cluster")
        response = await self._client._request("GET", f"/clusters/{cluster_id}/quality")
        return ClusterQuality.model_validate(response)

    async def get_topics(self, cluster_id: str) -> "ClusterTopics":
        """Get topics for a cluster (async)."""
        from ..types import ClusterTopics

        validate_id(cluster_id, "cluster")
        response = await self._client._request("GET", f"/clusters/{cluster_id}/topics")
        return ClusterTopics.model_validate(response)
