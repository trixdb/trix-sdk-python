"""Tests for personas resource."""

import pytest
from unittest.mock import patch

from trix import Trix, AsyncTrix
from trix.types import Persona, PersonaList, PersonaSpace


@pytest.fixture
def mock_persona_data():
    """Mock persona response data."""
    return {
        "id": "persona_123",
        "name": "Research",
        "slug": "research",
        "purpose": "Academic research",
        "system_prompt": "You are a research assistant.",
        "goals": [],
        "settings": {},
        "metadata": {},
        "is_default": False,
        "can_create_spaces": False,
        "created_at": "2026-01-01T00:00:00Z",
        "updated_at": "2026-01-01T00:00:00Z",
    }


@pytest.fixture
def mock_persona_list_data(mock_persona_data):
    """Mock persona list response data.

    Personas resolve from the agents endpoint, which returns the collection
    under the ``agents`` key.
    """
    return {"agents": [mock_persona_data]}


@pytest.fixture
def mock_persona_space_data():
    """Mock persona space membership data."""
    return {
        "space_id": "space_456",
        "role": "member",
        "can_create_memories": True,
        "can_delete_memories": False,
    }


class TestPersonaCreate:
    """Tests for creating personas."""

    def test_create_with_minimal_params(self, mock_persona_data):
        """Test creating a persona with only the required name parameter."""
        with patch.object(Trix, "_request") as mock_request:
            mock_request.return_value = mock_persona_data
            client = Trix(api_key="test_key")

            persona = client.personas.create(name="Research")

            assert isinstance(persona, Persona)
            assert persona.name == "Research"
            assert persona.id == "persona_123"
            call_args = mock_request.call_args
            json_data = call_args[1]["json"]
            assert json_data["name"] == "Research"
            assert "purpose" not in json_data
            assert "system_prompt" not in json_data
            client.close()

    def test_create_with_all_params(self, mock_persona_data):
        """Test creating a persona with all optional parameters."""
        full_data = mock_persona_data.copy()
        full_data["avatar_url"] = "https://example.com/avatar.png"
        full_data["is_default"] = True
        full_data["can_create_spaces"] = True
        full_data["settings"] = {"theme": "dark"}

        with patch.object(Trix, "_request") as mock_request:
            mock_request.return_value = full_data
            client = Trix(api_key="test_key")

            persona = client.personas.create(
                name="Research",
                slug="research",
                avatar_url="https://example.com/avatar.png",
                purpose="Academic research",
                system_prompt="You are a research assistant.",
                goals=[],
                settings={"theme": "dark"},
                is_default=True,
                can_create_spaces=True,
            )

            assert isinstance(persona, Persona)
            assert persona.name == "Research"
            assert persona.is_default is True
            assert persona.can_create_spaces is True
            client.close()

    def test_create_sends_correct_request(self, mock_persona_data):
        """Test that create sends POST /personas with correct JSON body."""
        with patch.object(Trix, "_request") as mock_request:
            mock_request.return_value = mock_persona_data
            client = Trix(api_key="test_key")

            client.personas.create(name="Research", purpose="Academic research")

            call_args = mock_request.call_args
            assert call_args[0][0] == "POST"
            assert call_args[0][1] == "/personas"
            json_data = call_args[1]["json"]
            assert json_data["name"] == "Research"
            assert json_data["purpose"] == "Academic research"
            client.close()

    @pytest.mark.asyncio
    async def test_create_async(self, mock_persona_data):
        """Test creating a persona with the async client."""
        with patch.object(AsyncTrix, "_request") as mock_request:
            mock_request.return_value = mock_persona_data
            client = AsyncTrix(api_key="test_key")

            persona = await client.personas.create(name="Research", purpose="Academic research")

            assert isinstance(persona, Persona)
            assert persona.name == "Research"
            assert persona.id == "persona_123"
            await client.close()


class TestPersonaList:
    """Tests for listing personas."""

    def test_list_personas(self, mock_persona_list_data):
        """Test listing all personas."""
        with patch.object(Trix, "_request") as mock_request:
            mock_request.return_value = mock_persona_list_data
            client = Trix(api_key="test_key")

            result = client.personas.list()

            assert isinstance(result, PersonaList)
            assert len(result.data) == 1
            assert result.data[0].name == "Research"
            assert result.data[0].slug == "research"
            client.close()

    def test_list_sends_correct_request(self, mock_persona_list_data):
        """Test that list resolves personas via GET /agents (personas merged in)."""
        with patch.object(Trix, "_request") as mock_request:
            mock_request.return_value = mock_persona_list_data
            client = Trix(api_key="test_key")

            client.personas.list()

            call_args = mock_request.call_args
            assert call_args[0][0] == "GET"
            assert call_args[0][1] == "/agents"
            client.close()

    @pytest.mark.asyncio
    async def test_list_async(self, mock_persona_list_data):
        """Test listing personas with the async client."""
        with patch.object(AsyncTrix, "_request") as mock_request:
            mock_request.return_value = mock_persona_list_data
            client = AsyncTrix(api_key="test_key")

            result = await client.personas.list()

            assert isinstance(result, PersonaList)
            assert len(result.data) == 1
            assert result.data[0].name == "Research"
            await client.close()


class TestPersonaGet:
    """Tests for getting a persona by ID."""

    def test_get_persona(self, mock_persona_data):
        """Test getting a persona by ID."""
        with patch.object(Trix, "_request") as mock_request:
            mock_request.return_value = mock_persona_data
            client = Trix(api_key="test_key")

            persona = client.personas.get("persona_123")

            assert isinstance(persona, Persona)
            assert persona.id == "persona_123"
            assert persona.name == "Research"
            assert persona.purpose == "Academic research"
            client.close()

    def test_get_sends_correct_request(self, mock_persona_data):
        """Test that get sends GET /personas/{id}."""
        with patch.object(Trix, "_request") as mock_request:
            mock_request.return_value = mock_persona_data
            client = Trix(api_key="test_key")

            client.personas.get("persona_123")

            call_args = mock_request.call_args
            assert call_args[0][0] == "GET"
            assert call_args[0][1] == "/personas/persona_123"
            client.close()

    def test_get_validates_id(self):
        """Test that get raises ValueError for invalid IDs."""
        with patch.object(Trix, "_request"):
            client = Trix(api_key="test_key")

            with pytest.raises(ValueError, match="persona ID cannot be empty"):
                client.personas.get("")

            client.close()

    @pytest.mark.asyncio
    async def test_get_async(self, mock_persona_data):
        """Test getting a persona with the async client."""
        with patch.object(AsyncTrix, "_request") as mock_request:
            mock_request.return_value = mock_persona_data
            client = AsyncTrix(api_key="test_key")

            persona = await client.personas.get("persona_123")

            assert isinstance(persona, Persona)
            assert persona.id == "persona_123"
            await client.close()


class TestPersonaGetBySlug:
    """Tests for getting a persona by slug."""

    def test_get_by_slug(self, mock_persona_data):
        """Test getting a persona by slug."""
        with patch.object(Trix, "_request") as mock_request:
            mock_request.return_value = mock_persona_data
            client = Trix(api_key="test_key")

            persona = client.personas.get_by_slug("research")

            assert isinstance(persona, Persona)
            assert persona.slug == "research"
            call_args = mock_request.call_args
            assert call_args[0][0] == "GET"
            assert call_args[0][1] == "/personas/slug/research"
            client.close()

    def test_get_by_slug_validates_empty(self):
        """Test that get_by_slug raises ValueError for empty slug."""
        with patch.object(Trix, "_request"):
            client = Trix(api_key="test_key")

            with pytest.raises(ValueError, match="persona slug cannot be empty"):
                client.personas.get_by_slug("")

            client.close()

    @pytest.mark.asyncio
    async def test_get_by_slug_async(self, mock_persona_data):
        """Test getting a persona by slug with the async client."""
        with patch.object(AsyncTrix, "_request") as mock_request:
            mock_request.return_value = mock_persona_data
            client = AsyncTrix(api_key="test_key")

            persona = await client.personas.get_by_slug("research")

            assert isinstance(persona, Persona)
            assert persona.slug == "research"
            await client.close()


class TestPersonaUpdate:
    """Tests for updating personas."""

    def test_update_name(self, mock_persona_data):
        """Test updating a persona's name."""
        updated = mock_persona_data.copy()
        updated["name"] = "Updated Research"

        with patch.object(Trix, "_request") as mock_request:
            mock_request.return_value = updated
            client = Trix(api_key="test_key")

            persona = client.personas.update("persona_123", name="Updated Research")

            assert isinstance(persona, Persona)
            assert persona.name == "Updated Research"
            call_args = mock_request.call_args
            json_data = call_args[1]["json"]
            assert json_data["name"] == "Updated Research"
            client.close()

    def test_update_multiple_fields(self, mock_persona_data):
        """Test updating multiple persona fields at once."""
        updated = mock_persona_data.copy()
        updated["name"] = "New Name"
        updated["purpose"] = "New purpose"
        updated["is_default"] = True

        with patch.object(Trix, "_request") as mock_request:
            mock_request.return_value = updated
            client = Trix(api_key="test_key")

            persona = client.personas.update(
                "persona_123",
                name="New Name",
                purpose="New purpose",
                is_default=True,
            )

            assert isinstance(persona, Persona)
            assert persona.name == "New Name"
            assert persona.purpose == "New purpose"
            assert persona.is_default is True
            call_args = mock_request.call_args
            json_data = call_args[1]["json"]
            assert json_data["name"] == "New Name"
            assert json_data["purpose"] == "New purpose"
            assert json_data["is_default"] is True
            client.close()

    def test_update_sends_correct_request(self, mock_persona_data):
        """Test that update sends PATCH /personas/{id}."""
        with patch.object(Trix, "_request") as mock_request:
            mock_request.return_value = mock_persona_data
            client = Trix(api_key="test_key")

            client.personas.update("persona_123", name="Research")

            call_args = mock_request.call_args
            assert call_args[0][0] == "PATCH"
            assert call_args[0][1] == "/personas/persona_123"
            client.close()

    @pytest.mark.asyncio
    async def test_update_async(self, mock_persona_data):
        """Test updating a persona with the async client."""
        updated = mock_persona_data.copy()
        updated["name"] = "Async Updated"

        with patch.object(AsyncTrix, "_request") as mock_request:
            mock_request.return_value = updated
            client = AsyncTrix(api_key="test_key")

            persona = await client.personas.update("persona_123", name="Async Updated")

            assert isinstance(persona, Persona)
            assert persona.name == "Async Updated"
            await client.close()


class TestPersonaDelete:
    """Tests for deleting personas."""

    def test_delete_persona(self):
        """Test deleting a persona returns None."""
        with patch.object(Trix, "_request") as mock_request:
            mock_request.return_value = None
            client = Trix(api_key="test_key")

            result = client.personas.delete("persona_123")

            assert result is None
            client.close()

    def test_delete_sends_correct_request(self):
        """Test that delete sends DELETE /personas/{id}."""
        with patch.object(Trix, "_request") as mock_request:
            mock_request.return_value = None
            client = Trix(api_key="test_key")

            client.personas.delete("persona_123")

            call_args = mock_request.call_args
            assert call_args[0][0] == "DELETE"
            assert call_args[0][1] == "/personas/persona_123"
            client.close()

    @pytest.mark.asyncio
    async def test_delete_async(self):
        """Test deleting a persona with the async client."""
        with patch.object(AsyncTrix, "_request") as mock_request:
            mock_request.return_value = None
            client = AsyncTrix(api_key="test_key")

            result = await client.personas.delete("persona_123")

            assert result is None
            await client.close()


class TestPersonaAddSpace:
    """Tests for adding spaces to personas."""

    def test_add_space_default_role(self, mock_persona_space_data):
        """Test adding a space with default role (member)."""
        with patch.object(Trix, "_request") as mock_request:
            mock_request.return_value = mock_persona_space_data
            client = Trix(api_key="test_key")

            ps = client.personas.add_space("persona_123", "space_456")

            assert isinstance(ps, PersonaSpace)
            assert ps.space_id == "space_456"
            assert ps.role == "member"
            assert ps.can_create_memories is True
            assert ps.can_delete_memories is False
            client.close()

    def test_add_space_admin_role(self, mock_persona_space_data):
        """Test adding a space with admin role and custom permissions."""
        admin_data = mock_persona_space_data.copy()
        admin_data["role"] = "admin"
        admin_data["can_delete_memories"] = True

        with patch.object(Trix, "_request") as mock_request:
            mock_request.return_value = admin_data
            client = Trix(api_key="test_key")

            ps = client.personas.add_space(
                "persona_123",
                "space_456",
                role="admin",
                can_create_memories=True,
                can_delete_memories=True,
            )

            assert isinstance(ps, PersonaSpace)
            assert ps.role == "admin"
            assert ps.can_delete_memories is True
            client.close()

    def test_add_space_sends_correct_request(self, mock_persona_space_data):
        """Test that add_space sends POST /personas/{id}/spaces."""
        with patch.object(Trix, "_request") as mock_request:
            mock_request.return_value = mock_persona_space_data
            client = Trix(api_key="test_key")

            client.personas.add_space("persona_123", "space_456")

            call_args = mock_request.call_args
            assert call_args[0][0] == "POST"
            assert call_args[0][1] == "/personas/persona_123/spaces"
            json_data = call_args[1]["json"]
            assert json_data["space_id"] == "space_456"
            assert json_data["role"] == "member"
            client.close()

    @pytest.mark.asyncio
    async def test_add_space_async(self, mock_persona_space_data):
        """Test adding a space with the async client."""
        with patch.object(AsyncTrix, "_request") as mock_request:
            mock_request.return_value = mock_persona_space_data
            client = AsyncTrix(api_key="test_key")

            ps = await client.personas.add_space("persona_123", "space_456")

            assert isinstance(ps, PersonaSpace)
            assert ps.space_id == "space_456"
            assert ps.role == "member"
            await client.close()


class TestPersonaRemoveSpace:
    """Tests for removing spaces from personas."""

    def test_remove_space(self):
        """Test removing a space from a persona returns None."""
        with patch.object(Trix, "_request") as mock_request:
            mock_request.return_value = None
            client = Trix(api_key="test_key")

            result = client.personas.remove_space("persona_123", "space_456")

            assert result is None
            client.close()

    def test_remove_space_sends_correct_request(self):
        """Test that remove_space sends DELETE /personas/{id}/spaces/{sid}."""
        with patch.object(Trix, "_request") as mock_request:
            mock_request.return_value = None
            client = Trix(api_key="test_key")

            client.personas.remove_space("persona_123", "space_456")

            call_args = mock_request.call_args
            assert call_args[0][0] == "DELETE"
            assert call_args[0][1] == "/personas/persona_123/spaces/space_456"
            client.close()

    @pytest.mark.asyncio
    async def test_remove_space_async(self):
        """Test removing a space with the async client."""
        with patch.object(AsyncTrix, "_request") as mock_request:
            mock_request.return_value = None
            client = AsyncTrix(api_key="test_key")

            result = await client.personas.remove_space("persona_123", "space_456")

            assert result is None
            await client.close()
