"""Knowledge resource for Trix SDK.

Provides high-level knowledge operations like topic summaries
and converting memories into structured notes.
"""

from typing import Any, Dict, List, Optional

from .base import BaseAsyncResource, BaseSyncResource


class KnowledgeResource(BaseSyncResource):
    """Resource for knowledge operations.

    Example:
        >>> summary = client.knowledge.summary("machine learning")
        >>> note = client.knowledge.to_note(query="project status")
    """

    def summary(
        self,
        topic: str,
        *,
        limit: int = 30,
        space_id: Optional[str] = None,
        group_by: str = "tags",
    ) -> Dict[str, Any]:
        """Get structured knowledge summary about a topic.

        Args:
            topic: Topic to summarize
            limit: Maximum memories to consider
            space_id: Filter by space
            group_by: Grouping strategy ("tags", "clusters", "time")

        Returns:
            Structured summary with grouped knowledge
        """
        body: Dict[str, Any] = {
            "topic": topic,
            "limit": limit,
            "group_by": group_by,
        }
        if space_id:
            body["space_id"] = space_id
        return self._request("POST", "/knowledge/summary", json=body)

    def to_note(
        self,
        *,
        memory_ids: Optional[List[str]] = None,
        query: Optional[str] = None,
        title: Optional[str] = None,
        space_id: Optional[str] = None,
        limit: int = 20,
    ) -> Dict[str, Any]:
        """Convert memories into a structured note.

        Provide either memory_ids or query to select memories.

        Args:
            memory_ids: Specific memory IDs to include
            query: Search query to find memories
            title: Optional title for the note
            space_id: Filter by space
            limit: Maximum memories to include

        Returns:
            Generated note with title, sections, and source memories
        """
        body: Dict[str, Any] = {"limit": limit}
        if memory_ids:
            body["memory_ids"] = memory_ids
        if query:
            body["query"] = query
        if title:
            body["title"] = title
        if space_id:
            body["space_id"] = space_id
        return self._request("POST", "/knowledge/to-note", json=body)


class AsyncKnowledgeResource(BaseAsyncResource):
    """Async resource for knowledge operations.

    Example:
        >>> summary = await client.knowledge.summary("machine learning")
        >>> note = await client.knowledge.to_note(query="project status")
    """

    async def summary(
        self,
        topic: str,
        *,
        limit: int = 30,
        space_id: Optional[str] = None,
        group_by: str = "tags",
    ) -> Dict[str, Any]:
        """Get structured knowledge summary about a topic (async).

        Args:
            topic: Topic to summarize
            limit: Maximum memories to consider
            space_id: Filter by space
            group_by: Grouping strategy ("tags", "clusters", "time")

        Returns:
            Structured summary with grouped knowledge
        """
        body: Dict[str, Any] = {
            "topic": topic,
            "limit": limit,
            "group_by": group_by,
        }
        if space_id:
            body["space_id"] = space_id
        return await self._request("POST", "/knowledge/summary", json=body)

    async def to_note(
        self,
        *,
        memory_ids: Optional[List[str]] = None,
        query: Optional[str] = None,
        title: Optional[str] = None,
        space_id: Optional[str] = None,
        limit: int = 20,
    ) -> Dict[str, Any]:
        """Convert memories into a structured note (async).

        Provide either memory_ids or query to select memories.

        Args:
            memory_ids: Specific memory IDs to include
            query: Search query to find memories
            title: Optional title for the note
            space_id: Filter by space
            limit: Maximum memories to include

        Returns:
            Generated note with title, sections, and source memories
        """
        body: Dict[str, Any] = {"limit": limit}
        if memory_ids:
            body["memory_ids"] = memory_ids
        if query:
            body["query"] = query
        if title:
            body["title"] = title
        if space_id:
            body["space_id"] = space_id
        return await self._request("POST", "/knowledge/to-note", json=body)
