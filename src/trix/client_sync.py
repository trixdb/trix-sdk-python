"""Synchronous Trix client implementation."""

import logging
import threading
import uuid
from types import TracebackType
from typing import Callable, Dict, List, Optional, Type

import httpx

from . import __api_version__, __version__
from .auth import Auth
from .client_base import (
    ErrorInterceptor,
    PoolConfig,
    RequestContext,
    RequestInterceptor,
    ResponseContext,
    ResponseInterceptor,
)
from .client_transport import SyncTransportMixin
from .resources import (
    AgentResource,
    ClustersResource,
    EnrichmentsResource,
    EntitiesResource,
    FactsResource,
    FeedbackResource,
    GraphResource,
    HighlightsResource,
    MemoriesResource,
    RelationshipsResource,
    ResourcesResource,
    SearchResource,
    SessionsResource,
    SpacesResource,
    TasksResource,
    WebhooksResource,
)
from .resources.bots import BotsResource
from .resources.goals import GoalsResource
from .resources.habits import HabitsResource
from .resources.personas import PersonasResource
from .resources.space_config import SpaceConfigResource
from .resources.workflows import WorkflowsResource
from .resources.invites import InvitesResource
from .resources.notes import NotesResource
from .resources.skills import SkillsResource
from .resources.templates import TemplatesResource
from .resources.crews import CrewsResource
from .resources.hubs import HubsResource
from .resources.hubs_roles import HubRolesResource
from .resources.files import FilesResource
from .resources.presets import PresetsResource
from .resources.calendar import CalendarResource
from .resources.knowledge import KnowledgeResource
from .utils.retry import RetryConfig
from .utils.security import get_env_credential, validate_base_url, validate_id

logger = logging.getLogger(__name__)


class Trix(SyncTransportMixin):
    """Synchronous Trix client.

    Example:
        >>> # Using environment variable (recommended)
        >>> client = Trix.from_env()
        >>>
        >>> # Or with explicit API key
        >>> client = Trix(api_key="your_api_key")
        >>> memory = client.memories.create(content="Important note")
        >>> print(memory.id)
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
    ) -> "Trix":
        """Create a Trix client using credentials from environment variables.

        Args:
            env_var: Environment variable name for API key
            base_url: Base URL override
            timeout: Request timeout in seconds
            max_retries: Maximum number of retries
            retry_config: Custom retry configuration
            pool_config: Connection pool configuration

        Returns:
            Configured Trix client
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
        """Initialize Trix client.

        For production use, prefer Trix.from_env() which reads credentials
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

        # Create HTTP client with connection pooling
        self._client = httpx.Client(
            base_url=self._base_url,
            timeout=timeout,
            headers=self._get_headers(),
            limits=self._pool_config.to_httpx_limits(),
        )

        # Initialize resources
        try:
            self._init_resources()
        except Exception:
            self._client.close()
            raise

    def _init_resources(self) -> None:
        """Initialize all resource handlers."""
        self.memories = MemoriesResource(self)
        self.relationships = RelationshipsResource(self)
        self.clusters = ClustersResource(self)
        self.spaces = SpacesResource(self)
        self.personas = PersonasResource(self)
        self.sessions = SessionsResource(self)
        self.resources = ResourcesResource(self)
        self.graph = GraphResource(self)
        self.search = SearchResource(self)
        self.webhooks = WebhooksResource(self)
        self.agent = AgentResource(self)
        self.feedback = FeedbackResource(self)
        self.highlights = HighlightsResource(self)
        self.facts = FactsResource(self)
        self.entities = EntitiesResource(self)
        self.enrichments = EnrichmentsResource(self)
        self.tasks = TasksResource(self)
        self.goals = GoalsResource(self)
        self.habits = HabitsResource(self)
        self.bots = BotsResource(self)
        self.space_config = SpaceConfigResource(self)
        self.workflows = WorkflowsResource(self)
        self.invites = InvitesResource(self)
        self.notes = NotesResource(self)
        self.skills = SkillsResource(self)
        self.templates = TemplatesResource(self)
        self.crews = CrewsResource(self)
        self.hubs = HubsResource(self)
        self.hub_roles = HubRolesResource(self)
        self.files = FilesResource(self)
        self.presets = PresetsResource(self)
        self.calendar = CalendarResource(self)
        self.knowledge = KnowledgeResource(self)

    def set_persona(self, persona_id: str) -> None:
        """Set the active persona for all subsequent requests."""
        validate_id(persona_id, "persona")
        self._persona_id = persona_id

    def clear_persona(self) -> None:
        """Clear the active persona."""
        self._persona_id = None

    def add_request_interceptor(self, interceptor: RequestInterceptor) -> Callable[[], None]:
        """Add a request interceptor. Returns a function to remove it."""
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

    def close(self) -> None:
        """Close the HTTP client and clear credentials."""
        self._client.close()
        self._auth.clear()
        logger.debug("Client closed and credentials cleared")

    def __enter__(self) -> "Trix":
        """Context manager entry."""
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        """Context manager exit."""
        self.close()
