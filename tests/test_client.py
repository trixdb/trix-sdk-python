"""Tests for TrixDB client."""

import pytest
from trixdb import TrixDB, AsyncTrixDB
from trixdb.exceptions import TrixDBError


def test_client_initialization_with_api_key():
    """Test client initialization with API key."""
    client = TrixDB(api_key="test_key")
    assert client._auth.api_key == "test_key"
    client.close()


def test_client_initialization_with_jwt():
    """Test client initialization with JWT token."""
    client = TrixDB(jwt_token="test_token")
    assert client._auth.jwt_token == "test_token"
    client.close()


def test_client_initialization_without_auth():
    """Test client initialization without authentication raises error."""
    with pytest.raises(ValueError):
        TrixDB()


def test_client_context_manager():
    """Test client as context manager."""
    with TrixDB(api_key="test_key") as client:
        assert client._auth.api_key == "test_key"


def test_client_custom_base_url():
    """Test client with custom base URL."""
    client = TrixDB(api_key="test_key", base_url="https://custom.api.com")
    assert client._base_url == "https://custom.api.com"
    client.close()


def test_client_custom_timeout():
    """Test client with custom timeout."""
    client = TrixDB(api_key="test_key", timeout=60.0)
    assert client._timeout == 60.0
    client.close()


@pytest.mark.asyncio
async def test_async_client_initialization():
    """Test async client initialization."""
    async with AsyncTrixDB(api_key="test_key") as client:
        assert client._auth.api_key == "test_key"


@pytest.mark.asyncio
async def test_async_client_context_manager():
    """Test async client as context manager."""
    client = AsyncTrixDB(api_key="test_key")
    async with client:
        assert client._auth.api_key == "test_key"
