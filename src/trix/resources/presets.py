"""Agent presets resource for Trix SDK."""

from typing import Any, Dict, Optional

from .base import BaseSyncResource
from ..types.preset import (
    AgentPreset,
    AgentPresetCreate,
    AgentPresetList,
    AgentPresetUpdate,
)
from ..utils.security import validate_id


class PresetsResource(BaseSyncResource):
    """Resource for managing agent presets.

    Agent presets define execution configurations for AI agents,
    including model selection, tool access, and budget controls.

    Example:
        >>> preset = client.presets.create(
        ...     name="Fast Research",
        ...     provider="openai",
        ...     model="gpt-4.1",
        ... )
    """

    def list(self, include_system: Optional[bool] = None) -> AgentPresetList:
        """List all agent presets.

        Args:
            include_system: Whether to include system presets (default: True)
        """
        params: Dict[str, Any] = {}
        if include_system is not None:
            params["include_system"] = include_system
        response = self._request("GET", "/agent-presets", params=params)
        return AgentPresetList.model_validate(response)

    def get(self, id_or_slug: str) -> AgentPreset:
        """Get an agent preset by ID or slug."""
        response = self._request("GET", f"/agent-presets/{id_or_slug}")
        return AgentPreset.model_validate(response.get("preset", response))

    def create(self, name: str, **kwargs: Any) -> AgentPreset:
        """Create a new agent preset."""
        data = AgentPresetCreate(name=name, **kwargs)
        response = self._request("POST", "/agent-presets", json=data.model_dump(exclude_none=True))
        return AgentPreset.model_validate(response.get("preset", response))

    def update(self, id: str, **kwargs: Any) -> AgentPreset:
        """Update an agent preset."""
        validate_id(id, "preset")
        data = AgentPresetUpdate(**kwargs)
        response = self._request(
            "PATCH", f"/agent-presets/{id}", json=data.model_dump(exclude_none=True)
        )
        return AgentPreset.model_validate(response.get("preset", response))

    def delete(self, id: str) -> None:
        """Delete an agent preset."""
        validate_id(id, "preset")
        self._request("DELETE", f"/agent-presets/{id}")
