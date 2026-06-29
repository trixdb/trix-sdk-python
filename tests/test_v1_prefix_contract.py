"""Contract tests: every request path is versioned under ``/v1``.

Regression coverage for the CRIT finding where the SDK omitted the ``/v1``
API-version prefix. Because resource files use leading-slash paths (``/goals``)
and httpx replaces the base_url path for leading-slash request paths, any
``/v1`` a caller put in ``base_url`` was silently dropped and the request 404'd.

These tests are deterministic and do NOT hit the network: an ``httpx``
``MockTransport`` captures the final constructed request URL so we can assert
the path the client would actually send.
"""

from typing import List, Tuple

import httpx
import pytest

from trix import Trix
from trix.client_base import versioned_path

# A permissive body so list-style resource calls can parse a (empty) response.
PERMISSIVE_BODY = {
    "data": [],
    "bots": [],
    "agents": [],
    "runs": [],
    "items": [],
    "total": 0,
}


def _capturing_client(
    base_url: str = "https://api.trixdb.com",
) -> Tuple[Trix, List[httpx.Request]]:
    """Build a Trix client whose transport records the final request URL."""
    captured: List[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        captured.append(request)
        return httpx.Response(200, json=PERMISSIVE_BODY)

    client = Trix(api_key="test_key", base_url=base_url)
    client._client.close()
    client._client = httpx.Client(
        base_url=client._base_url,
        transport=httpx.MockTransport(handler),
    )
    return client, captured


# --------------------------------------------------------------------------- #
# Unit: the versioned_path helper                                             #
# --------------------------------------------------------------------------- #


def test_versioned_path_prepends_v1():
    assert versioned_path("/goals") == "/v1/goals"
    assert versioned_path("/knowledge/facts") == "/v1/knowledge/facts"


def test_versioned_path_normalizes_missing_leading_slash():
    assert versioned_path("goals") == "/v1/goals"


def test_versioned_path_is_idempotent_for_already_versioned():
    # GitHub resource paths already carry /v1 — must not become /v1/v1.
    assert versioned_path("/v1/projects/p1/github/dora-metrics") == (
        "/v1/projects/p1/github/dora-metrics"
    )
    assert versioned_path("/v1") == "/v1"


# --------------------------------------------------------------------------- #
# Integration: final constructed URL path always starts with /v1              #
# --------------------------------------------------------------------------- #


def test_representative_calls_are_versioned():
    """A representative set of resource calls must all hit a /v1 path."""
    client, captured = _capturing_client()
    calls = [
        lambda: client.goals.list(),
        lambda: client.tasks.list(),
        lambda: client.habits.list(),
        lambda: client.notes.list(),
        lambda: client.sessions.list(),
        lambda: client.webhooks.list(),
        lambda: client.facts.list(),
        lambda: client.entities.list(),
        lambda: client.ping(),
    ]
    for call in calls:
        try:
            call()
        except Exception:  # noqa: BLE001 - URL is captured before any parsing
            pass
        assert captured, "no request was issued"
        assert captured[-1].url.path.startswith("/v1/"), captured[-1].url.path
    client.close()


def test_bots_resource_maps_to_v1_agents():
    """bots.* must hit the /v1/agents namespace (was /bots -> 404)."""
    client, captured = _capturing_client()
    try:
        client.bots.list()
    except Exception:  # noqa: BLE001
        pass
    assert captured[-1].url.path == "/v1/agents"
    client.close()


def test_personas_resource_resolves_via_v1_agents():
    """personas.list must resolve via /v1/agents (was /personas -> 410)."""
    client, captured = _capturing_client()
    try:
        client.personas.list()
    except Exception:  # noqa: BLE001
        pass
    assert captured[-1].url.path == "/v1/agents"
    client.close()


def test_goals_path_is_exactly_v1_goals():
    client, captured = _capturing_client()
    try:
        client.goals.list()
    except Exception:  # noqa: BLE001
        pass
    assert captured[-1].url.path == "/v1/goals"
    client.close()


def test_v1_not_doubled_when_base_url_has_v1():
    """A base_url that already includes /v1 must not yield /v1/v1."""
    client, captured = _capturing_client(base_url="https://api.trixdb.com/v1")
    try:
        client.goals.list()
    except Exception:  # noqa: BLE001
        pass
    assert captured[-1].url.path == "/v1/goals"
    client.close()


def test_already_versioned_path_not_double_prefixed():
    """Transport must not re-prefix a path that already starts with /v1."""
    client, captured = _capturing_client()
    try:
        # MockTransport responses lack ``.elapsed``; the URL is captured first.
        client._request("GET", "/v1/projects/p1/github/dora-metrics")
    except Exception:  # noqa: BLE001
        pass
    assert captured[-1].url.path == "/v1/projects/p1/github/dora-metrics"
    client.close()


@pytest.mark.asyncio
async def test_async_calls_are_versioned():
    """The async transport must also version request paths."""
    from trix import AsyncTrix

    captured: List[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        captured.append(request)
        return httpx.Response(200, json=PERMISSIVE_BODY)

    client = AsyncTrix(api_key="test_key", base_url="https://api.trixdb.com")
    await client._client.aclose()
    client._client = httpx.AsyncClient(
        base_url=client._base_url,
        transport=httpx.MockTransport(handler),
    )
    try:
        await client.bots.list()
    except Exception:  # noqa: BLE001
        pass
    assert captured[-1].url.path == "/v1/agents"
    await client.close()
