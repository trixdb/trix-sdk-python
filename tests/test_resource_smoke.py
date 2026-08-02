"""Per-resource smoke tests against a real client + ``httpx.MockTransport``.

Issue #12. Each row drives one method of a resource through a *real*
``Trix`` / ``AsyncTrix`` (no mocked client) wired to an ``httpx.MockTransport``
and asserts the HTTP verb and the exact ``/v1`` request path. This catches two
bug classes the old bare-``Mock()`` resource tests structurally could not:

* **missing-method** — a method that calls a client attribute the real client
  does not expose raises ``AttributeError`` here instead of silently passing.
* **endpoint-drift** — a wrong path or a ``/v1/v1`` double-prefix is caught by
  the URL assertion.

We assert the *request* (verb + path), not the parsed response: a minimal body
often does not satisfy the response model, so a post-capture ``ValidationError``
/ ``KeyError`` is expected and ignored — the request was already recorded.
``GitHubResource`` has its own dedicated harness in
``test_github_client_verbs.py`` and is intentionally not duplicated here.
"""

import pytest
from pydantic import ValidationError

from tests.support import capturing_async_client, capturing_sync_client

# A permissive body: empty collections + common pagination keys so most list
# endpoints validate; single-object endpoints raise ValidationError (ignored).
BODY = {
    "data": [],
    "items": [],
    "results": [],
    "memories": [],
    "notes": [],
    "tasks": [],
    "goals": [],
    "habits": [],
    "skills": [],
    "templates": [],
    "crews": [],
    "presets": [],
    "clusters": [],
    "webhooks": [],
    "resources": [],
    "spaces": [],
    "agents": [],
    "sessions": [],
    "workflows": [],
    "invites": [],
    "events": [],
    "highlights": [],
    "facts": [],
    "entities": [],
    "roles": [],
    "connections": [],
    "members": [],
    "types": [],
    "suggestions": [],
    "total": 0,
    "count": 0,
    "limit": 0,
    "offset": 0,
    "has_more": False,
    "pagination": {"total": 0, "limit": 0, "offset": 0, "has_more": False},
}

# (accessor, method, args, kwargs, verb, path[without /v1])
CASES = [
    ("memories", "list", (), {}, "GET", "/memories"),
    ("relationships", "get_types", (), {}, "GET", "/relationships/types"),
    ("clusters", "list", (), {}, "GET", "/clusters"),
    ("spaces", "list", (), {}, "GET", "/spaces"),
    ("personas", "list", (), {}, "GET", "/agents"),
    ("sessions", "list", (), {}, "GET", "/cli-sessions"),
    ("resources", "list", (), {}, "GET", "/resources"),
    ("graph", "get_stats", (), {}, "GET", "/graph/stats"),
    ("search", "get_config", (), {}, "GET", "/search/config"),
    ("webhooks", "list", (), {}, "GET", "/webhooks"),
    ("agent", "list_sessions", (), {}, "GET", "/agent/sessions"),
    ("feedback", "batch", (), {"useful_ids": ["mem_1"]}, "POST", "/feedback/batch"),
    ("highlights", "list_global", (), {}, "GET", "/highlights"),
    ("facts", "list", (), {}, "GET", "/knowledge/facts"),
    ("entities", "list", (), {}, "GET", "/knowledge/entities"),
    ("enrichments", "list", ("mem_1",), {}, "GET", "/memories/mem_1/enrichments"),
    ("tasks", "list", (), {}, "GET", "/tasks"),
    ("goals", "list", (), {}, "GET", "/goals"),
    ("habits", "list", (), {}, "GET", "/habits"),
    ("bots", "list", (), {}, "GET", "/agents"),
    ("space_config", "get", ("space_1",), {}, "GET", "/spaces/space_1/config"),
    ("workflows", "list", (), {}, "GET", "/workflows"),
    ("invites", "list", (), {}, "GET", "/accounts/invites"),
    ("notes", "list", (), {}, "GET", "/notes"),
    ("skills", "list", (), {}, "GET", "/skills"),
    ("templates", "list", (), {}, "GET", "/templates"),
    ("crews", "list", (), {}, "GET", "/crews"),
    ("hubs", "list_members", ("hub_1",), {}, "GET", "/hubs/hub_1/members"),
    ("hub_roles", "list_roles", ("hub_1",), {}, "GET", "/hubs/hub_1/roles"),
    ("files", "get_quota", (), {}, "GET", "/files/quota"),
    ("presets", "list", (), {}, "GET", "/agent-presets"),
    ("calendar", "list_events", (), {}, "GET", "/calendar/events"),
    ("knowledge", "to_note", (), {"memory_ids": ["mem_1"]}, "POST", "/knowledge/to-note"),
]
IDS = [c[0] for c in CASES]


def _assert_request(captured, verb, path):
    assert len(captured) == 1, f"expected exactly one request, got {len(captured)}"
    req = captured[0]
    assert req.method == verb
    assert req.url.path == "/v1" + path
    assert "/v1/v1" not in req.url.path


@pytest.mark.parametrize("accessor,method,args,kwargs,verb,path", CASES, ids=IDS)
def test_sync_resource_smoke(accessor, method, args, kwargs, verb, path):
    client, captured = capturing_sync_client(BODY)
    try:
        bound = getattr(getattr(client, accessor), method)  # missing -> AttributeError
        try:
            bound(*args, **kwargs)
        except (ValidationError, KeyError):
            pass  # request already captured; minimal body may not parse
    finally:
        client.close()
    _assert_request(captured, verb, path)


@pytest.mark.parametrize("accessor,method,args,kwargs,verb,path", CASES, ids=IDS)
async def test_async_resource_smoke(accessor, method, args, kwargs, verb, path):
    client, captured = capturing_async_client(BODY)
    try:
        bound = getattr(getattr(client, accessor), method)  # missing -> AttributeError
        try:
            await bound(*args, **kwargs)
        except (ValidationError, KeyError):
            pass
    finally:
        await client.close()
    _assert_request(captured, verb, path)
