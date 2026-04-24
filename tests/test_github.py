"""Tests for GitHubResource — ADR-152 GitHub project integration."""

from unittest.mock import Mock

from trix.resources.github import GitHubResource

PROJECT_ID = "proj_abc123"
CONN_ID = "conn_xyz789"

CONNECTION = {
    "id": CONN_ID,
    "project_id": PROJECT_ID,
    "repo_full_name": "acme/api",
    "webhook_active": True,
    "sync_commits": True,
    "sync_pull_requests": True,
    "sync_issues": True,
    "last_webhook_at": "2026-04-20T10:00:00Z",
}

VELOCITY = {
    "merged_last_7_days": 5,
    "merged_last_30_days": 18,
    "avg_cycle_time_hours": 36.5,
    "avg_cycle_time_days": 1.5,
}

CYCLE_TIME = {
    "avg_cycle_days_last_30": 4.2,
    "avg_cycle_days_30_60": 5.1,
    "avg_open_age_days": 8.3,
    "open_issue_count": 12,
    "closed_last_30": 9,
    "trend": "improving",
}

ATTRIBUTION = {
    "total_commits": 120,
    "total_prs": 28,
    "agent_breakdown": {"claude": 15, "copilot": 8},
    "agent_total": 23,
    "human_total": 97,
    "agent_ratio": 0.19,
}

NARRATIVE_RESPONSE = {
    "narrative": "This week the team shipped 5 PRs closing 3 goals.",
    "stored": True,
    "window_days": 7,
}


class TestGitHubResourceConnections:
    """Tests for connection management methods."""

    def test_list_connections(self):
        mock_client = Mock()
        mock_client._request.return_value = {"connections": [CONNECTION], "count": 1}

        resource = GitHubResource(mock_client)
        result = resource.list_connections(PROJECT_ID)

        args, kwargs = mock_client._request.call_args
        assert args == ("GET", f"/projects/{PROJECT_ID}/github")
        assert result.count == 1
        assert result.connections[0].repo_full_name == "acme/api"

    def test_link_repo_returns_webhook_credentials(self):
        mock_client = Mock()
        mock_client._request.return_value = {
            "connection": CONNECTION,
            "webhook_url": "https://api.trixdb.com/webhooks/github/abc",
            "webhook_secret": "s3cr3t",
        }

        resource = GitHubResource(mock_client)
        result = resource.link_repo(
            PROJECT_ID,
            connection_id="oauth_1",
            repo_id="r_123",
            repo_full_name="acme/api",
        )

        args, kwargs = mock_client._request.call_args
        assert args == ("POST", f"/projects/{PROJECT_ID}/github")
        assert "acme/api" in result.webhook_url or result.webhook_secret == "s3cr3t"
        assert result.connection.repo_full_name == "acme/api"

    def test_update_connection_sends_patch(self):
        mock_client = Mock()
        mock_client._request.return_value = {**CONNECTION, "sync_commits": False}

        resource = GitHubResource(mock_client)
        result = resource.update_connection(PROJECT_ID, CONN_ID, sync_commits=False)

        args, kwargs = mock_client._request.call_args
        assert args == ("PATCH", f"/projects/{PROJECT_ID}/github/{CONN_ID}")
        assert kwargs["json"]["sync_commits"] is False
        assert result.sync_commits is False

    def test_update_connection_omits_none_fields(self):
        """Only explicitly-set fields should appear in the PATCH body."""
        mock_client = Mock()
        mock_client._request.return_value = CONNECTION

        resource = GitHubResource(mock_client)
        resource.update_connection(PROJECT_ID, CONN_ID, pr_review_bot_enabled=True)

        _, kwargs = mock_client._request.call_args
        assert "pr_review_bot_enabled" in kwargs["json"]
        assert "sync_commits" not in kwargs["json"]


class TestGitHubResourceActivity:
    """Tests for activity and churn methods."""

    def test_get_activity_defaults(self):
        mock_client = Mock()
        mock_client._request.return_value = {"memories": [], "total": 0, "count": 0}

        resource = GitHubResource(mock_client)
        resource.get_activity(PROJECT_ID)

        _, kwargs = mock_client._request.call_args
        assert kwargs["params"]["type"] == "all"
        assert kwargs["params"]["limit"] == 20

    def test_get_activity_custom_type(self):
        mock_client = Mock()
        mock_client._request.return_value = {"memories": [], "total": 0, "count": 0}

        resource = GitHubResource(mock_client)
        resource.get_activity(PROJECT_ID, type="pull_request", limit=5)

        _, kwargs = mock_client._request.call_args
        assert kwargs["params"]["type"] == "pull_request"
        assert kwargs["params"]["limit"] == 5

    def test_get_churn_files(self):
        mock_client = Mock()
        mock_client._request.return_value = {
            "files": [
                {
                    "file_path": "src/app.py",
                    "repo_full_name": "acme/api",
                    "touch_count": 42,
                    "last_touched_at": "2026-04-20T00:00:00Z",
                }
            ],
            "count": 1,
        }

        resource = GitHubResource(mock_client)
        result = resource.get_churn_files(PROJECT_ID, limit=10)

        assert result.count == 1
        assert result.files[0].file_path == "src/app.py"
        assert result.files[0].touch_count == 42


class TestGitHubResourceQuality:
    """Tests for quality analytics methods."""

    def test_get_quality_summary(self):
        mock_client = Mock()
        mock_client._request.return_value = {
            "summary": {
                "total_files_tracked": 200,
                "hotspot_count": 8,
                "hotspot_ratio": 4,
            },
            "top_hotspots": [],
        }

        resource = GitHubResource(mock_client)
        result = resource.get_quality_summary(PROJECT_ID)

        args, _ = mock_client._request.call_args
        assert args == ("GET", f"/projects/{PROJECT_ID}/github/quality")
        assert result.summary.hotspot_count == 8

    def test_search_symbols(self):
        mock_client = Mock()
        mock_client._request.return_value = {"symbols": [], "count": 0}

        resource = GitHubResource(mock_client)
        resource.search_symbols(PROJECT_ID, "AuthService", limit=5)

        _, kwargs = mock_client._request.call_args
        assert kwargs["params"]["q"] == "AuthService"
        assert kwargs["params"]["limit"] == 5

    def test_get_file_symbols_uses_file_param(self):
        """get_file_symbols must pass 'file', not 'file_path', to the API."""
        mock_client = Mock()
        mock_client._request.return_value = {"symbols": [], "count": 0}

        resource = GitHubResource(mock_client)
        resource.get_file_symbols(PROJECT_ID, "src/auth/service.py")

        _, kwargs = mock_client._request.call_args
        assert kwargs["params"]["file"] == "src/auth/service.py"
        assert "file_path" not in kwargs["params"]


class TestGitHubResourceAnalytics:
    """Tests for Phase 3/4 analytics methods."""

    def test_get_velocity(self):
        mock_client = Mock()
        mock_client._request.return_value = VELOCITY

        resource = GitHubResource(mock_client)
        result = resource.get_velocity(PROJECT_ID)

        args, _ = mock_client._request.call_args
        assert args == ("GET", f"/projects/{PROJECT_ID}/github/velocity")
        assert result.merged_last_7_days == 5
        assert result.avg_cycle_time_days == 1.5

    def test_get_velocity_null_cycle_time(self):
        mock_client = Mock()
        mock_client._request.return_value = {
            **VELOCITY,
            "avg_cycle_time_hours": None,
            "avg_cycle_time_days": None,
        }

        resource = GitHubResource(mock_client)
        result = resource.get_velocity(PROJECT_ID)
        assert result.avg_cycle_time_days is None

    def test_get_flagged_prs(self):
        mock_client = Mock()
        mock_client._request.return_value = {
            "prs": [
                {
                    "id": "mem_1",
                    "summary": "feat: add auth module",
                    "flags": ["pr:scope-creep", "pr:no-tests"],
                    "created_at": "2026-04-19T08:00:00Z",
                }
            ]
        }

        resource = GitHubResource(mock_client)
        result = resource.get_flagged_prs(PROJECT_ID)

        assert len(result.prs) == 1
        assert "pr:scope-creep" in result.prs[0].flags

    def test_get_flagged_prs_empty(self):
        mock_client = Mock()
        mock_client._request.return_value = {"prs": []}

        resource = GitHubResource(mock_client)
        result = resource.get_flagged_prs(PROJECT_ID)
        assert result.prs == []

    def test_get_cycle_time(self):
        mock_client = Mock()
        mock_client._request.return_value = CYCLE_TIME

        resource = GitHubResource(mock_client)
        result = resource.get_cycle_time(PROJECT_ID)

        assert result.trend == "improving"
        assert result.avg_cycle_days_last_30 == 4.2
        assert result.open_issue_count == 12

    def test_get_agent_attribution(self):
        mock_client = Mock()
        mock_client._request.return_value = ATTRIBUTION

        resource = GitHubResource(mock_client)
        result = resource.get_agent_attribution(PROJECT_ID)

        assert result.agent_breakdown == {"claude": 15, "copilot": 8}
        assert abs(result.agent_ratio - 0.19) < 0.001

    def test_get_goal_progress(self):
        # progress is stored as 0.0–1.0 (not 0–100)
        mock_client = Mock()
        mock_client._request.return_value = {
            "goals": [
                {
                    "id": "goal_1",
                    "title": "Reduce p95 latency",
                    "progress": 0.72,
                    "status": "active",
                    "progress_type": "github",
                    "last_github_progress": 0.68,
                    "last_github_updated_at": "2026-04-21T10:00:00Z",
                }
            ]
        }

        resource = GitHubResource(mock_client)
        result = resource.get_goal_progress(PROJECT_ID)

        assert len(result.goals) == 1
        assert result.goals[0].title == "Reduce p95 latency"
        assert abs(result.goals[0].progress - 0.72) < 0.001
        assert result.goals[0].last_github_progress is not None
        assert abs(result.goals[0].last_github_progress - 0.68) < 0.001
        assert result.goals[0].last_github_updated_at == "2026-04-21T10:00:00Z"

    def test_get_release_readiness(self):
        mock_client = Mock()
        mock_client._request.return_value = {
            "score": 85,
            "ready": True,
            "signals": {
                "open_prs": 1,
                "blocking_tasks": 0,
                "goal_completion_pct": 88,
                "scope_creep_prs": 0,
            },
            "details": {"open_prs": [], "blocking_tasks": [], "scope_creep_prs": []},
        }

        resource = GitHubResource(mock_client)
        result = resource.get_release_readiness(PROJECT_ID)

        assert result.score == 85
        assert result.ready is True
        assert result.signals.open_prs == 1


class TestGitHubResourceScan:
    """Tests for scan and delete operations."""

    def test_scan_repo_posts_to_scan_endpoint(self):
        mock_client = Mock()
        mock_client._request.return_value = {
            "scanned": True,
            "commits": 12,
            "prs": 4,
            "issues": 7,
            "files": 28,
            "hotspots": 3,
            "pr_briefs": 2,
        }

        resource = GitHubResource(mock_client)
        result = resource.scan_repo(PROJECT_ID, CONN_ID)

        args, _ = mock_client._request.call_args
        assert args == ("POST", f"/projects/{PROJECT_ID}/github/{CONN_ID}/scan")
        assert result.scanned is True
        assert result.commits == 12
        assert result.pr_briefs == 2

    def test_scan_repo_returns_errors_list(self):
        mock_client = Mock()
        mock_client._request.return_value = {
            "scanned": False,
            "commits": 0,
            "prs": 0,
            "issues": 0,
            "files": 0,
            "hotspots": 0,
            "pr_briefs": 0,
            "errors": ["GitHub API rate limit exceeded"],
        }

        resource = GitHubResource(mock_client)
        result = resource.scan_repo(PROJECT_ID, CONN_ID)

        assert result.scanned is False
        assert result.errors is not None
        assert "rate limit" in result.errors[0]

    def test_delete_connection_sends_delete(self):
        mock_client = Mock()
        mock_client._request.return_value = None

        resource = GitHubResource(mock_client)
        resource.delete_connection(PROJECT_ID, CONN_ID)

        args, _ = mock_client._request.call_args
        assert args == ("DELETE", f"/projects/{PROJECT_ID}/github/{CONN_ID}")


class TestGitHubResourceNarrative:
    """Tests for delivery narrative methods."""

    def test_generate_narrative_posts_with_window_days(self):
        mock_client = Mock()
        mock_client._request.return_value = NARRATIVE_RESPONSE

        resource = GitHubResource(mock_client)
        result = resource.generate_narrative(PROJECT_ID, window_days=7)

        args, kwargs = mock_client._request.call_args
        assert args == ("POST", f"/projects/{PROJECT_ID}/github/narrative")
        assert kwargs["json"]["window_days"] == 7
        assert result.stored is True
        assert "shipped" in result.narrative

    def test_generate_narrative_uses_default_window(self):
        mock_client = Mock()
        mock_client._request.return_value = NARRATIVE_RESPONSE

        resource = GitHubResource(mock_client)
        resource.generate_narrative(PROJECT_ID)

        _, kwargs = mock_client._request.call_args
        assert kwargs["json"]["window_days"] == 7

    def test_get_latest_narrative(self):
        mock_client = Mock()
        mock_client._request.return_value = {
            "narrative": {
                "id": "mem_n1",
                "content": "Week 16 delivery summary…",
                "created_at": "2026-04-21T00:00:00Z",
            }
        }

        resource = GitHubResource(mock_client)
        result = resource.get_latest_narrative(PROJECT_ID)

        args, _ = mock_client._request.call_args
        assert args == ("GET", f"/projects/{PROJECT_ID}/github/narrative")
        assert result.narrative is not None
        assert "Week 16" in result.narrative.content

    def test_get_latest_narrative_when_none_exists(self):
        mock_client = Mock()
        mock_client._request.return_value = {"narrative": None}

        resource = GitHubResource(mock_client)
        result = resource.get_latest_narrative(PROJECT_ID)
        assert result.narrative is None


class TestGitHubResourceFileComplexity:
    """Tests for file complexity analytics."""

    def test_get_file_complexity_returns_metrics(self):
        mock_client = Mock()
        mock_client._request.return_value = {
            "files": [
                {
                    "file_path": "src/auth/service.ts",
                    "repo_full_name": "acme/api",
                    "language": "typescript",
                    "cyclomatic_complexity": 18,
                    "cognitive_complexity": 12,
                    "loc": 320,
                    "hotspot_score": 0.87,
                    "complexity_level": "warning",
                    "computed_at": "2026-04-20T10:00:00Z",
                }
            ],
            "count": 1,
        }

        resource = GitHubResource(mock_client)
        result = resource.get_file_complexity(PROJECT_ID)

        args, _ = mock_client._request.call_args
        assert args == ("GET", f"/projects/{PROJECT_ID}/github/complexity")
        assert len(result.files) == 1
        assert result.files[0].complexity_level == "warning"
        assert abs(result.files[0].hotspot_score - 0.87) < 0.001
        assert result.files[0].cyclomatic_complexity == 18
        assert result.count == 1

    def test_get_file_complexity_with_filters(self):
        mock_client = Mock()
        mock_client._request.return_value = {"files": [], "count": 0}

        resource = GitHubResource(mock_client)
        resource.get_file_complexity(PROJECT_ID, file="src/auth.ts", repo="acme/api")

        _, kwargs = mock_client._request.call_args
        assert kwargs["params"]["file"] == "src/auth.ts"
        assert kwargs["params"]["repo"] == "acme/api"

    def test_get_file_complexity_empty_list(self):
        mock_client = Mock()
        mock_client._request.return_value = {"files": [], "count": 0}

        resource = GitHubResource(mock_client)
        result = resource.get_file_complexity(PROJECT_ID)

        assert result.files == []
        assert result.count == 0
