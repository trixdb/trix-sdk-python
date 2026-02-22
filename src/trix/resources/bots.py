"""Bots resource for Trix SDK."""

from typing import Any, Dict, List, Optional

from .base import BaseAsyncResource, BaseSyncResource
from ..types.bot import (
    Bot,
    BotCreate,
    BotList,
    BotRun,
    BotRunList,
    BotRunRequest,
    BotUpdate,
    BotAddSpace,
    BotSpace,
    BotTrigger,
    BotTriggerCreate,
)
from ..utils.security import validate_id


class BotsResource(BaseSyncResource):
    """Resource for managing bots."""

    def create(self, name: str, system_prompt: str, **kwargs: Any) -> Bot:
        """Create a new bot."""
        data = BotCreate(name=name, system_prompt=system_prompt, **kwargs)
        response = self._request("POST", "/bots", json=data.model_dump(exclude_none=True))
        return Bot.model_validate(response)

    def list(self, status: Optional[str] = None) -> BotList:
        """List all bots."""
        params: Dict[str, Any] = {}
        if status:
            params["status"] = status
        response = self._request("GET", "/bots", params=params or None)
        return BotList.model_validate(response)

    def get(self, id_or_slug: str) -> Bot:
        """Get a bot by ID or slug."""
        response = self._request("GET", f"/bots/{id_or_slug}")
        return Bot.model_validate(response)

    def update(self, id: str, **kwargs: Any) -> Bot:
        """Update a bot."""
        validate_id(id, "bot")
        data = BotUpdate(**kwargs)
        response = self._request(
            "PATCH", f"/bots/{id}", json=data.model_dump(exclude_none=True)
        )
        return Bot.model_validate(response)

    def delete(self, id: str) -> None:
        """Delete a bot."""
        validate_id(id, "bot")
        self._request("DELETE", f"/bots/{id}")

    def add_space(self, bot_id: str, space_id: str, permission: str = "read") -> BotSpace:
        """Grant space access to a bot."""
        validate_id(bot_id, "bot")
        data = BotAddSpace(space_id=space_id, permission=permission)
        response = self._request("POST", f"/bots/{bot_id}/spaces", json=data.model_dump())
        return BotSpace.model_validate(response)

    def remove_space(self, bot_id: str, space_id: str) -> None:
        """Revoke space access from a bot."""
        validate_id(bot_id, "bot")
        validate_id(space_id, "space")
        self._request("DELETE", f"/bots/{bot_id}/spaces/{space_id}")

    def add_trigger(self, bot_id: str, type: str, **kwargs: Any) -> BotTrigger:
        """Add a trigger to a bot."""
        validate_id(bot_id, "bot")
        data = BotTriggerCreate(type=type, **kwargs)
        response = self._request(
            "POST", f"/bots/{bot_id}/triggers", json=data.model_dump(exclude_none=True)
        )
        return BotTrigger.model_validate(response)

    def remove_trigger(self, bot_id: str, trigger_id: str) -> None:
        """Remove a trigger from a bot."""
        validate_id(bot_id, "bot")
        self._request("DELETE", f"/bots/{bot_id}/triggers/{trigger_id}")

    def run(
        self, bot_id: str, message: Optional[str] = None, context: Optional[Dict[str, Any]] = None
    ) -> BotRun:
        """Trigger a bot run."""
        data = BotRunRequest(message=message, context=context)
        response = self._request(
            "POST", f"/bots/{bot_id}/run", json=data.model_dump(exclude_none=True)
        )
        return BotRun.model_validate(response)

    def list_runs(
        self, bot_id: str, limit: int = 20, offset: int = 0
    ) -> BotRunList:
        """List bot runs."""
        response = self._request(
            "GET", f"/bots/{bot_id}/runs", params={"limit": limit, "offset": offset}
        )
        return BotRunList.model_validate(response)

    def get_run(self, bot_id: str, run_id: str) -> BotRun:
        """Get a specific bot run."""
        response = self._request("GET", f"/bots/{bot_id}/runs/{run_id}")
        return BotRun.model_validate(response)


class AsyncBotsResource(BaseAsyncResource):
    """Async resource for managing bots."""

    async def create(self, name: str, system_prompt: str, **kwargs: Any) -> Bot:
        """Create a new bot (async)."""
        data = BotCreate(name=name, system_prompt=system_prompt, **kwargs)
        response = await self._request("POST", "/bots", json=data.model_dump(exclude_none=True))
        return Bot.model_validate(response)

    async def list(self, status: Optional[str] = None) -> BotList:
        """List all bots (async)."""
        params: Dict[str, Any] = {}
        if status:
            params["status"] = status
        response = await self._request("GET", "/bots", params=params or None)
        return BotList.model_validate(response)

    async def get(self, id_or_slug: str) -> Bot:
        """Get a bot by ID or slug (async)."""
        response = await self._request("GET", f"/bots/{id_or_slug}")
        return Bot.model_validate(response)

    async def update(self, id: str, **kwargs: Any) -> Bot:
        """Update a bot (async)."""
        validate_id(id, "bot")
        data = BotUpdate(**kwargs)
        response = await self._request(
            "PATCH", f"/bots/{id}", json=data.model_dump(exclude_none=True)
        )
        return Bot.model_validate(response)

    async def delete(self, id: str) -> None:
        """Delete a bot (async)."""
        validate_id(id, "bot")
        await self._request("DELETE", f"/bots/{id}")

    async def add_space(self, bot_id: str, space_id: str, permission: str = "read") -> BotSpace:
        """Grant space access to a bot (async)."""
        validate_id(bot_id, "bot")
        data = BotAddSpace(space_id=space_id, permission=permission)
        response = await self._request("POST", f"/bots/{bot_id}/spaces", json=data.model_dump())
        return BotSpace.model_validate(response)

    async def remove_space(self, bot_id: str, space_id: str) -> None:
        """Revoke space access from a bot (async)."""
        validate_id(bot_id, "bot")
        validate_id(space_id, "space")
        await self._request("DELETE", f"/bots/{bot_id}/spaces/{space_id}")

    async def add_trigger(self, bot_id: str, type: str, **kwargs: Any) -> BotTrigger:
        """Add a trigger to a bot (async)."""
        validate_id(bot_id, "bot")
        data = BotTriggerCreate(type=type, **kwargs)
        response = await self._request(
            "POST", f"/bots/{bot_id}/triggers", json=data.model_dump(exclude_none=True)
        )
        return BotTrigger.model_validate(response)

    async def remove_trigger(self, bot_id: str, trigger_id: str) -> None:
        """Remove a trigger from a bot (async)."""
        validate_id(bot_id, "bot")
        await self._request("DELETE", f"/bots/{bot_id}/triggers/{trigger_id}")

    async def run(
        self, bot_id: str, message: Optional[str] = None, context: Optional[Dict[str, Any]] = None
    ) -> BotRun:
        """Trigger a bot run (async)."""
        data = BotRunRequest(message=message, context=context)
        response = await self._request(
            "POST", f"/bots/{bot_id}/run", json=data.model_dump(exclude_none=True)
        )
        return BotRun.model_validate(response)

    async def list_runs(
        self, bot_id: str, limit: int = 20, offset: int = 0
    ) -> BotRunList:
        """List bot runs (async)."""
        response = await self._request(
            "GET", f"/bots/{bot_id}/runs", params={"limit": limit, "offset": offset}
        )
        return BotRunList.model_validate(response)

    async def get_run(self, bot_id: str, run_id: str) -> BotRun:
        """Get a specific bot run (async)."""
        response = await self._request("GET", f"/bots/{bot_id}/runs/{run_id}")
        return BotRun.model_validate(response)
