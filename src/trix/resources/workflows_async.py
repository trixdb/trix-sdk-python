"""Async workflows resource for Trix SDK."""

from typing import Any, Dict, List, Optional

from .base import BaseAsyncResource
from ..types.workflow import (
    TriggerCreate,
    TriggerUpdate,
    Workflow,
    WorkflowCreate,
    WorkflowList,
    WorkflowRun,
    WorkflowRunList,
    WorkflowTrigger,
    WorkflowUpdate,
)
from ..utils.security import validate_id


class AsyncWorkflowsResource(BaseAsyncResource):
    """Async resource for managing workflows.

    Example:
        >>> workflow = await client.workflows.create(
        ...     name="Daily Summary",
        ...     steps=[{"type": "summarize", "config": {}}],
        ... )
        >>> await client.workflows.trigger(workflow.id)
    """

    async def create(
        self,
        name: str,
        description: Optional[str] = None,
        space_id: Optional[str] = None,
        steps: Optional[List[Dict[str, Any]]] = None,
        trigger: Optional[Dict[str, Any]] = None,
    ) -> Workflow:
        """Create a new workflow (async)."""
        data = WorkflowCreate(
            name=name,
            description=description,
            space_id=space_id,
            steps=steps or [],
            trigger=trigger,
        )
        response = await self._request(
            "POST", "/workflows", json=data.model_dump(exclude_none=True)
        )
        return Workflow.model_validate(response)

    async def list(
        self,
        status: Optional[str] = None,
        space_id: Optional[str] = None,
        limit: int = 20,
        offset: int = 0,
    ) -> WorkflowList:
        """List workflows with optional filtering (async)."""
        params: Dict[str, Any] = {"limit": limit, "offset": offset}
        if status is not None:
            params["status"] = status
        if space_id is not None:
            params["spaceId"] = space_id
        response = await self._request("GET", "/workflows", params=params)
        return WorkflowList.model_validate(response)

    async def get(self, workflow_id: str) -> Workflow:
        """Get a workflow by ID (async)."""
        validate_id(workflow_id, "workflow")
        response = await self._request("GET", f"/workflows/{workflow_id}")
        return Workflow.model_validate(response)

    async def update(
        self,
        workflow_id: str,
        version: int,
        name: Optional[str] = None,
        description: Optional[str] = None,
        status: Optional[str] = None,
        trigger: Optional[Dict[str, Any]] = None,
        steps: Optional[List[Dict[str, Any]]] = None,
    ) -> Workflow:
        """Update a workflow (async)."""
        validate_id(workflow_id, "workflow")
        data = WorkflowUpdate(
            version=version,
            name=name,
            description=description,
            status=status,
            trigger=trigger,
            steps=steps,
        )
        response = await self._request(
            "PATCH", f"/workflows/{workflow_id}", json=data.model_dump(exclude_none=True)
        )
        return Workflow.model_validate(response)

    async def delete(self, workflow_id: str) -> None:
        """Delete a workflow (async)."""
        validate_id(workflow_id, "workflow")
        await self._request("DELETE", f"/workflows/{workflow_id}")

    async def trigger(
        self,
        workflow_id: str,
        input: Optional[Dict[str, Any]] = None,
    ) -> WorkflowRun:
        """Trigger a workflow run (async)."""
        validate_id(workflow_id, "workflow")
        body: Dict[str, Any] = {}
        if input is not None:
            body["input"] = input
        response = await self._request("POST", f"/workflows/{workflow_id}/trigger", json=body)
        return WorkflowRun.model_validate(response)

    async def list_runs(
        self,
        workflow_id: str,
        limit: int = 20,
        offset: int = 0,
    ) -> WorkflowRunList:
        """List runs for a workflow (async)."""
        validate_id(workflow_id, "workflow")
        params: Dict[str, Any] = {"limit": limit, "offset": offset}
        response = await self._request("GET", f"/workflows/{workflow_id}/runs", params=params)
        return WorkflowRunList.model_validate(response)

    async def list_triggers(self, workflow_id: str) -> List[WorkflowTrigger]:
        """List triggers for a workflow (async)."""
        validate_id(workflow_id, "workflow")
        response = await self._request("GET", f"/workflows/{workflow_id}/triggers")
        return [WorkflowTrigger.model_validate(t) for t in response]

    async def create_trigger(
        self,
        workflow_id: str,
        type: str,
        cron_expression: Optional[str] = None,
        timezone: Optional[str] = None,
        event_types: Optional[List[str]] = None,
        event_filter: Optional[Dict[str, Any]] = None,
        enabled: Optional[bool] = None,
    ) -> WorkflowTrigger:
        """Create a trigger for a workflow (async)."""
        validate_id(workflow_id, "workflow")
        data = TriggerCreate(
            type=type,
            cron_expression=cron_expression,
            timezone=timezone,
            event_types=event_types,
            event_filter=event_filter,
            enabled=enabled,
        )
        response = await self._request(
            "POST",
            f"/workflows/{workflow_id}/triggers",
            json=data.model_dump(exclude_none=True),
        )
        return WorkflowTrigger.model_validate(response)

    async def update_trigger(
        self,
        workflow_id: str,
        trigger_id: str,
        cron_expression: Optional[str] = None,
        timezone: Optional[str] = None,
        event_types: Optional[List[str]] = None,
        event_filter: Optional[Dict[str, Any]] = None,
        enabled: Optional[bool] = None,
    ) -> WorkflowTrigger:
        """Update a workflow trigger (async)."""
        validate_id(workflow_id, "workflow")
        validate_id(trigger_id, "trigger")
        data = TriggerUpdate(
            cron_expression=cron_expression,
            timezone=timezone,
            event_types=event_types,
            event_filter=event_filter,
            enabled=enabled,
        )
        response = await self._request(
            "PATCH",
            f"/workflows/{workflow_id}/triggers/{trigger_id}",
            json=data.model_dump(exclude_none=True),
        )
        return WorkflowTrigger.model_validate(response)

    async def delete_trigger(self, workflow_id: str, trigger_id: str) -> None:
        """Delete a workflow trigger (async)."""
        validate_id(workflow_id, "workflow")
        validate_id(trigger_id, "trigger")
        await self._request("DELETE", f"/workflows/{workflow_id}/triggers/{trigger_id}")
