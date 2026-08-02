"""Regression tests for the client verb helpers (GitHub issue #5).

Before the fix, ~144 ``GitHubResource`` / ``AsyncGitHubResource`` methods called
``self._client.get/post/put/patch/delete`` — methods that did not exist on the
``Trix`` / ``AsyncTrix`` client — raising ``AttributeError`` at runtime. The
existing GitHub tests never caught this because they mock ``_client`` as a bare
``Mock()`` (where ``.get`` auto-creates an attribute).

These tests wire a *real* client to an ``httpx.MockTransport`` so the whole
path is exercised: verb helper -> ``_request`` -> ``versioned_path`` ->
transport -> ``response_model.model_validate``. They also pin the request
method and the exact ``/v1`` path, guarding against a ``/v1/v1`` double-prefix.
"""

import datetime
import json as jsonlib

import httpx

from trix import AsyncTrix, Trix
from trix.resources.github_types import GenerateTestsResult, IssueCycleTimeResult

PROJECT_ID = "6a9bfe12-0001-4001-b000-000000000001"

CYCLE_TIME_BODY = {
    "by_label": [
        {
            "label": "bug",
            "issue_count": 3,
            "avg_days": 2.5,
            "median_days": 2.0,
            "min_days": 1.0,
            "max_days": 5.0,
        }
    ],
    "lookback_days": 90,
}


def _make_handler(captured, body):
    """Build a MockTransport handler that records requests and returns ``body``."""

    def handler(request: httpx.Request) -> httpx.Response:
        captured.append(request)
        response = httpx.Response(200, json=body)
        # MockTransport responses don't get an ``.elapsed`` set by httpx; the
        # transport's debug logging reads it, so provide one for the test.
        response._elapsed = datetime.timedelta(seconds=0)
        return response

    return handler


def _sync_client(handler) -> Trix:
    client = Trix(api_key="test_key", base_url="https://api.test.com")
    client._client.close()
    client._client = httpx.Client(base_url=client._base_url, transport=httpx.MockTransport(handler))
    return client


def _async_client(handler) -> AsyncTrix:
    client = AsyncTrix(api_key="test_key", base_url="https://api.test.com")
    client._client = httpx.AsyncClient(
        base_url=client._base_url, transport=httpx.MockTransport(handler)
    )
    return client


class TestSyncGitHubVerbHelpers:
    def test_get_with_response_model(self):
        """GET helper: correct verb, single /v1 path, params, and typed model."""
        captured: list = []
        client = _sync_client(_make_handler(captured, CYCLE_TIME_BODY))
        try:
            result = client.github.get_issue_cycle_time(PROJECT_ID, days=90)
        finally:
            client.close()

        assert len(captured) == 1
        req = captured[0]
        assert req.method == "GET"
        assert req.url.path == f"/v1/projects/{PROJECT_ID}/github/issue-cycle-time"
        assert "/v1/v1" not in req.url.path
        assert req.url.params.get("days") == "90"
        assert isinstance(result, IssueCycleTimeResult)
        assert result.lookback_days == 90
        assert result.by_label[0].label == "bug"

    def test_post_without_response_model(self):
        """POST helper (dead_code_ratio): raw dict returned, JSON body forwarded."""
        captured: list = []
        raw_body = {"files": [{"path": "a.py", "dead_ratio": 0.9}], "total": 1}
        client = _sync_client(_make_handler(captured, raw_body))
        try:
            result = client.github.dead_code_ratio(PROJECT_ID, tier="zombie")
        finally:
            client.close()

        req = captured[0]
        assert req.method == "POST"
        assert req.url.path == f"/v1/projects/{PROJECT_ID}/github/query"
        sent = jsonlib.loads(req.content)
        assert sent["from"] == "dead_code_ratio"
        assert sent["where"]["tier"] == "zombie"
        # No response_model -> the raw dict is returned unchanged.
        assert result == raw_body

    def test_post_with_response_model(self):
        """POST helper (generate_tests): typed model returned from a POST body."""
        captured: list = []
        body = {"test_file_path": "tests/test_a.py", "language": "python", "function_count": 2}
        client = _sync_client(_make_handler(captured, body))
        try:
            result = client.github.generate_tests(
                PROJECT_ID, repo_full_name="acme/api", file_path="src/a.py"
            )
        finally:
            client.close()

        req = captured[0]
        assert req.method == "POST"
        assert req.url.path == f"/v1/projects/{PROJECT_ID}/github/generate-tests"
        sent = jsonlib.loads(req.content)
        assert sent == {"repo_full_name": "acme/api", "file_path": "src/a.py"}
        assert isinstance(result, GenerateTestsResult)
        assert result.test_file_path == "tests/test_a.py"
        assert result.function_count == 2


class TestAsyncGitHubVerbHelpers:
    async def test_async_get_with_response_model(self):
        captured: list = []
        client = _async_client(_make_handler(captured, CYCLE_TIME_BODY))
        try:
            result = await client.github.get_issue_cycle_time(PROJECT_ID, days=90)
        finally:
            await client.close()

        req = captured[0]
        assert req.method == "GET"
        assert req.url.path == f"/v1/projects/{PROJECT_ID}/github/issue-cycle-time"
        assert "/v1/v1" not in req.url.path
        assert req.url.params.get("days") == "90"
        assert isinstance(result, IssueCycleTimeResult)
        assert result.by_label[0].label == "bug"

    async def test_async_post_without_response_model(self):
        captured: list = []
        raw_body = {"files": [], "total": 0}
        client = _async_client(_make_handler(captured, raw_body))
        try:
            result = await client.github.dead_code_ratio(PROJECT_ID)
        finally:
            await client.close()

        req = captured[0]
        assert req.method == "POST"
        assert req.url.path == f"/v1/projects/{PROJECT_ID}/github/query"
        assert result == raw_body
