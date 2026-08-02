"""Protocol definitions for type-safe interfaces in Trix SDK."""

from typing import (
    Any,
    AsyncIterator,
    BinaryIO,
    Dict,
    Iterator,
    Optional,
    Protocol,
    Tuple,
    Type,
    Union,
    runtime_checkable,
)

from pydantic import BaseModel


@runtime_checkable
class SyncClientProtocol(Protocol):
    """
    Protocol for synchronous Trix client.

    This protocol defines the interface that the sync client must implement.
    Resources use this protocol for type-safe client access.
    """

    _client: Any  # httpx.Client

    def _request(
        self,
        method: str,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        timeout: Optional[float] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Any:
        """Make an HTTP request and return parsed response."""
        ...

    def _request_raw(
        self,
        method: str,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        timeout: Optional[float] = None,
    ) -> bytes:
        """Make an HTTP request and return raw bytes."""
        ...

    def _request_stream(
        self,
        method: str,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        chunk_size: int = 8192,
        timeout: Optional[float] = None,
    ) -> Iterator[bytes]:
        """Make an HTTP request and stream the response."""
        ...

    def _request_multipart(
        self,
        method: str,
        path: str,
        data: Optional[Dict[str, Any]] = None,
        files: Optional[Dict[str, Union[BinaryIO, Tuple[Any, ...]]]] = None,
        params: Optional[Dict[str, Any]] = None,
        timeout: Optional[float] = None,
    ) -> Any:
        """Make a multipart/form-data HTTP request."""
        ...

    def get(
        self,
        path: str,
        *,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        response_model: Optional[Type[BaseModel]] = None,
    ) -> Any:
        """Issue a GET request, optionally validating into a pydantic model."""
        ...

    def post(
        self,
        path: str,
        *,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        response_model: Optional[Type[BaseModel]] = None,
    ) -> Any:
        """Issue a POST request, optionally validating into a pydantic model."""
        ...

    def put(
        self,
        path: str,
        *,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        response_model: Optional[Type[BaseModel]] = None,
    ) -> Any:
        """Issue a PUT request, optionally validating into a pydantic model."""
        ...

    def patch(
        self,
        path: str,
        *,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        response_model: Optional[Type[BaseModel]] = None,
    ) -> Any:
        """Issue a PATCH request, optionally validating into a pydantic model."""
        ...

    def delete(
        self,
        path: str,
        *,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        response_model: Optional[Type[BaseModel]] = None,
    ) -> Any:
        """Issue a DELETE request, optionally validating into a pydantic model."""
        ...


@runtime_checkable
class AsyncClientProtocol(Protocol):
    """
    Protocol for asynchronous Trix client.

    This protocol defines the interface that the async client must implement.
    Resources use this protocol for type-safe client access.
    """

    _client: Any  # httpx.AsyncClient

    async def _request(
        self,
        method: str,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        timeout: Optional[float] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Any:
        """Make an async HTTP request and return parsed response."""
        ...

    async def _request_raw(
        self,
        method: str,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        timeout: Optional[float] = None,
    ) -> bytes:
        """Make an async HTTP request and return raw bytes."""
        ...

    def _request_stream(
        self,
        method: str,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        chunk_size: int = 8192,
        timeout: Optional[float] = None,
    ) -> AsyncIterator[bytes]:
        """Make an async HTTP request and stream the response (async generator)."""
        ...

    async def _request_multipart(
        self,
        method: str,
        path: str,
        data: Optional[Dict[str, Any]] = None,
        files: Optional[Dict[str, Union[BinaryIO, Tuple[Any, ...]]]] = None,
        params: Optional[Dict[str, Any]] = None,
        timeout: Optional[float] = None,
    ) -> Any:
        """Make an async multipart/form-data HTTP request."""
        ...

    async def get(
        self,
        path: str,
        *,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        response_model: Optional[Type[BaseModel]] = None,
    ) -> Any:
        """Issue a GET request, optionally validating into a pydantic model."""
        ...

    async def post(
        self,
        path: str,
        *,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        response_model: Optional[Type[BaseModel]] = None,
    ) -> Any:
        """Issue a POST request, optionally validating into a pydantic model."""
        ...

    async def put(
        self,
        path: str,
        *,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        response_model: Optional[Type[BaseModel]] = None,
    ) -> Any:
        """Issue a PUT request, optionally validating into a pydantic model."""
        ...

    async def patch(
        self,
        path: str,
        *,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        response_model: Optional[Type[BaseModel]] = None,
    ) -> Any:
        """Issue a PATCH request, optionally validating into a pydantic model."""
        ...

    async def delete(
        self,
        path: str,
        *,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        response_model: Optional[Type[BaseModel]] = None,
    ) -> Any:
        """Issue a DELETE request, optionally validating into a pydantic model."""
        ...


# Type alias for any client type
ClientProtocol = Union[SyncClientProtocol, AsyncClientProtocol]
