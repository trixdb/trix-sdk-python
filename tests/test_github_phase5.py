"""Tests for GitHubResource Phase 5 — Code Quality Scanner + Repo Stats (ADR-152)."""

from unittest.mock import Mock

import pytest

from tests.support import spec_client
from trix.resources.github import GitHubResource
from trix.resources.github_async import AsyncGitHubResource

PROJECT_ID = "6a9bfe12-0001-4001-b000-000000000001"
SUGGESTION_ID = "7b8cfe34-0002-4002-b001-000000000002"

SUGGESTION = {
    "id": SUGGESTION_ID,
    "category": "security",
    "priority": "critical",
    "title": "SQL injection risk in UserRepository",
    "description": "Use parameterised queries.",
    "file_path": "src/db/user_repo.py",
    "evidence": {},
    "status": "open",
    "generated_by": "rule",
    "generated_at": "2026-04-20T12:00:00Z",
}

SUMMARY_ROW = {"category": "security", "priority": "critical", "cnt": "3"}

HISTORY_ITEM = {
    "id": "snap-001",
    "snapshotted_at": "2026-04-18T00:00:00Z",
    "suggestion_count": 12,
    "critical_count": 3,
    "warning_count": 5,
    "total_files": 200,
    "hotspot_count": 8,
}

REPO_STATS = {
    "stats": {
        "repo": {
            "full_name": "acme/api",
            "description": "Core API",
            "stars": 42,
            "forks": 7,
            "open_issues": 3,
            "primary_language": "Python",
            "license": "MIT",
            "is_private": False,
            "size_kb": 12000,
        },
        "languages": [{"name": "Python", "bytes": 400000, "pct": 88.5}],
        "contributors": [
            {
                "login": "alice",
                "avatar_url": "https://example.com/a.png",
                "profile_url": "https://github.com/alice",
                "contributions": 120,
            }
        ],
        "readme": "# Acme API\nFast and reliable.",
        "open_pr_count": 2,
        "local_metrics": {
            "analyzed_files": 180,
            "total_loc": 22000,
            "hotspot_count": 8,
            "critical_files": 3,
            "warning_files": 5,
        },
    }
}


class TestGenerateCodeImprovements:
    def test_posts_to_generate_endpoint(self):
        client = spec_client()
        client._request.return_value = {"generated": 7, "repo": "acme/api"}
        result = GitHubResource(client).generate_code_improvements(PROJECT_ID)
        args, kwargs = client._request.call_args
        assert args == ("POST", f"/projects/{PROJECT_ID}/github/improvements/generate")
        assert kwargs.get("json") == {}
        assert result.generated == 7
        assert result.repo == "acme/api"


class TestGetCodeImprovements:
    def test_default_status_open(self):
        client = spec_client()
        client._request.return_value = {"suggestions": [SUGGESTION]}
        result = GitHubResource(client).get_code_improvements(PROJECT_ID)
        _, kwargs = client._request.call_args
        assert kwargs["params"]["status"] == "open"
        assert len(result.suggestions) == 1

    def test_filters_by_category_and_priority(self):
        client = spec_client()
        client._request.return_value = {"suggestions": []}
        GitHubResource(client).get_code_improvements(
            PROJECT_ID, category="security", priority="critical", status="open"
        )
        _, kwargs = client._request.call_args
        assert kwargs["params"]["category"] == "security"
        assert kwargs["params"]["priority"] == "critical"

    def test_maps_suggestion_fields(self):
        client = spec_client()
        client._request.return_value = {"suggestions": [SUGGESTION]}
        result = GitHubResource(client).get_code_improvements(PROJECT_ID)
        s = result.suggestions[0]
        assert s.id == SUGGESTION_ID
        assert s.category == "security"
        assert s.priority == "critical"
        assert s.file_path == "src/db/user_repo.py"


class TestUpdateCodeImprovementStatus:
    def test_patches_correct_endpoint(self):
        client = spec_client()
        client._request.return_value = {"suggestion": {**SUGGESTION, "status": "resolved"}}
        result = GitHubResource(client).update_code_improvement_status(
            PROJECT_ID, SUGGESTION_ID, "resolved"
        )
        args, kwargs = client._request.call_args
        assert args == ("PATCH", f"/projects/{PROJECT_ID}/github/improvements/{SUGGESTION_ID}")
        assert kwargs.get("json") == {"status": "resolved"}
        assert result.status == "resolved"

    def test_returns_code_improvement_model(self):
        client = spec_client()
        client._request.return_value = {"suggestion": SUGGESTION}
        result = GitHubResource(client).update_code_improvement_status(
            PROJECT_ID, SUGGESTION_ID, "open"
        )
        assert result.id == SUGGESTION_ID


class TestGetImprovementsSummary:
    def test_returns_list_of_summary_rows(self):
        client = spec_client()
        client._request.return_value = {"summary": [SUMMARY_ROW]}
        result = GitHubResource(client).get_improvements_summary(PROJECT_ID)
        assert isinstance(result, list)
        assert result[0].category == "security"
        assert result[0].priority == "critical"
        assert result[0].cnt == "3"

    def test_empty_summary(self):
        client = spec_client()
        client._request.return_value = {"summary": []}
        result = GitHubResource(client).get_improvements_summary(PROJECT_ID)
        assert result == []


class TestGetImprovementsHistory:
    def test_returns_list_of_history_items(self):
        client = spec_client()
        client._request.return_value = {"history": [HISTORY_ITEM]}
        result = GitHubResource(client).get_improvements_history(PROJECT_ID)
        assert isinstance(result, list)
        item = result[0]
        assert item.suggestion_count == 12
        assert item.critical_count == 3
        assert item.total_files == 200

    def test_empty_history(self):
        client = spec_client()
        client._request.return_value = {"history": []}
        result = GitHubResource(client).get_improvements_history(PROJECT_ID)
        assert result == []


class TestGetRepoStats:
    def test_calls_stats_endpoint(self):
        client = spec_client()
        client._request.return_value = REPO_STATS
        GitHubResource(client).get_repo_stats(PROJECT_ID)
        args, _ = client._request.call_args
        assert args == ("GET", f"/projects/{PROJECT_ID}/github/improvements/stats")

    def test_maps_repo_meta(self):
        client = spec_client()
        client._request.return_value = REPO_STATS
        result = GitHubResource(client).get_repo_stats(PROJECT_ID)
        assert result.stats.repo is not None
        assert result.stats.repo.full_name == "acme/api"
        assert result.stats.repo.stars == 42

    def test_maps_languages(self):
        client = spec_client()
        client._request.return_value = REPO_STATS
        result = GitHubResource(client).get_repo_stats(PROJECT_ID)
        assert len(result.stats.languages) == 1
        assert result.stats.languages[0].name == "Python"

    def test_maps_local_metrics(self):
        client = spec_client()
        client._request.return_value = REPO_STATS
        result = GitHubResource(client).get_repo_stats(PROJECT_ID)
        m = result.stats.local_metrics
        assert m.analyzed_files == 180
        assert m.total_loc == 22000
        assert m.hotspot_count == 8


@pytest.mark.asyncio
class TestAsyncPhase5:
    """Async variants mirror sync behaviour."""

    async def test_async_generate_code_improvements(self):
        client = spec_client()
        client._request = Mock(return_value={"generated": 4, "repo": "acme/web"})
        from unittest.mock import AsyncMock

        client._request = AsyncMock(return_value={"generated": 4, "repo": "acme/web"})
        result = await AsyncGitHubResource(client).generate_code_improvements(PROJECT_ID)
        assert result.generated == 4

    async def test_async_get_code_improvements(self):
        from unittest.mock import AsyncMock

        client = spec_client()
        client._request = AsyncMock(return_value={"suggestions": [SUGGESTION]})
        result = await AsyncGitHubResource(client).get_code_improvements(PROJECT_ID)
        assert len(result.suggestions) == 1

    async def test_async_get_repo_stats(self):
        from unittest.mock import AsyncMock

        client = spec_client()
        client._request = AsyncMock(return_value=REPO_STATS)
        result = await AsyncGitHubResource(client).get_repo_stats(PROJECT_ID)
        assert result.stats.repo is not None
        assert result.stats.repo.stars == 42
