"""Tests for TemplatesResource."""

from tests.support import spec_client
from trix.resources.templates import TemplatesResource

TEMPLATE_RESPONSE = {
    "id": "tmpl_123",
    "account_id": "acct_456",
    "name": "Research Assistant",
    "slug": "research-assistant",
    "description": "A helpful research bot",
    "category": "productivity",
    "tags": ["research", "ai"],
    "system_prompt": "You are a research assistant.",
    "tools": [],
    "settings": {},
    "metadata": {},
    "status": "active",
    "is_public": False,
    "install_count": 0,
    "rating": None,
    "review_count": 0,
    "created_at": "2025-01-01T00:00:00Z",
    "updated_at": "2025-01-01T00:00:00Z",
}

TEMPLATE_LIST_RESPONSE = {
    "templates": [TEMPLATE_RESPONSE],
    "total": 1,
    "limit": 20,
    "offset": 0,
}


class TestTemplatesList:
    """Tests for templates.list()."""

    def test_list_all(self):
        """Test listing all templates."""
        mock_client = spec_client()
        mock_client._request.return_value = TEMPLATE_LIST_RESPONSE

        resource = TemplatesResource(mock_client)
        result = resource.list()

        call_args = mock_client._request.call_args
        assert call_args[0] == ("GET", "/templates")
        params = call_args[1]["params"]
        assert params["limit"] == 20
        assert params["offset"] == 0
        assert len(result.templates) == 1
        assert result.templates[0].id == "tmpl_123"
        assert result.total == 1

    def test_list_with_filters(self):
        """Test listing templates with category and status filters."""
        mock_client = spec_client()
        mock_client._request.return_value = TEMPLATE_LIST_RESPONSE

        resource = TemplatesResource(mock_client)
        resource.list(category="productivity", status="active", limit=10)

        call_args = mock_client._request.call_args
        params = call_args[1]["params"]
        assert params["category"] == "productivity"
        assert params["status"] == "active"
        assert params["limit"] == 10


class TestTemplatesGet:
    """Tests for templates.get()."""

    def test_get_by_id(self):
        """Test getting a template by ID."""
        mock_client = spec_client()
        mock_client._request.return_value = TEMPLATE_RESPONSE

        resource = TemplatesResource(mock_client)
        result = resource.get("tmpl_123")

        call_args = mock_client._request.call_args
        assert call_args[0] == ("GET", "/templates/tmpl_123")
        assert result.id == "tmpl_123"
        assert result.name == "Research Assistant"
        assert result.category == "productivity"


class TestTemplatesCreate:
    """Tests for templates.create()."""

    def test_create_basic(self):
        """Test creating a template with just a name."""
        mock_client = spec_client()
        mock_client._request.return_value = TEMPLATE_RESPONSE

        resource = TemplatesResource(mock_client)
        result = resource.create(name="Research Assistant")

        call_args = mock_client._request.call_args
        assert call_args[0] == ("POST", "/templates")
        body = call_args[1]["json"]
        assert body["name"] == "Research Assistant"
        assert result.id == "tmpl_123"

    def test_create_with_options(self):
        """Test creating a template with all options."""
        mock_client = spec_client()
        mock_client._request.return_value = TEMPLATE_RESPONSE

        resource = TemplatesResource(mock_client)
        resource.create(
            name="Research Assistant",
            description="A helpful research bot",
            category="productivity",
            tags=["research", "ai"],
            system_prompt="You are a research assistant.",
        )

        call_args = mock_client._request.call_args
        body = call_args[1]["json"]
        assert body["name"] == "Research Assistant"
        assert body["description"] == "A helpful research bot"
        assert body["category"] == "productivity"
        assert body["tags"] == ["research", "ai"]
        assert body["system_prompt"] == "You are a research assistant."


class TestTemplatesDelete:
    """Tests for templates.delete()."""

    def test_delete_by_id(self):
        """Test deleting a template."""
        mock_client = spec_client()
        mock_client._request.return_value = None

        resource = TemplatesResource(mock_client)
        resource.delete("tmpl_123")

        call_args = mock_client._request.call_args
        assert call_args[0] == ("DELETE", "/templates/tmpl_123")
