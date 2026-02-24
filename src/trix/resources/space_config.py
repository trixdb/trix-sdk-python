"""Space configuration resource for Trix SDK."""

from typing import Optional

from .base import BaseAsyncResource, BaseSyncResource
from ..types.space_config import (
    SpaceConfigAuditResponse,
    SpaceConfigPatch,
    SpaceConfigResponse,
    SpaceConfigValidation,
)
from ..utils.security import validate_id


class SpaceConfigResource(BaseSyncResource):
    """Resource for managing space configuration.

    Provides access to the ADR-042 Space Configuration Layer, which
    supports per-space configuration for memory, LLM, retrieval, and
    privacy settings with defaults/overrides semantics.

    Example:
        >>> config = client.space_config.get("space_123")
        >>> print(config.config["retrieval"].effective)
        >>>
        >>> updated = client.space_config.update("space_123", retrieval={"top_k": 20})
    """

    def get(self, space_id: str) -> SpaceConfigResponse:
        """Get the full configuration for a space.

        Returns all four categories (memory, llm, retrieval, privacy)
        with their defaults, overrides, and effective values.

        Args:
            space_id: Space ID

        Returns:
            Space configuration with version number

        Raises:
            ValidationError: If ID format is invalid
            NotFoundError: If space doesn't exist

        Example:
            >>> config = client.space_config.get("space_123")
            >>> print(config.version)
        """
        validate_id(space_id, "space")
        response = self._request("GET", f"/spaces/{space_id}/config")
        return SpaceConfigResponse.model_validate(response)

    def update(
        self,
        space_id: str,
        memory: Optional[dict] = None,
        llm: Optional[dict] = None,
        retrieval: Optional[dict] = None,
        privacy: Optional[dict] = None,
        expected_version: Optional[int] = None,
    ) -> SpaceConfigResponse:
        """Update space configuration using JSON Merge Patch semantics.

        Only include the categories and keys you want to change.

        Args:
            space_id: Space ID
            memory: Memory configuration overrides
            llm: LLM configuration overrides
            retrieval: Retrieval configuration overrides
            privacy: Privacy configuration overrides
            expected_version: Optimistic concurrency version (If-Match header)

        Returns:
            Updated space configuration

        Raises:
            ValidationError: If ID format is invalid or patch is invalid
            NotFoundError: If space doesn't exist

        Example:
            >>> updated = client.space_config.update(
            ...     "space_123",
            ...     retrieval={"top_k": 20},
            ...     privacy={"pii_detection": True}
            ... )
        """
        validate_id(space_id, "space")
        patch = SpaceConfigPatch(memory=memory, llm=llm, retrieval=retrieval, privacy=privacy)
        headers = {}
        if expected_version is not None:
            headers["If-Match"] = str(expected_version)
        response = self._request(
            "PATCH",
            f"/spaces/{space_id}/config",
            json=patch.model_dump(exclude_none=True),
            headers=headers if headers else None,
        )
        return SpaceConfigResponse.model_validate(response)

    def validate(
        self,
        space_id: str,
        memory: Optional[dict] = None,
        llm: Optional[dict] = None,
        retrieval: Optional[dict] = None,
        privacy: Optional[dict] = None,
    ) -> SpaceConfigValidation:
        """Validate a configuration patch without applying it (dry run).

        Args:
            space_id: Space ID
            memory: Memory configuration overrides to validate
            llm: LLM configuration overrides to validate
            retrieval: Retrieval configuration overrides to validate
            privacy: Privacy configuration overrides to validate

        Returns:
            Validation result with errors (if any) and affected categories

        Raises:
            ValidationError: If ID format is invalid
            NotFoundError: If space doesn't exist

        Example:
            >>> result = client.space_config.validate(
            ...     "space_123", retrieval={"top_k": -1}
            ... )
            >>> if not result.valid:
            ...     print("Errors:", result.errors)
        """
        validate_id(space_id, "space")
        patch = SpaceConfigPatch(memory=memory, llm=llm, retrieval=retrieval, privacy=privacy)
        response = self._request(
            "POST", f"/spaces/{space_id}/config/validate", json=patch.model_dump(exclude_none=True)
        )
        return SpaceConfigValidation.model_validate(response)

    def audit(
        self, space_id: str, limit: int = 50, offset: int = 0
    ) -> SpaceConfigAuditResponse:
        """Get the configuration audit trail for a space.

        Args:
            space_id: Space ID
            limit: Maximum number of events to return (default: 50)
            offset: Number of events to skip (default: 0)

        Returns:
            Paginated audit events

        Raises:
            ValidationError: If ID format is invalid
            NotFoundError: If space doesn't exist

        Example:
            >>> audit = client.space_config.audit("space_123", limit=10)
            >>> for event in audit.events:
            ...     print(f"{event.category} changed by {event.source}")
        """
        validate_id(space_id, "space")
        response = self._request(
            "GET", f"/spaces/{space_id}/config/audit", params={"limit": limit, "offset": offset}
        )
        return SpaceConfigAuditResponse.model_validate(response)


class AsyncSpaceConfigResource(BaseAsyncResource):
    """Async resource for managing space configuration.

    Provides access to the ADR-042 Space Configuration Layer with
    async/await support.

    Example:
        >>> config = await client.space_config.get("space_123")
        >>> print(config.config["retrieval"].effective)
    """

    async def get(self, space_id: str) -> SpaceConfigResponse:
        """Get the full configuration for a space (async).

        Args:
            space_id: Space ID

        Returns:
            Space configuration with version number
        """
        validate_id(space_id, "space")
        response = await self._request("GET", f"/spaces/{space_id}/config")
        return SpaceConfigResponse.model_validate(response)

    async def update(
        self,
        space_id: str,
        memory: Optional[dict] = None,
        llm: Optional[dict] = None,
        retrieval: Optional[dict] = None,
        privacy: Optional[dict] = None,
        expected_version: Optional[int] = None,
    ) -> SpaceConfigResponse:
        """Update space configuration using JSON Merge Patch semantics (async).

        Args:
            space_id: Space ID
            memory: Memory configuration overrides
            llm: LLM configuration overrides
            retrieval: Retrieval configuration overrides
            privacy: Privacy configuration overrides
            expected_version: Optimistic concurrency version (If-Match header)

        Returns:
            Updated space configuration
        """
        validate_id(space_id, "space")
        patch = SpaceConfigPatch(memory=memory, llm=llm, retrieval=retrieval, privacy=privacy)
        headers = {}
        if expected_version is not None:
            headers["If-Match"] = str(expected_version)
        response = await self._request(
            "PATCH",
            f"/spaces/{space_id}/config",
            json=patch.model_dump(exclude_none=True),
            headers=headers if headers else None,
        )
        return SpaceConfigResponse.model_validate(response)

    async def validate(
        self,
        space_id: str,
        memory: Optional[dict] = None,
        llm: Optional[dict] = None,
        retrieval: Optional[dict] = None,
        privacy: Optional[dict] = None,
    ) -> SpaceConfigValidation:
        """Validate a configuration patch without applying it (async).

        Args:
            space_id: Space ID
            memory: Memory configuration overrides to validate
            llm: LLM configuration overrides to validate
            retrieval: Retrieval configuration overrides to validate
            privacy: Privacy configuration overrides to validate

        Returns:
            Validation result with errors (if any) and affected categories
        """
        validate_id(space_id, "space")
        patch = SpaceConfigPatch(memory=memory, llm=llm, retrieval=retrieval, privacy=privacy)
        response = await self._request(
            "POST", f"/spaces/{space_id}/config/validate", json=patch.model_dump(exclude_none=True)
        )
        return SpaceConfigValidation.model_validate(response)

    async def audit(
        self, space_id: str, limit: int = 50, offset: int = 0
    ) -> SpaceConfigAuditResponse:
        """Get the configuration audit trail for a space (async).

        Args:
            space_id: Space ID
            limit: Maximum number of events to return (default: 50)
            offset: Number of events to skip (default: 0)

        Returns:
            Paginated audit events
        """
        validate_id(space_id, "space")
        response = await self._request(
            "GET", f"/spaces/{space_id}/config/audit", params={"limit": limit, "offset": offset}
        )
        return SpaceConfigAuditResponse.model_validate(response)
