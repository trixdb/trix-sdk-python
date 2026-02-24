"""Space configuration type definitions for Trix SDK.

These types support the ADR-042 Space Configuration Layer,
which provides per-space configuration for memory, LLM,
retrieval, and privacy settings.
"""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class SpaceConfigCategory(BaseModel):
    """A configuration category with defaults, overrides, and effective values.

    Attributes:
        defaults: System-level defaults for this category
        overrides: Space-specific overrides set by the user
        effective: Computed values (defaults merged with overrides)
    """

    defaults: Dict[str, Any]
    overrides: Dict[str, Any]
    effective: Dict[str, Any]


class SpaceConfigResponse(BaseModel):
    """Full space configuration response.

    Contains all four configuration categories and an optimistic
    concurrency version number.

    Attributes:
        config: Dictionary of category name to SpaceConfigCategory
        version: Optimistic concurrency version number
    """

    config: Dict[str, SpaceConfigCategory]
    version: int


class SpaceConfigPatch(BaseModel):
    """Partial configuration patch using JSON Merge Patch semantics.

    Only include the categories and keys you want to change.
    Set a key to None to remove an override and revert to the default.

    Attributes:
        memory: Memory configuration overrides
        llm: LLM configuration overrides
        retrieval: Retrieval configuration overrides
        privacy: Privacy configuration overrides
    """

    memory: Optional[Dict[str, Any]] = None
    llm: Optional[Dict[str, Any]] = None
    retrieval: Optional[Dict[str, Any]] = None
    privacy: Optional[Dict[str, Any]] = None


class SpaceConfigValidation(BaseModel):
    """Result of a dry-run configuration validation.

    Attributes:
        valid: Whether the patch is valid
        errors: List of validation error messages
        categories: List of affected category names
    """

    valid: bool
    errors: List[str]
    categories: List[str]


class SpaceConfigAuditEvent(BaseModel):
    """A single audit trail event for a configuration change.

    Attributes:
        id: Unique event ID
        space_id: Space ID this event belongs to
        category: Configuration category that was changed
        actor_user_id: User who made the change (null for system changes)
        source: Source of the change (e.g., 'api', 'system')
        patch: The patch that was applied
        previous_value: The previous configuration value
        created_at: ISO 8601 timestamp of when the change occurred
    """

    id: str
    space_id: str
    category: str
    actor_user_id: Optional[str] = None
    source: str
    patch: Dict[str, Any]
    previous_value: Dict[str, Any]
    created_at: str


class SpaceConfigAuditResponse(BaseModel):
    """Paginated audit trail response.

    Attributes:
        events: List of audit events
        total: Total number of events
        limit: Page size
        offset: Page offset
    """

    events: List[SpaceConfigAuditEvent]
    total: int
    limit: int
    offset: int
