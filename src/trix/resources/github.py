"""GitHub project integration resource for Trix SDK (ADR-152)."""

from typing import Any, Dict, List, Optional

from .base import BaseSyncResource
from ..utils.security import validate_id
from .github_types import (
    ActivityResponse,
    AgentAttributionResponse,
    ChurnFilesResponse,
    CodeImprovement,
    CodeImprovementsResponse,
    CycleTimeResponse,
    FileComplexityResponse,
    FlaggedPRsResponse,
    PRBrief,  # noqa: F401
    PRBriefsResponse,
    HealthSnapshotResponse,
    GenerateNarrativeResponse,
    GitHubConnection,
    GitHubConnectionsResponse,
    GoalProgressResponse,
    ImprovementGenerateResponse,
    ImprovementsHistoryItem,
    ImprovementSummaryRow,
    LatestNarrativeResponse,
    LinkRepoResponse,
    QualitySummaryResponse,
    ReleaseReadinessResponse,
    RepoStatsResponse,
    ReviewStats,
    ScanRepoResponse,
    SymbolsResponse,
    VelocityResponse,
    WeeklyActivityDay,
    TechnicalDebt,
    QualityGate,
    AgentPRResult,
    PRReviewResult,
    ScanCodeResult,
    CodeSummaryResult,
    CloneGroupsResult,
    DeadExportsResult,
    TestCoverageResult,
    LoadBearingResult,
    BugDensityResult,
)

# Re-export all types so existing imports from this module still work
from .github_types import *  # noqa: F401,F403


# ── Sync resource ──────────────────────────────────────────────────────────


class GitHubResource(BaseSyncResource):
    """Sync resource for GitHub project integration.

    Example:
        >>> connections = client.github.list_connections("project-id")
        >>> churn = client.github.get_churn_files("project-id", limit=10)
    """

    def list_connections(self, project_id: str) -> GitHubConnectionsResponse:
        """List GitHub repos linked to a project."""
        validate_id(project_id, "project")
        response = self._request("GET", f"/projects/{project_id}/github")
        return GitHubConnectionsResponse.model_validate(response)

    def link_repo(
        self,
        project_id: str,
        *,
        connection_id: str,
        repo_id: str,
        repo_full_name: str,
    ) -> LinkRepoResponse:
        """Link a GitHub repo to a project."""
        validate_id(project_id, "project")
        data = {"connection_id": connection_id, "repo_id": repo_id, "repo_full_name": repo_full_name}
        response = self._request("POST", f"/projects/{project_id}/github", json=data)
        return LinkRepoResponse.model_validate(response)

    def get_activity(
        self,
        project_id: str,
        *,
        type: str = "all",
        limit: int = 20,
        offset: int = 0,
    ) -> ActivityResponse:
        """Get GitHub activity memories for a project."""
        validate_id(project_id, "project")
        params: Dict[str, Any] = {"type": type, "limit": limit, "offset": offset}
        response = self._request("GET", f"/projects/{project_id}/github/activity", params=params)
        return ActivityResponse.model_validate(response)

    def get_churn_files(
        self,
        project_id: str,
        *,
        limit: int = 20,
        repo: Optional[str] = None,
    ) -> ChurnFilesResponse:
        """Get the most frequently changed files for a project."""
        validate_id(project_id, "project")
        params: Dict[str, Any] = {"limit": limit}
        if repo is not None:
            params["repo"] = repo
        response = self._request("GET", f"/projects/{project_id}/github/churn", params=params)
        return ChurnFilesResponse.model_validate(response)

    def get_file_complexity(
        self,
        project_id: str,
        *,
        file: Optional[str] = None,
        repo: Optional[str] = None,
    ) -> FileComplexityResponse:
        """Get cyclomatic and cognitive complexity metrics for tracked files."""
        validate_id(project_id, "project")
        params: Dict[str, Any] = {}
        if file is not None:
            params["file"] = file
        if repo is not None:
            params["repo"] = repo
        response = self._request(
            "GET", f"/projects/{project_id}/github/complexity", params=params or None
        )
        return FileComplexityResponse.model_validate(response)

    def get_quality_summary(self, project_id: str) -> QualitySummaryResponse:
        """Get code quality summary including hotspot analysis."""
        validate_id(project_id, "project")
        response = self._request("GET", f"/projects/{project_id}/github/quality")
        return QualitySummaryResponse.model_validate(response)

    def search_symbols(
        self,
        project_id: str,
        q: str,
        *,
        repo: Optional[str] = None,
        limit: int = 20,
    ) -> SymbolsResponse:
        """Search indexed code symbols by query string."""
        validate_id(project_id, "project")
        params: Dict[str, Any] = {"q": q, "limit": limit}
        if repo is not None:
            params["repo"] = repo
        response = self._request("GET", f"/projects/{project_id}/github/symbols", params=params)
        return SymbolsResponse.model_validate(response)

    def get_file_symbols(
        self,
        project_id: str,
        file_path: str,
        *,
        repo: Optional[str] = None,
    ) -> SymbolsResponse:
        """List all symbols in a specific file."""
        validate_id(project_id, "project")
        params: Dict[str, Any] = {"file": file_path}
        if repo is not None:
            params["repo"] = repo
        response = self._request("GET", f"/projects/{project_id}/github/symbols", params=params)
        return SymbolsResponse.model_validate(response)

    def get_release_readiness(self, project_id: str) -> ReleaseReadinessResponse:
        """Get release readiness score and signals."""
        validate_id(project_id, "project")
        response = self._request("GET", f"/projects/{project_id}/github/release-readiness")
        return ReleaseReadinessResponse.model_validate(response)

    def get_velocity(self, project_id: str) -> VelocityResponse:
        """Get PR merge velocity and average cycle time."""
        validate_id(project_id, "project")
        response = self._request("GET", f"/projects/{project_id}/github/velocity")
        return VelocityResponse.model_validate(response)

    def get_health_snapshot(self, project_id: str) -> HealthSnapshotResponse:
        """Get a one-call project health snapshot for agents.

        Aggregates code quality gate, PR velocity, open PR risk signals,
        and top issues. Use as the first call to understand project state.
        """
        validate_id(project_id, "project")
        response = self._request("GET", f"/projects/{project_id}/github/health-snapshot")
        return HealthSnapshotResponse.model_validate(response)

    def get_flagged_prs(self, project_id: str) -> FlaggedPRsResponse:
        """Get risk-flagged pull requests."""
        validate_id(project_id, "project")
        response = self._request("GET", f"/projects/{project_id}/github/flagged-prs")
        return FlaggedPRsResponse.model_validate(response)

    def get_pr_briefs(
        self,
        project_id: str,
        *,
        state: str = "open",
        pr_number: Optional[int] = None,
        limit: int = 20,
        min_quality_score: Optional[int] = None,
        max_quality_score: Optional[int] = None,
    ) -> PRBriefsResponse:
        """Get PR briefs with quality scores and risk signals.

        Args:
            project_id: Project UUID.
            state: Filter by PR state — 'open', 'closed', or 'all'.
            pr_number: Fetch brief for a specific PR number.
            limit: Max results to return (1–50).
            min_quality_score: Exclude PRs below this quality threshold (0–100).
            max_quality_score: Exclude PRs above this quality threshold — use to surface risky PRs.
        """
        validate_id(project_id, "project")
        params: Dict[str, Any] = {"state": state, "limit": limit}
        if pr_number is not None:
            params["pr_number"] = pr_number
        if min_quality_score is not None:
            params["min_quality_score"] = min_quality_score
        if max_quality_score is not None:
            params["max_quality_score"] = max_quality_score
        response = self._request(
            "GET", f"/projects/{project_id}/github/pr-briefs", params=params
        )
        return PRBriefsResponse.model_validate(response)

    def get_cycle_time(self, project_id: str) -> CycleTimeResponse:
        """Get issue cycle time trends."""
        validate_id(project_id, "project")
        response = self._request("GET", f"/projects/{project_id}/github/cycle-time")
        return CycleTimeResponse.model_validate(response)

    def get_agent_attribution(self, project_id: str) -> AgentAttributionResponse:
        """Get AI vs human commit/PR attribution breakdown."""
        validate_id(project_id, "project")
        response = self._request("GET", f"/projects/{project_id}/github/agent-attribution")
        return AgentAttributionResponse.model_validate(response)

    def get_goal_progress(self, project_id: str) -> GoalProgressResponse:
        """Get goal progress driven by GitHub issue activity."""
        validate_id(project_id, "project")
        response = self._request("GET", f"/projects/{project_id}/github/goal-progress")
        return GoalProgressResponse.model_validate(response)

    def update_connection(
        self,
        project_id: str,
        connection_id: str,
        *,
        pr_review_bot_enabled: Optional[bool] = None,
        sync_commits: Optional[bool] = None,
        sync_pull_requests: Optional[bool] = None,
        sync_issues: Optional[bool] = None,
    ) -> GitHubConnection:
        """Update a GitHub connection's settings."""
        validate_id(project_id, "project")
        data: Dict[str, Any] = {}
        if pr_review_bot_enabled is not None:
            data["pr_review_bot_enabled"] = pr_review_bot_enabled
        if sync_commits is not None:
            data["sync_commits"] = sync_commits
        if sync_pull_requests is not None:
            data["sync_pull_requests"] = sync_pull_requests
        if sync_issues is not None:
            data["sync_issues"] = sync_issues
        response = self._request("PATCH", f"/projects/{project_id}/github/{connection_id}", json=data)
        return GitHubConnection.model_validate(response)

    def generate_narrative(
        self, project_id: str, *, window_days: int = 7
    ) -> GenerateNarrativeResponse:
        """Generate a narrative summary of recent GitHub activity."""
        validate_id(project_id, "project")
        response = self._request(
            "POST", f"/projects/{project_id}/github/narrative", json={"window_days": window_days}
        )
        return GenerateNarrativeResponse.model_validate(response)

    def get_latest_narrative(self, project_id: str) -> LatestNarrativeResponse:
        """Get the latest generated narrative for a project."""
        validate_id(project_id, "project")
        response = self._request("GET", f"/projects/{project_id}/github/narrative")
        return LatestNarrativeResponse.model_validate(response)

    def scan_repo(self, project_id: str, connection_id: str) -> ScanRepoResponse:
        """Trigger a full backfill scan of a linked GitHub repository."""
        validate_id(project_id, "project")
        validate_id(connection_id, "connection")
        response = self._request(
            "POST", f"/projects/{project_id}/github/{connection_id}/scan", json={}
        )
        return ScanRepoResponse.model_validate(response)

    def delete_connection(self, project_id: str, connection_id: str) -> None:
        """Remove a GitHub repository link from a project."""
        validate_id(project_id, "project")
        validate_id(connection_id, "connection")
        self._request("DELETE", f"/projects/{project_id}/github/{connection_id}")

    # ── Phase 5: Code Quality Scanner + Repo Stats ────────────────────────

    def generate_code_improvements(self, project_id: str) -> ImprovementGenerateResponse:
        """Trigger a code quality scan (Dependabot + code scanning + secret scanning + LLM)."""
        validate_id(project_id, "project")
        response = self._request(
            "POST", f"/projects/{project_id}/github/improvements/generate", json={}
        )
        return ImprovementGenerateResponse.model_validate(response)

    def get_code_improvements(
        self,
        project_id: str,
        *,
        category: Optional[str] = None,
        priority: Optional[str] = None,
        status: str = "open",
        file_path: Optional[str] = None,
    ) -> CodeImprovementsResponse:
        """List code improvement suggestions with optional filters.

        Args:
            file_path: Filter by file path substring, e.g. "src/auth" returns
                       all findings in that directory.
        """
        validate_id(project_id, "project")
        params: Dict[str, Any] = {"status": status}
        if category is not None:
            params["category"] = category
        if priority is not None:
            params["priority"] = priority
        if file_path is not None:
            params["file_path"] = file_path
        response = self._request(
            "GET", f"/projects/{project_id}/github/improvements", params=params
        )
        return CodeImprovementsResponse.model_validate(response)

    def create_issue_from_suggestion(
        self, project_id: str, suggestion_id: str
    ) -> Dict[str, Any]:
        """Push a code quality finding to GitHub Issues and mark it in_progress."""
        validate_id(project_id, "project")
        validate_id(suggestion_id, "suggestion")
        return self._request(
            "POST",
            f"/projects/{project_id}/github/improvements/{suggestion_id}/create-issue",
        )

    def update_code_improvement_status(
        self, project_id: str, suggestion_id: str, status: str
    ) -> CodeImprovement:
        """Update the status of a code improvement suggestion."""
        validate_id(project_id, "project")
        validate_id(suggestion_id, "suggestion")
        response = self._request(
            "PATCH",
            f"/projects/{project_id}/github/improvements/{suggestion_id}",
            json={"status": status},
        )
        return CodeImprovement.model_validate(response["suggestion"])

    def get_improvements_summary(self, project_id: str) -> List[ImprovementSummaryRow]:
        """Get priority/category summary counts for open suggestions."""
        validate_id(project_id, "project")
        response = self._request("GET", f"/projects/{project_id}/github/improvements/summary")
        return [ImprovementSummaryRow.model_validate(r) for r in response.get("summary", [])]

    def get_improvements_history(self, project_id: str) -> List[ImprovementsHistoryItem]:
        """Get historical code quality metric snapshots."""
        validate_id(project_id, "project")
        response = self._request("GET", f"/projects/{project_id}/github/improvements/history")
        return [ImprovementsHistoryItem.model_validate(r) for r in response.get("history", [])]

    def get_repo_stats(self, project_id: str) -> RepoStatsResponse:
        """Fetch live repo stats: stars, languages, contributors, LOC, README preview."""
        validate_id(project_id, "project")
        response = self._request("GET", f"/projects/{project_id}/github/improvements/stats")
        return RepoStatsResponse.model_validate(response)

    def get_review_stats(self, project_id: str) -> ReviewStats:
        """Get PR review analytics: approval rate + top reviewers (last 30 days)."""
        validate_id(project_id, "project")
        response = self._request("GET", f"/projects/{project_id}/github/review-stats")
        return ReviewStats.model_validate(response)

    def get_weekly_activity(self, project_id: str) -> List[WeeklyActivityDay]:
        """Get daily commit/PR/issue counts for the last 52 weeks (heatmap data)."""
        validate_id(project_id, "project")
        response = self._request("GET", f"/projects/{project_id}/github/activity/weekly")
        return [WeeklyActivityDay.model_validate(d) for d in (response if isinstance(response, list) else [])]

    def get_code_debt(self, project_id: str) -> TechnicalDebt:
        """Get technical debt aggregated by category (minutes + hours)."""
        validate_id(project_id, "project")
        response = self._request("GET", f"/projects/{project_id}/github/improvements/debt")
        return TechnicalDebt.model_validate(response)

    def get_quality_gate(self, project_id: str) -> QualityGate:
        """Evaluate quality gate — returns pass/fail with per-check detail."""
        validate_id(project_id, "project")
        response = self._request("GET", f"/projects/{project_id}/github/improvements/quality-gate")
        return QualityGate.model_validate(response)

    def query_code(self, project_id: str, query: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a CQL query over code metrics (files or functions)."""
        validate_id(project_id, "project")
        return self._request("POST", f"/projects/{project_id}/github/query", json=query)

    def review_pr(
        self,
        project_id: str,
        connection_id: str,
        pr_number: int,
        *,
        event: str = "COMMENT",
        dry_run: bool = False,
    ) -> PRReviewResult:
        """Run an agent PR review and post a structured comment to GitHub."""
        validate_id(project_id, "project")
        response = self._request(
            "POST",
            f"/projects/{project_id}/github/review-pr",
            json={"connection_id": connection_id, "pr_number": pr_number, "event": event, "dry_run": dry_run},
        )
        return PRReviewResult.model_validate(response)

    def create_pr(
        self,
        project_id: str,
        *,
        connection_id: str,
        branch_name: str,
        commit_message: str,
        pr_title: str,
        changes: List[Dict[str, str]],
        base_branch: str = "main",
        pr_body: str = "",
    ) -> AgentPRResult:
        """Create a GitHub PR with agent-authored file changes (max 50 files)."""
        validate_id(project_id, "project")
        response = self._request(
            "POST",
            f"/projects/{project_id}/github/create-pr",
            json={"connection_id": connection_id, "branch_name": branch_name, "base_branch": base_branch, "commit_message": commit_message, "pr_title": pr_title, "pr_body": pr_body, "changes": changes},
        )
        return AgentPRResult.model_validate(response)

    def scan_code(self, project_id: str, *, file_path: str, content: str) -> ScanCodeResult:
        """Scan arbitrary file content with all SAST + secret scanners (no GitHub auth needed)."""
        validate_id(project_id, "project")
        response = self._request(
            "POST",
            f"/projects/{project_id}/github/scan-code",
            json={"file_path": file_path, "content": content},
        )
        return ScanCodeResult.model_validate(response)

    def get_code_summary(self, project_id: str) -> CodeSummaryResult:
        """Combined code health snapshot — quality gate, debt, hotspots, smells, languages."""
        validate_id(project_id, "project")
        return CodeSummaryResult.model_validate(
            self._request("GET", f"/projects/{project_id}/github/code-summary")
        )

    def get_clone_groups(self, project_id: str) -> CloneGroupsResult:
        """Structural code clone groups — sets of functions with identical normalised structure."""
        validate_id(project_id, "project")
        return CloneGroupsResult.model_validate(
            self._request("GET", f"/projects/{project_id}/github/clone-groups")
        )

    def get_dead_exports(self, project_id: str) -> DeadExportsResult:
        """Unused exported symbols in JS/TS files (dead code candidates)."""
        validate_id(project_id, "project")
        return DeadExportsResult.model_validate(
            self._request("GET", f"/projects/{project_id}/github/dead-exports")
        )

    def get_test_coverage(self, project_id: str) -> TestCoverageResult:
        """Test file coverage by naming convention — source files without paired tests."""
        validate_id(project_id, "project")
        return TestCoverageResult.model_validate(
            self._request("GET", f"/projects/{project_id}/github/test-coverage")
        )

    def get_load_bearing_functions(
        self, project_id: str, *, min_callers: int = 3
    ) -> LoadBearingResult:
        """Functions called by many files — high blast-radius, risky to change."""
        validate_id(project_id, "project")
        return LoadBearingResult.model_validate(
            self._request("GET", f"/projects/{project_id}/github/load-bearing?min_callers={min_callers}")
        )

    def get_bug_density(self, project_id: str) -> BugDensityResult:
        """Per-file issue density — open suggestions per 1,000 LOC, ranked by density."""
        validate_id(project_id, "project")
        return BugDensityResult.model_validate(
            self._request("GET", f"/projects/{project_id}/github/bug-density")
        )
