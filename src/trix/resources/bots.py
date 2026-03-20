"""Bots resource for Trix SDK."""

import asyncio
import logging
import time
from typing import Any, AsyncIterator, Dict, Iterator, List, Optional

import httpx

from concurrent.futures import ThreadPoolExecutor

from .base import BaseAsyncResource, BaseSyncResource
from ..exceptions import TimeoutError
from ..types.bot import (
    Bot,
    BotCreate,
    BotList,
    BotRun,
    BotRunList,
    BotRunRequest,
    BotRunBatchRequest,
    BotRunBatchResult,
    BotUpdate,
    BotAddSpace,
    BotSpace,
    BotTrigger,
    BotTriggerCreate,
)
from ..types.bot_run_step import BotRunStep, BotRunStreamRequest
from ..utils.security import validate_id
from ..utils.sse import iter_sse_lines, parse_sse_line

logger = logging.getLogger(__name__)


class BotsResource(BaseSyncResource):
    """Resource for managing bots."""

    def create(self, name: str, system_prompt: str, **kwargs: Any) -> Bot:
        """Create a new bot."""
        data = BotCreate(name=name, system_prompt=system_prompt, **kwargs)
        response = self._request("POST", "/bots", json=data.model_dump(exclude_none=True))
        return Bot.model_validate(response)

    def list(
        self, status: Optional[str] = None, limit: int = 100, offset: int = 0,
    ) -> BotList:
        """List all bots."""
        params: Dict[str, Any] = {"limit": limit, "offset": offset}
        if status:
            params["status"] = status
        response = self._request("GET", "/bots", params=params)
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

    def run_stream(
        self,
        bot_id: str,
        message: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
    ) -> Iterator[BotRunStep]:
        """Trigger a bot run with streaming SSE events.

        Yields typed BotRunStep events as they arrive from the server.

        Args:
            bot_id: Bot ID to run
            message: Optional input message
            context: Optional context dict

        Yields:
            BotRunStep events from the streaming response
        """
        data = BotRunStreamRequest(message=message, context=context)
        headers = {"Accept": "text/event-stream"}
        client: httpx.Client = self._client._client
        with client.stream(
            "POST",
            f"/bots/{bot_id}/run",
            json=data.model_dump(exclude_none=True),
            headers=headers,
        ) as response:
            for line in iter_sse_lines(response.iter_bytes(chunk_size=1024)):
                parsed = parse_sse_line(line)
                if parsed is not None:
                    yield BotRunStep.model_validate(parsed)

    def run_and_wait(
        self,
        bot_id: str,
        message: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
        poll_interval: float = 1.0,
        timeout: float = 300.0,
    ) -> BotRun:
        """Trigger a bot run and poll until complete.

        Args:
            bot_id: Bot ID to run
            message: Optional input message
            context: Optional context dict
            poll_interval: Seconds between poll requests (default: 1.0)
            timeout: Maximum seconds to wait (default: 300.0)

        Returns:
            Completed BotRun

        Raises:
            TimeoutError: If run does not complete within timeout
        """
        bot_run = self.run(bot_id, message=message, context=context)
        return self._poll_run(bot_id, bot_run.id, poll_interval, timeout)

    def _poll_run(
        self, bot_id: str, run_id: str, poll_interval: float, timeout: float
    ) -> BotRun:
        """Poll a bot run until it reaches a terminal status."""
        start = time.monotonic()
        terminal_statuses = {"completed", "failed", "cancelled"}
        while True:
            run = self.get_run(bot_id, run_id)
            if run.status in terminal_statuses:
                return run
            elapsed = time.monotonic() - start
            if elapsed + poll_interval > timeout:
                raise TimeoutError(
                    f"Bot run {run_id} did not complete within {timeout}s"
                )
            time.sleep(poll_interval)

    def list_runs(self, bot_id: str, limit: int = 20, offset: int = 0) -> BotRunList:
        """List bot runs."""
        response = self._request(
            "GET", f"/bots/{bot_id}/runs", params={"limit": limit, "offset": offset}
        )
        return BotRunList.model_validate(response)

    def get_run(self, bot_id: str, run_id: str) -> BotRun:
        """Get a specific bot run."""
        response = self._request("GET", f"/bots/{bot_id}/runs/{run_id}")
        return BotRun.model_validate(response)

    def run_batch(self, requests: List[BotRunBatchRequest]) -> List[BotRunBatchResult]:
        """Run multiple bots in parallel using threads.

        Args:
            requests: List of batch run requests.

        Returns:
            List of results (one per request, in order).
        """
        def _run_one(req: BotRunBatchRequest) -> BotRunBatchResult:
            try:
                run = self.run(req.bot_id, message=req.message, context=req.context)
                return BotRunBatchResult(bot_id=req.bot_id, run=run)
            except Exception as e:
                return BotRunBatchResult(bot_id=req.bot_id, error=str(e))

        with ThreadPoolExecutor(max_workers=min(len(requests), 10)) as pool:
            return list(pool.map(_run_one, requests))

    def list_all(self, **params: Any) -> Iterator[Bot]:
        """Iterate over all bots using offset-based pagination."""
        limit = 100
        offset = 0
        while True:
            result = self.list(limit=limit, offset=offset, **params)
            for bot in result.bots:
                yield bot
            if len(result.bots) < limit:
                break
            offset += limit

    def list_runs_all(self, bot_id: str, **params: Any) -> Iterator[BotRun]:
        """Iterate over all runs for a bot using offset-based pagination.

        Args:
            bot_id: Bot ID.

        Yields:
            Individual BotRun objects.
        """
        limit = params.pop("limit", 100)
        offset = params.pop("offset", 0)
        while True:
            result = self.list_runs(bot_id, limit=limit, offset=offset)
            for run in result.runs:
                yield run
            if len(result.runs) < limit:
                break
            offset += limit


class AsyncBotsResource(BaseAsyncResource):
    """Async resource for managing bots."""

    async def create(self, name: str, system_prompt: str, **kwargs: Any) -> Bot:
        """Create a new bot (async)."""
        data = BotCreate(name=name, system_prompt=system_prompt, **kwargs)
        response = await self._request("POST", "/bots", json=data.model_dump(exclude_none=True))
        return Bot.model_validate(response)

    async def list(
        self, status: Optional[str] = None, limit: int = 100, offset: int = 0,
    ) -> BotList:
        """List all bots (async)."""
        params: Dict[str, Any] = {"limit": limit, "offset": offset}
        if status:
            params["status"] = status
        response = await self._request("GET", "/bots", params=params)
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

    async def run_stream(
        self,
        bot_id: str,
        message: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
    ) -> AsyncIterator[BotRunStep]:
        """Stream bot run events via SSE (async)."""
        data = BotRunStreamRequest(message=message, context=context)
        headers = {"Accept": "text/event-stream"}
        client: httpx.AsyncClient = self._client._client
        async with client.stream(
            "POST",
            f"/bots/{bot_id}/run",
            json=data.model_dump(exclude_none=True),
            headers=headers,
        ) as response:
            buffer = ""
            async for chunk in response.aiter_bytes(chunk_size=1024):
                buffer += chunk.decode("utf-8", errors="replace")
                while "\n" in buffer:
                    line, buffer = buffer.split("\n", 1)
                    if not line.strip():
                        continue
                    parsed = parse_sse_line(line)
                    if parsed is not None:
                        yield BotRunStep.model_validate(parsed)

    async def run_and_wait(
        self,
        bot_id: str,
        message: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
        poll_interval: float = 1.0,
        timeout: float = 300.0,
    ) -> BotRun:
        """Trigger a bot run and poll until complete (async)."""
        bot_run = await self.run(bot_id, message=message, context=context)
        return await self._poll_run(bot_id, bot_run.id, poll_interval, timeout)

    async def _poll_run(
        self, bot_id: str, run_id: str, poll_interval: float, timeout: float
    ) -> BotRun:
        """Poll a bot run until it reaches a terminal status (async)."""
        start = time.monotonic()
        terminal_statuses = {"completed", "failed", "cancelled"}
        while True:
            run = await self.get_run(bot_id, run_id)
            if run.status in terminal_statuses:
                return run
            elapsed = time.monotonic() - start
            if elapsed + poll_interval > timeout:
                raise TimeoutError(
                    f"Bot run {run_id} did not complete within {timeout}s"
                )
            await asyncio.sleep(poll_interval)

    async def list_runs(self, bot_id: str, limit: int = 20, offset: int = 0) -> BotRunList:
        """List bot runs (async)."""
        response = await self._request(
            "GET", f"/bots/{bot_id}/runs", params={"limit": limit, "offset": offset}
        )
        return BotRunList.model_validate(response)

    async def get_run(self, bot_id: str, run_id: str) -> BotRun:
        """Get a specific bot run (async)."""
        response = await self._request("GET", f"/bots/{bot_id}/runs/{run_id}")
        return BotRun.model_validate(response)

    async def run_batch(self, requests: List[BotRunBatchRequest]) -> List[BotRunBatchResult]:
        """Run multiple bots in parallel using asyncio.gather (async)."""
        async def _run_one(req: BotRunBatchRequest) -> BotRunBatchResult:
            try:
                run = await self.run(req.bot_id, message=req.message, context=req.context)
                return BotRunBatchResult(bot_id=req.bot_id, run=run)
            except Exception as e:
                return BotRunBatchResult(bot_id=req.bot_id, error=str(e))

        return list(await asyncio.gather(*[_run_one(r) for r in requests]))

    async def list_all(self, **params: Any) -> AsyncIterator[Bot]:
        """Iterate over all bots with auto-pagination (async)."""
        limit = 100
        offset = 0
        while True:
            result = await self.list(limit=limit, offset=offset, **params)
            for bot in result.bots:
                yield bot
            if len(result.bots) < limit:
                break
            offset += limit

    async def list_runs_all(self, bot_id: str, **params: Any) -> AsyncIterator[BotRun]:
        """Iterate over all runs with auto-pagination (async)."""
        limit = params.pop("limit", 100)
        offset = params.pop("offset", 0)
        while True:
            result = await self.list_runs(bot_id, limit=limit, offset=offset)
            for run in result.runs:
                yield run
            if len(result.runs) < limit:
                break
            offset += limit
