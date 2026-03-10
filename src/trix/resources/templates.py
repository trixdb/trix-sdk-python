"""Templates resource for Trix SDK (ADR-067 Phase 5)."""

from typing import Any, Dict, Optional

from .base import BaseAsyncResource, BaseSyncResource
from ..types.template import (
    Template,
    TemplateCreate,
    TemplateInstallResult,
    TemplateList,
    TemplateReview,
    TemplateReviewCreate,
    TemplateUpdate,
)
from ..utils.security import validate_id


class TemplatesResource(BaseSyncResource):
    """Resource for managing bot/agent templates."""

    def create(self, name: str, **kwargs: Any) -> Template:
        """Create a new template."""
        data = TemplateCreate(name=name, **kwargs)
        response = self._request("POST", "/templates", json=data.model_dump(exclude_none=True))
        return Template.model_validate(response)

    def list(
        self,
        category: Optional[str] = None,
        status: Optional[str] = None,
        limit: int = 20,
        offset: int = 0,
    ) -> TemplateList:
        """List templates with optional filtering."""
        params: Dict[str, Any] = {"limit": limit, "offset": offset}
        if category is not None:
            params["category"] = category
        if status is not None:
            params["status"] = status
        response = self._request("GET", "/templates", params=params)
        return TemplateList.model_validate(response)

    def get(self, template_id: str) -> Template:
        """Get a template by ID."""
        validate_id(template_id, "template")
        response = self._request("GET", f"/templates/{template_id}")
        return Template.model_validate(response)

    def update(self, template_id: str, **kwargs: Any) -> Template:
        """Update a template."""
        validate_id(template_id, "template")
        data = TemplateUpdate(**kwargs)
        response = self._request(
            "PATCH", f"/templates/{template_id}", json=data.model_dump(exclude_none=True)
        )
        return Template.model_validate(response)

    def delete(self, template_id: str) -> None:
        """Delete a template."""
        validate_id(template_id, "template")
        self._request("DELETE", f"/templates/{template_id}")

    def browse(
        self,
        category: Optional[str] = None,
        q: Optional[str] = None,
        sort: Optional[str] = None,
        limit: int = 20,
        offset: int = 0,
    ) -> TemplateList:
        """Browse marketplace templates."""
        params: Dict[str, Any] = {"limit": limit, "offset": offset}
        if category is not None:
            params["category"] = category
        if q is not None:
            params["q"] = q
        if sort is not None:
            params["sort"] = sort
        response = self._request("GET", "/templates/marketplace", params=params)
        return TemplateList.model_validate(response)

    def install(self, template_id: str) -> TemplateInstallResult:
        """Install a marketplace template as a bot."""
        validate_id(template_id, "template")
        response = self._request("POST", f"/templates/{template_id}/install")
        return TemplateInstallResult.model_validate(response)

    def review(self, template_id: str, rating: int, comment: Optional[str] = None) -> TemplateReview:
        """Submit a review for a template."""
        validate_id(template_id, "template")
        data = TemplateReviewCreate(rating=rating, comment=comment)
        response = self._request(
            "POST", f"/templates/{template_id}/reviews", json=data.model_dump(exclude_none=True)
        )
        return TemplateReview.model_validate(response)

    def marketplace(
        self,
        category: Optional[str] = None,
        sort: Optional[str] = None,
        limit: int = 20,
    ) -> TemplateList:
        """Browse marketplace templates with convenience parameters.

        Args:
            category: Optional category filter.
            sort: Sort order (e.g. 'popular', 'recent', 'rating').
            limit: Maximum results to return.

        Returns:
            TemplateList with matching marketplace templates.
        """
        return self.browse(category=category, sort=sort, limit=limit)


class AsyncTemplatesResource(BaseAsyncResource):
    """Async resource for managing bot/agent templates."""

    async def create(self, name: str, **kwargs: Any) -> Template:
        """Create a new template (async)."""
        data = TemplateCreate(name=name, **kwargs)
        response = await self._request(
            "POST", "/templates", json=data.model_dump(exclude_none=True)
        )
        return Template.model_validate(response)

    async def list(
        self,
        category: Optional[str] = None,
        status: Optional[str] = None,
        limit: int = 20,
        offset: int = 0,
    ) -> TemplateList:
        """List templates with optional filtering (async)."""
        params: Dict[str, Any] = {"limit": limit, "offset": offset}
        if category is not None:
            params["category"] = category
        if status is not None:
            params["status"] = status
        response = await self._request("GET", "/templates", params=params)
        return TemplateList.model_validate(response)

    async def get(self, template_id: str) -> Template:
        """Get a template by ID (async)."""
        validate_id(template_id, "template")
        response = await self._request("GET", f"/templates/{template_id}")
        return Template.model_validate(response)

    async def update(self, template_id: str, **kwargs: Any) -> Template:
        """Update a template (async)."""
        validate_id(template_id, "template")
        data = TemplateUpdate(**kwargs)
        response = await self._request(
            "PATCH", f"/templates/{template_id}", json=data.model_dump(exclude_none=True)
        )
        return Template.model_validate(response)

    async def delete(self, template_id: str) -> None:
        """Delete a template (async)."""
        validate_id(template_id, "template")
        await self._request("DELETE", f"/templates/{template_id}")

    async def browse(
        self,
        category: Optional[str] = None,
        q: Optional[str] = None,
        sort: Optional[str] = None,
        limit: int = 20,
        offset: int = 0,
    ) -> TemplateList:
        """Browse marketplace templates (async)."""
        params: Dict[str, Any] = {"limit": limit, "offset": offset}
        if category is not None:
            params["category"] = category
        if q is not None:
            params["q"] = q
        if sort is not None:
            params["sort"] = sort
        response = await self._request("GET", "/templates/marketplace", params=params)
        return TemplateList.model_validate(response)

    async def install(self, template_id: str) -> TemplateInstallResult:
        """Install a marketplace template as a bot (async)."""
        validate_id(template_id, "template")
        response = await self._request("POST", f"/templates/{template_id}/install")
        return TemplateInstallResult.model_validate(response)

    async def review(
        self, template_id: str, rating: int, comment: Optional[str] = None
    ) -> TemplateReview:
        """Submit a review for a template (async)."""
        validate_id(template_id, "template")
        data = TemplateReviewCreate(rating=rating, comment=comment)
        response = await self._request(
            "POST",
            f"/templates/{template_id}/reviews",
            json=data.model_dump(exclude_none=True),
        )
        return TemplateReview.model_validate(response)

    async def marketplace(
        self,
        category: Optional[str] = None,
        sort: Optional[str] = None,
        limit: int = 20,
    ) -> TemplateList:
        """Browse marketplace templates with convenience parameters (async).

        Args:
            category: Optional category filter.
            sort: Sort order (e.g. 'popular', 'recent', 'rating').
            limit: Maximum results to return.

        Returns:
            TemplateList with matching marketplace templates.
        """
        return await self.browse(category=category, sort=sort, limit=limit)
