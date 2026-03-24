"""Synchronous Trix client implementation."""

import logging
import threading
import time
import uuid
from types import TracebackType
from typing import Any, BinaryIO, Callable, Dict, Iterator, List, Optional, Tuple, Type, Union

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
    _safe_log_params,
    check_api_version,
    handle_response,
)
from .exceptions import APIError, ConnectionError, RateLimitError, ServerError, TimeoutError
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
from .utils.retry import RetryConfig
from .utils.security import get_env_credential, validate_base_url


logger = logging.getLogger(__name__)


class Trix:
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

        This is the recommended way to create a client for production use.

        Args:
            env_var: Environment variable name for API key (default: TRIX_API_KEY)
            base_url: Base URL (default: from TRIX_BASE_URL or https://api.trixdb.com)
            timeout: Request timeout in seconds
            max_retries: Maximum number of retries
            retry_config: Custom retry configuration
            pool_config: Connection pool configuration

        Returns:
            Configured Trix client

        Raises:
            ValueError: If environment variable is not set
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

        Args:
            api_key: API key for authentication
            jwt_token: JWT token for authentication (alternative to api_key)
            base_url: Base URL for Trix API (must be HTTPS)
            timeout: Request timeout in seconds
            max_retries: Maximum number of retries for failed requests
            retry_config: Custom retry configuration
            pool_config: Connection pool configuration
            allow_insecure: Allow HTTP for local development (NOT for production)
            request_interceptors: List of request interceptors
            response_interceptors: List of response interceptors
            error_interceptors: List of error interceptors

        Raises:
            ValueError: If neither api_key nor jwt_token is provided
            ValueError: If base_url is not a valid HTTPS URL
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

    def set_persona(self, persona_id: str) -> None:
        """Set the active persona for all subsequent requests."""
        self._persona_id = persona_id

    def clear_persona(self) -> None:
        """Clear the active persona."""
        self._persona_id = None

    def add_request_interceptor(self, interceptor: RequestInterceptor) -> Callable[[], None]:
        """Add a request interceptor.

        Args:
            interceptor: Function that receives RequestContext and optionally returns modified context

        Returns:
            Function to remove the interceptor
        """
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

    def _request(
        self,
        method: str,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        timeout: Optional[float] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Any:
        """Make HTTP request to Trix API with retry logic."""
        last_exception: Optional[Exception] = None
        config = self._retry_config
        request_timeout = timeout if timeout is not None else self._timeout

        merged_headers = self._get_headers()
        if headers:
            merged_headers.update(headers)
        request_context = RequestContext(
            method=method, path=path, params=params, json=json, headers=merged_headers
        )
        request_context = self._run_request_interceptors(request_context)

        for attempt in range(config.max_retries + 1):
            try:
                response = self._execute_request(request_context, request_timeout)
                return self._process_response(response, request_context)
            except (RateLimitError, ServerError) as e:
                last_exception = self._handle_retry(e, attempt, config, request_context)
                if last_exception is not None:
                    raise last_exception
            except httpx.TimeoutException as e:
                raise self._handle_httpx_error(e, request_context, "timeout")
            except httpx.NetworkError as e:
                raise self._handle_httpx_error(e, request_context, "network")
            except httpx.HTTPError as e:
                raise self._handle_httpx_error(e, request_context, "http")

        if last_exception:
            raise last_exception
        raise RuntimeError("Retry logic failed unexpectedly")

    def _execute_request(self, ctx: RequestContext, timeout: float) -> httpx.Response:
        """Execute the HTTP request."""
        logger.debug(f"Request: {ctx.method} {ctx.path} params={_safe_log_params(ctx.params)}")
        return self._client.request(
            method=ctx.method,
            url=ctx.path,
            params=ctx.params,
            json=ctx.json,
            headers=ctx.headers,
            timeout=timeout,
        )

    MAX_RESPONSE_SIZE = 50 * 1024 * 1024  # 50MB

    def _process_response(self, response: httpx.Response, ctx: RequestContext) -> Any:
        """Process and validate the HTTP response."""
        safe_headers = {
            k: v if k.lower() != "authorization" else "[REDACTED]"
            for k, v in response.headers.items()
        }
        logger.debug(f"Response: {response.status_code} headers={safe_headers}")

        content_length = response.headers.get("content-length")
        if content_length and int(content_length) > self.MAX_RESPONSE_SIZE:
            raise ValueError(
                f"Response too large: {content_length} bytes (max {self.MAX_RESPONSE_SIZE})"
            )

        check_api_version(response)
        handle_response(response)

        response_data: Any = {} if response.status_code == 204 else response.json()
        response_context = ResponseContext(
            request=ctx,
            status_code=response.status_code,
            headers=dict(response.headers),
            data=response_data,
        )
        response_context = self._run_response_interceptors(response_context)
        return response_context.data

    def _handle_retry(
        self, error: Exception, attempt: int, config: RetryConfig, ctx: RequestContext
    ) -> Optional[Exception]:
        """Handle retry logic for retryable errors. Returns exception if should raise."""
        if attempt >= config.max_retries:
            return self._run_error_interceptors(error, ctx)

        retry_after = getattr(error, "retry_after", None)
        delay = config.calculate_delay(attempt, retry_after)
        logger.warning(
            f"Attempt {attempt + 1}/{config.max_retries + 1} failed: {error}. Retrying in {delay:.2f}s..."
        )
        time.sleep(delay)
        return None

    def _handle_httpx_error(
        self, error: Exception, ctx: RequestContext, error_type: str
    ) -> Exception:
        """Convert httpx errors to Trix errors."""
        logger.debug(f"Request {error_type} error: {error}")
        if error_type == "timeout":
            exc: Exception = TimeoutError(f"Request timed out: {error}")
        elif error_type == "network":
            exc = ConnectionError(f"Network error: {error}")
        else:
            exc = APIError(f"HTTP error: {error}")
        return self._run_error_interceptors(exc, ctx)

    def _request_raw(
        self,
        method: str,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        timeout: Optional[float] = None,
    ) -> bytes:
        """Make HTTP request and return raw bytes."""
        request_timeout = timeout if timeout is not None else self._timeout
        try:
            logger.debug(f"Request (raw): {method} {path} params={_safe_log_params(params)}")
            response = self._client.request(
                method=method, url=path, params=params, timeout=request_timeout
            )
            logger.debug(f"Response (raw): {response.status_code}")
            check_api_version(response)
            handle_response(response)
            return response.content
        except httpx.TimeoutException as e:
            raise TimeoutError(f"Request timed out: {e}") from e
        except httpx.NetworkError as e:
            raise ConnectionError(f"Network error: {e}") from e
        except httpx.HTTPError as e:
            raise APIError(f"HTTP error: {e}") from e

    def _request_stream(
        self,
        method: str,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        chunk_size: int = 8192,
        timeout: Optional[float] = None,
    ) -> Iterator[bytes]:
        """Make HTTP request and stream the response."""
        request_timeout = timeout if timeout is not None else self._timeout
        try:
            logger.debug(f"Request (stream): {method} {path} params={_safe_log_params(params)}")
            with self._client.stream(
                method=method, url=path, params=params, timeout=request_timeout
            ) as response:
                logger.debug(f"Response (stream): {response.status_code}")
                check_api_version(response)
                handle_response(response)
                for chunk in response.iter_bytes(chunk_size=chunk_size):
                    yield chunk
        except httpx.TimeoutException as e:
            raise TimeoutError(f"Request timed out: {e}") from e
        except httpx.NetworkError as e:
            raise ConnectionError(f"Network error: {e}") from e
        except httpx.HTTPError as e:
            raise APIError(f"HTTP error: {e}") from e

    def _request_multipart(
        self,
        method: str,
        path: str,
        data: Optional[Dict[str, Any]] = None,
        files: Optional[Dict[str, Union[BinaryIO, Tuple[Any, ...]]]] = None,
        params: Optional[Dict[str, Any]] = None,
        timeout: Optional[float] = None,
    ) -> Any:
        """Make multipart/form-data HTTP request for file uploads."""
        request_timeout = timeout if timeout is not None else self._timeout
        try:
            logger.debug(f"Request (multipart): {method} {path}")
            headers = {k: v for k, v in self._get_headers().items() if k.lower() != "content-type"}
            response = self._client.request(
                method=method,
                url=path,
                data=data,
                files=files,
                params=params,
                headers=headers,
                timeout=request_timeout,
            )
            logger.debug(f"Response (multipart): {response.status_code}")
            check_api_version(response)
            handle_response(response)
            return {} if response.status_code == 204 else response.json()
        except httpx.TimeoutException as e:
            raise TimeoutError(f"Request timed out: {e}") from e
        except httpx.NetworkError as e:
            raise ConnectionError(f"Network error: {e}") from e
        except httpx.HTTPError as e:
            raise APIError(f"HTTP error: {e}") from e

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
