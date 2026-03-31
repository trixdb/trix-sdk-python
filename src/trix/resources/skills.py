"""Skills resource for Trix SDK."""

from typing import Any, Dict, List, Optional

from .base import BaseAsyncResource, BaseSyncResource
from ..types.skill import (
    BotSkillAttachment,
    Skill,
    SkillCreate,
    SkillList,
    SkillUpdate,
)
from ..utils.security import validate_id


class SkillsResource(BaseSyncResource):
    """Resource for managing reusable instruction packages.

    Example:
        >>> skill = client.skills.create(
        ...     name="code-review",
        ...     description="Review code for best practices.",
        ...     content="# Code Review Instructions...",
        ... )
        >>> client.skills.attach_to_bot(skill.id, bot_id="bot-uuid")
    """

    def create(
        self,
        name: str,
        description: Optional[str] = None,
        content: Optional[str] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Skill:
        """Create a new skill."""
        data = SkillCreate(
            name=name,
            description=description,
            content=content,
            tags=tags,
            metadata=metadata,
        )
        response = self._request("POST", "/skills", json=data.model_dump(exclude_none=True))
        return Skill.model_validate(response)

    def list(
        self,
        limit: int = 50,
        offset: int = 0,
    ) -> List[Skill]:
        """List skills."""
        params: Dict[str, Any] = {"limit": limit, "offset": offset}
        response = self._request("GET", "/skills", params=params)
        result = SkillList.model_validate(response)
        return result.skills

    def get(self, id_or_slug: str) -> Skill:
        """Get a skill by ID or slug."""
        response = self._request("GET", f"/skills/{id_or_slug}")
        return Skill.model_validate(response)

    def update(
        self,
        skill_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        content: Optional[str] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Skill:
        """Update a skill."""
        validate_id(skill_id, "skill")
        data = SkillUpdate(
            name=name,
            description=description,
            content=content,
            tags=tags,
            metadata=metadata,
        )
        response = self._request(
            "PATCH", f"/skills/{skill_id}", json=data.model_dump(exclude_none=True)
        )
        return Skill.model_validate(response)

    def delete(self, skill_id: str) -> None:
        """Delete a skill."""
        validate_id(skill_id, "skill")
        self._request("DELETE", f"/skills/{skill_id}")

    def publish(self, skill_id: str) -> Skill:
        """Publish a skill to the marketplace."""
        validate_id(skill_id, "skill")
        response = self._request("POST", f"/skills/{skill_id}/publish")
        return Skill.model_validate(response)

    def install(self, skill_id: str) -> Skill:
        """Install a skill from the marketplace."""
        validate_id(skill_id, "skill")
        response = self._request("POST", f"/skills/{skill_id}/install")
        return Skill.model_validate(response)

    def marketplace(
        self,
        q: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> List[Skill]:
        """Search the skill marketplace."""
        params: Dict[str, Any] = {"limit": limit, "offset": offset}
        if q is not None:
            params["q"] = q
        response = self._request("GET", "/skills/marketplace", params=params)
        result = SkillList.model_validate(response)
        return result.skills

    def attach_to_bot(
        self,
        skill_id: str,
        bot_id: str,
        enabled: bool = True,
        priority: Optional[int] = None,
        config: Optional[Dict[str, Any]] = None,
    ) -> BotSkillAttachment:
        """Attach a skill to a bot."""
        validate_id(skill_id, "skill")
        body: Dict[str, Any] = {"bot_id": bot_id, "enabled": enabled}
        if priority is not None:
            body["priority"] = priority
        if config is not None:
            body["config"] = config
        response = self._request("POST", f"/skills/{skill_id}/bots", json=body)
        return BotSkillAttachment.model_validate(response)

    def detach_from_bot(self, skill_id: str, bot_id: str) -> None:
        """Detach a skill from a bot."""
        validate_id(skill_id, "skill")
        validate_id(bot_id, "bot")
        self._request("DELETE", f"/skills/{skill_id}/bots/{bot_id}")

    def list_bots(self, skill_id: str) -> List[BotSkillAttachment]:
        """List bots attached to a skill."""
        validate_id(skill_id, "skill")
        response = self._request("GET", f"/skills/{skill_id}/bots")
        return [BotSkillAttachment.model_validate(b) for b in response.get("bots", [])]


class AsyncSkillsResource(BaseAsyncResource):
    """Async resource for managing reusable instruction packages."""

    async def create(
        self,
        name: str,
        description: Optional[str] = None,
        content: Optional[str] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Skill:
        """Create a new skill (async)."""
        data = SkillCreate(
            name=name,
            description=description,
            content=content,
            tags=tags,
            metadata=metadata,
        )
        response = await self._request("POST", "/skills", json=data.model_dump(exclude_none=True))
        return Skill.model_validate(response)

    async def list(
        self,
        limit: int = 50,
        offset: int = 0,
    ) -> List[Skill]:
        """List skills (async)."""
        params: Dict[str, Any] = {"limit": limit, "offset": offset}
        response = await self._request("GET", "/skills", params=params)
        result = SkillList.model_validate(response)
        return result.skills

    async def get(self, id_or_slug: str) -> Skill:
        """Get a skill by ID or slug (async)."""
        response = await self._request("GET", f"/skills/{id_or_slug}")
        return Skill.model_validate(response)

    async def update(
        self,
        skill_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        content: Optional[str] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Skill:
        """Update a skill (async)."""
        validate_id(skill_id, "skill")
        data = SkillUpdate(
            name=name,
            description=description,
            content=content,
            tags=tags,
            metadata=metadata,
        )
        response = await self._request(
            "PATCH", f"/skills/{skill_id}", json=data.model_dump(exclude_none=True)
        )
        return Skill.model_validate(response)

    async def delete(self, skill_id: str) -> None:
        """Delete a skill (async)."""
        validate_id(skill_id, "skill")
        await self._request("DELETE", f"/skills/{skill_id}")

    async def publish(self, skill_id: str) -> Skill:
        """Publish a skill to the marketplace (async)."""
        validate_id(skill_id, "skill")
        response = await self._request("POST", f"/skills/{skill_id}/publish")
        return Skill.model_validate(response)

    async def install(self, skill_id: str) -> Skill:
        """Install a skill from the marketplace (async)."""
        validate_id(skill_id, "skill")
        response = await self._request("POST", f"/skills/{skill_id}/install")
        return Skill.model_validate(response)

    async def marketplace(
        self,
        q: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> List[Skill]:
        """Search the skill marketplace (async)."""
        params: Dict[str, Any] = {"limit": limit, "offset": offset}
        if q is not None:
            params["q"] = q
        response = await self._request("GET", "/skills/marketplace", params=params)
        result = SkillList.model_validate(response)
        return result.skills

    async def attach_to_bot(
        self,
        skill_id: str,
        bot_id: str,
        enabled: bool = True,
        priority: Optional[int] = None,
        config: Optional[Dict[str, Any]] = None,
    ) -> BotSkillAttachment:
        """Attach a skill to a bot (async)."""
        validate_id(skill_id, "skill")
        body: Dict[str, Any] = {"bot_id": bot_id, "enabled": enabled}
        if priority is not None:
            body["priority"] = priority
        if config is not None:
            body["config"] = config
        response = await self._request("POST", f"/skills/{skill_id}/bots", json=body)
        return BotSkillAttachment.model_validate(response)

    async def detach_from_bot(self, skill_id: str, bot_id: str) -> None:
        """Detach a skill from a bot (async)."""
        validate_id(skill_id, "skill")
        validate_id(bot_id, "bot")
        await self._request("DELETE", f"/skills/{skill_id}/bots/{bot_id}")

    async def list_bots(self, skill_id: str) -> List[BotSkillAttachment]:
        """List bots attached to a skill (async)."""
        validate_id(skill_id, "skill")
        response = await self._request("GET", f"/skills/{skill_id}/bots")
        return [BotSkillAttachment.model_validate(b) for b in response.get("bots", [])]
