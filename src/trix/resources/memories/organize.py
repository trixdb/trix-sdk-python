"""Memory organize operations mixin.

Provides store-and-organize composite operation that stores a memory
and runs tagging, enrichment, linking, and clustering in one request.
"""

from typing import Any, Dict, List, Optional


class OrganizeOperationsMixin:
    """Mixin providing organize operations for sync memories resource."""

    _client: Any  # Type hint for the client

    def store_and_organize(
        self,
        content: str,
        *,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        space_id: Optional[str] = None,
        detect_contradictions: bool = False,
    ) -> Dict[str, Any]:
        """Store a memory and automatically organize it.

        Stores the memory then runs tagging, enrichment, linking, and
        clustering in a single request.

        Args:
            content: Memory content
            tags: Optional initial tags
            metadata: Optional metadata
            space_id: Space to store in
            detect_contradictions: Run contradiction detection (~200ms)

        Returns:
            Stored memory with organization results
        """
        body: Dict[str, Any] = {"content": content}
        if tags:
            body["tags"] = tags
        if metadata:
            body["metadata"] = metadata
        if space_id:
            body["space_id"] = space_id
        if detect_contradictions:
            body["detect_contradictions"] = True
        return self._client._request("POST", "/memories/store-organize", json=body)


class AsyncOrganizeOperationsMixin:
    """Mixin providing organize operations for async memories resource."""

    _client: Any  # Type hint for the client

    async def store_and_organize(
        self,
        content: str,
        *,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        space_id: Optional[str] = None,
        detect_contradictions: bool = False,
    ) -> Dict[str, Any]:
        """Store a memory and automatically organize it (async).

        Stores the memory then runs tagging, enrichment, linking, and
        clustering in a single request.

        Args:
            content: Memory content
            tags: Optional initial tags
            metadata: Optional metadata
            space_id: Space to store in
            detect_contradictions: Run contradiction detection (~200ms)

        Returns:
            Stored memory with organization results
        """
        body: Dict[str, Any] = {"content": content}
        if tags:
            body["tags"] = tags
        if metadata:
            body["metadata"] = metadata
        if space_id:
            body["space_id"] = space_id
        if detect_contradictions:
            body["detect_contradictions"] = True
        return await self._client._request(
            "POST", "/memories/store-organize", json=body
        )
