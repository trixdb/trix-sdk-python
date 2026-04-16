"""Asynchronous Trix client implementation."""

import logging
import threading
import time
import uuid
from types import TracebackType
from typing import Callable, Dict, List, Optional, Type

import httpx

from . import __api_version__, __version__
from .auth import Auth
from .types import PingResult
from .client_base import (
    ErrorInterceptor,
    PoolConfig,
    RequestContext,
    RequestInterceptor,
    ResponseContext,
    ResponseInterceptor,
)
from .client_transport_async import AsyncTransportMixin
from .resources.agent import AsyncAgentResource
from .resources.bots import AsyncBotsResource
from .resources.habits_async import AsyncHabitsResource
from .resources.clusters_async import AsyncClustersResource
from .resources.enrichments import AsyncEnrichmentsResource
from .resources.entities_async import AsyncEntitiesResource
from .resources.facts_async import AsyncFactsResource
from .resources.feedback import AsyncFeedbackResource
from .resources.goals_async import AsyncGoalsResource
from .resources.graph import AsyncGraphResource
from .resources.highlights import AsyncHighlightsResource
from .resources.memories import AsyncMemoriesResource
from .resources.relationships import AsyncRelationshipsResource
from .resources.resources import AsyncResourcesResource
from .resources.search import AsyncSearchResource
from .resources.sessions_async import AsyncSessionsResource
from .resources.spaces import AsyncSpacesResource
from .resources.personas import AsyncPersonasResource
from .resources.space_config import AsyncSpaceConfigResource
from .resources.tasks_async import AsyncTasksResource
from .resources.webhooks import AsyncWebhooksResource
from .resources.workflows_async import AsyncWorkflowsResource
from .resources.crews import AsyncCrewsResource
from .resources.hubs import AsyncHubsResource
from .resources.hubs_roles import AsyncHubRolesResource
from .resources.files import AsyncFilesResource
from .resources.invites import AsyncInvitesResource
from .resources.notes_async import AsyncNotesResource
from .resources.presets_async import AsyncPresetsResource
from .resources.calendar import AsyncCalendarResource
from .resources.skills import AsyncSkillsResource
from .resources.templates import AsyncTemplatesResource
from .resources.knowledge import AsyncKnowledgeResource
from .utils.retry import RetryConfig
from .utils.security import get_env_credential, validate_base_url, validate_id

logger = logging.getLogger(__name__)


class AsyncTrix(AsyncTransportMixin):
    """Asynchronous Trix client.

    Example:
        >>> async with AsyncTrix.from_env() as client:
        ...     memory = await client.memories.create(content="Important note")
        ...     print(memory.id)
    """

    @classmethod
    def from_env(
        cls,
        env_var: str = "TRIX_API_KEY",
        base_url: Optional[str] = None,
        timeout: float = 30.0,
        max_retries: int = 3,
        retry_config: Optional[RetryConfig] = None,
        pool_config: Optional[PoolConfig] = None,
    ) -> "AsyncTrix":
        """Create an async Trix client using credentials from environment variables.

        Args:
            env_var: Environment variable name for API key
            base_url: Base URL override
            timeout: Request timeout in seconds
            max_retries: Maximum number of retries
            retry_config: Custom retry configuration
            pool_config: Connection pool configuration

        Returns:
            Configured AsyncTrix client
        """
        import os

        api_key = get_env_credential(env_var, required=True)
        base_url = base_url or os.environ.get("TRIX_BASE_URL", "https://api.trixdb.com")

        return cls(
            api_key=api_key,
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
            retry_config=retry_config,
            pool_config=pool_config,
        )

    def __init__(
        self,
        api_key: Optional[str] = None,
        jwt_token: Optional[str] = None,
        base_url: str = "https://api.trixdb.com",
        timeout: float = 30.0,
        max_retries: int = 3,
        retry_config: Optional[RetryConfig] = None,
        pool_config: Optional[PoolConfig] = None,
        allow_insecure: bool = False,
        request_interceptors: Optional[List[RequestInterceptor]] = None,
        response_interceptors: Optional[List[ResponseInterceptor]] = None,
        error_interceptors: Optional[List[ErrorInterceptor]] = None,
    ) -> None:
        """Initialize async Trix client.

        For production use, prefer AsyncTrix.from_env() which reads credentials
        from environment variables.
        """
        self._auth = Auth(api_key=api_key, jwt_token=jwt_token)
        self._base_url = validate_base_url(base_url, allow_http=allow_insecure)
        self._timeout = timeout
        self._retry_config = retry_config or RetryConfig(max_retries=max_retries)
        self._pool_config = pool_config or PoolConfig()
        self._persona_id: Optional[str] = None

        # Initialize interceptors
        self._interceptor_lock = threading.Lock()
        self._request_interceptors: List[RequestInterceptor] = list(request_interceptors or [])
        self._response_interceptors: List[ResponseInterceptor] = list(response_interceptors or [])
        self._error_interceptors: List[ErrorInterceptor] = list(error_interceptors or [])

        # Create async HTTP client with connection pooling
        self._client = httpx.AsyncClient(
            base_url=self._base_url,
            timeout=timeout,
            headers=self._get_headers(),
            limits=self._pool_config.to_httpx_limits(),
        )

        # Initialize async resources
        try:
            self._init_resources()
        except Exception:
            self._close_client_on_init_failure()
            raise

    def _close_client_on_init_failure(self) -> None:
        """Close async client on init failure (sync fallback)."""
        try:
            import asyncio as _aio

            loop = _aio.get_event_loop()
            if loop.is_running():
                loop.create_task(self._client.aclose())
            else:
                loop.run_until_complete(self._client.aclose())
        except RuntimeError:
            pass  # No event loop available; transport will be GC'd

    def _init_resources(self) -> None:
        """Initialize all async resource handlers."""
        self.memories = AsyncMemoriesResource(self)
        self.relationships = AsyncRelationshipsResource(self)
        self.clusters = AsyncClustersResource(self)
        self.spaces = AsyncSpacesResource(self)
        self.personas = AsyncPersonasResource(self)
        self.sessions = AsyncSessionsResource(self)
        self.resources = AsyncResourcesResource(self)
        self.graph = AsyncGraphResource(self)
        self.search = AsyncSearchResource(self)
        self.webhooks = AsyncWebhooksResource(self)
        self.agent = AsyncAgentResource(self)
        self.feedback = AsyncFeedbackResource(self)
        self.highlights = AsyncHighlightsResource(self)
        self.facts = AsyncFactsResource(self)
        self.entities = AsyncEntitiesResource(self)
        self.enrichments = AsyncEnrichmentsResource(self)
        self.tasks = AsyncTasksResource(self)
        self.goals = AsyncGoalsResource(self)
        self.habits = AsyncHabitsResource(self)
        self.bots = AsyncBotsResource(self)
        self.space_config = AsyncSpaceConfigResource(self)
        self.workflows = AsyncWorkflowsResource(self)
        self.invites = AsyncInvitesResource(self)
        self.notes = AsyncNotesResource(self)
        self.skills = AsyncSkillsResource(self)
        self.templates = AsyncTemplatesResource(self)
        self.crews = AsyncCrewsResource(self)
        self.hubs = AsyncHubsResource(self)
        self.hub_roles = AsyncHubRolesResource(self)
        self.files = AsyncFilesResource(self)
        self.presets = AsyncPresetsResource(self)
        self.calendar = AsyncCalendarResource(self)
        self.knowledge = AsyncKnowledgeResource(self)

    def set_persona(self, persona_id: str) -> None:
        """Set the active persona for all subsequent requests."""
        validate_id(persona_id, "persona")
        self._persona_id = persona_id

    def clear_persona(self) -> None:
        """Clear the active persona."""
        self._persona_id = None

    def add_request_interceptor(self, interceptor: RequestInterceptor) -> Callable[[], None]:
        """Add a request interceptor."""
        with self._interceptor_lock:
            self._request_interceptors.append(interceptor)

        def remove() -> None:
            with self._interceptor_lock:
                if interceptor in self._request_interceptors:
                    self._request_interceptors.remove(interceptor)

        return remove

    def add_response_interceptor(self, interceptor: ResponseInterceptor) -> Callable[[], None]:
        """Add a response interceptor."""
        with self._interceptor_lock:
            self._response_interceptors.append(interceptor)

        def remove() -> None:
            with self._interceptor_lock:
                if interceptor in self._response_interceptors:
                    self._response_interceptors.remove(interceptor)

        return remove

    def add_error_interceptor(self, interceptor: ErrorInterceptor) -> Callable[[], None]:
        """Add an error interceptor."""
        with self._interceptor_lock:
            self._error_interceptors.append(interceptor)

        def remove() -> None:
            with self._interceptor_lock:
                if interceptor in self._error_interceptors:
                    self._error_interceptors.remove(interceptor)

        return remove

    def _run_request_interceptors(self, context: RequestContext) -> RequestContext:
        """Run all request interceptors."""
        with self._interceptor_lock:
            interceptors = list(self._request_interceptors)
        ctx = context
        for interceptor in interceptors:
            result = interceptor(ctx)
            if result is not None:
                ctx = result
        return ctx

    def _run_response_interceptors(self, context: ResponseContext) -> ResponseContext:
        """Run all response interceptors."""
        with self._interceptor_lock:
            interceptors = list(self._response_interceptors)
        ctx = context
        for interceptor in interceptors:
            result = interceptor(ctx)
            if result is not None:
                ctx = result
        return ctx

    def _run_error_interceptors(self, error: Exception, request: RequestContext) -> Exception:
        """Run all error interceptors."""
        with self._interceptor_lock:
            interceptors = list(self._error_interceptors)
        err = error
        for interceptor in interceptors:
            err = interceptor(err, request)
        return err

    def _get_headers(self) -> Dict[str, str]:
        """Get request headers with authentication and versioning."""
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": f"trix-python-sdk/{__version__}",
            "X-SDK-Version": __version__,
            "X-API-Version": __api_version__,
        }
        headers.update(self._auth.get_headers())
        headers["X-Correlation-Id"] = uuid.uuid4().hex[:16]
        if self._persona_id:
            headers["X-Persona-Id"] = self._persona_id
        return headers

    async def ping(self) -> PingResult:
        """Async health-check ping against ``GET /v1/health`` (ADR-143)."""
        start = time.monotonic()
        body = await self._request("GET", "/health")
        latency_ms = int((time.monotonic() - start) * 1000)
        status_ok = isinstance(body, dict) and body.get("status") == "ok"
        version = body.get("version") if isinstance(body, dict) else None
        return PingResult(ok=status_ok, version=version, latency_ms=latency_ms)

    async def close(self) -> None:
        """Close the async HTTP client and clear credentials."""
        await self._client.aclose()
        self._auth.clear()
        logger.debug("Async client closed and credentials cleared")

    async def __aenter__(self) -> "AsyncTrix":
        """Async context manager entry."""
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        """Async context manager exit."""
        await self.close()
