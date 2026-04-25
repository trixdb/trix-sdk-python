"""Async GitHub project integration resource for Trix SDK (ADR-152)."""

from typing import Any, Dict, List, Optional

from .base import BaseAsyncResource
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
    GoalProgressHistoryResponse,
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
    ActiveBranchesResult,
    ContributorQualityResult,
    PrAgingResult,
    PrSizeDistributionResult,
    ReviewTurnaroundResult,
    WorkQueueResult,
    ReviewerWorkloadResult,
    ApprovedPRsResult,
    IssueBacklogResult,
    ReviewCoverageResult,
    IssueAssigneesResult,
    CommitLeadersResult,
    LabelVelocityResult,
    MilestonesResult,
    PRQualityWeek,
    WeekOverWeekResult,
    IssueTriageResult,
    IssueFlowResult,
    IssueCycleTimeResult,
    IssueThroughputResult,
    IssueResolversResult,
    CycleTimeTrendResult,
    PrMergeTimeResult,
    ContributorMomentumResult,
    AgentAuditResult,
    ScopeCreepResult,
    AssigneeCycleTimeResult,
    PRTaskAlignmentResult,
    TestGapResult,
    DORAResult,
    AIvsHumanResult,
    BusFactorResult,
)


class AsyncGitHubResource(BaseAsyncResource):
    """Async resource for GitHub project integration.

    Example:
        >>> connections = await client.github.list_connections("project-id")
        >>> churn = await client.github.get_churn_files("project-id", limit=10)
    """

    async def list_connections(self, project_id: str) -> GitHubConnectionsResponse:
        """List GitHub repos linked to a project (async)."""
        validate_id(project_id, "project")
        response = await self._request("GET", f"/projects/{project_id}/github")
        return GitHubConnectionsResponse.model_validate(response)

    async def link_repo(
        self,
        project_id: str,
        *,
        connection_id: str,
        repo_id: str,
        repo_full_name: str,
    ) -> LinkRepoResponse:
        """Link a GitHub repo to a project (async)."""
        validate_id(project_id, "project")
        data = {
            "connection_id": connection_id,
            "repo_id": repo_id,
            "repo_full_name": repo_full_name,
        }
        response = await self._request("POST", f"/projects/{project_id}/github", json=data)
        return LinkRepoResponse.model_validate(response)

    async def get_activity(
        self,
        project_id: str,
        *,
        type: str = "all",
        limit: int = 20,
        offset: int = 0,
    ) -> ActivityResponse:
        """Get GitHub activity memories for a project (async)."""
        validate_id(project_id, "project")
        params: Dict[str, Any] = {"type": type, "limit": limit, "offset": offset}
        response = await self._request(
            "GET", f"/projects/{project_id}/github/activity", params=params
        )
        return ActivityResponse.model_validate(response)

    async def get_churn_files(
        self,
        project_id: str,
        *,
        limit: int = 20,
        repo: Optional[str] = None,
    ) -> ChurnFilesResponse:
        """Get the most frequently changed files for a project (async)."""
        validate_id(project_id, "project")
        params: Dict[str, Any] = {"limit": limit}
        if repo is not None:
            params["repo"] = repo
        response = await self._request("GET", f"/projects/{project_id}/github/churn", params=params)
        return ChurnFilesResponse.model_validate(response)

    async def get_file_complexity(
        self,
        project_id: str,
        *,
        file: Optional[str] = None,
        repo: Optional[str] = None,
    ) -> FileComplexityResponse:
        """Get cyclomatic and cognitive complexity metrics for tracked files (async)."""
        validate_id(project_id, "project")
        params: Dict[str, Any] = {}
        if file is not None:
            params["file"] = file
        if repo is not None:
            params["repo"] = repo
        response = await self._request(
            "GET", f"/projects/{project_id}/github/complexity", params=params or None
        )
        return FileComplexityResponse.model_validate(response)

    async def get_quality_summary(self, project_id: str) -> QualitySummaryResponse:
        """Get code quality summary including hotspot analysis (async)."""
        validate_id(project_id, "project")
        response = await self._request("GET", f"/projects/{project_id}/github/quality")
        return QualitySummaryResponse.model_validate(response)

    async def search_symbols(
        self,
        project_id: str,
        q: str,
        *,
        repo: Optional[str] = None,
        limit: int = 20,
    ) -> SymbolsResponse:
        """Search indexed code symbols by query string (async)."""
        validate_id(project_id, "project")
        params: Dict[str, Any] = {"q": q, "limit": limit}
        if repo is not None:
            params["repo"] = repo
        response = await self._request(
            "GET", f"/projects/{project_id}/github/symbols", params=params
        )
        return SymbolsResponse.model_validate(response)

    async def get_file_symbols(
        self,
        project_id: str,
        file_path: str,
        *,
        repo: Optional[str] = None,
    ) -> SymbolsResponse:
        """List all symbols in a specific file (async)."""
        validate_id(project_id, "project")
        params: Dict[str, Any] = {"file": file_path}
        if repo is not None:
            params["repo"] = repo
        response = await self._request(
            "GET", f"/projects/{project_id}/github/symbols", params=params
        )
        return SymbolsResponse.model_validate(response)

    async def get_release_readiness(self, project_id: str) -> ReleaseReadinessResponse:
        """Get release readiness score and signals (async)."""
        validate_id(project_id, "project")
        response = await self._request("GET", f"/projects/{project_id}/github/release-readiness")
        return ReleaseReadinessResponse.model_validate(response)

    async def get_velocity(self, project_id: str) -> VelocityResponse:
        """Get PR merge velocity and average cycle time (async)."""
        validate_id(project_id, "project")
        response = await self._request("GET", f"/projects/{project_id}/github/velocity")
        return VelocityResponse.model_validate(response)

    async def get_health_snapshot(self, project_id: str) -> HealthSnapshotResponse:
        """Get a one-call project health snapshot for agents (async).

        Aggregates code quality gate, PR velocity, open PR risk signals,
        and top issues. Use as the first call to understand project state.
        """
        validate_id(project_id, "project")
        response = await self._request("GET", f"/projects/{project_id}/github/health-snapshot")
        return HealthSnapshotResponse.model_validate(response)

    async def get_flagged_prs(self, project_id: str) -> FlaggedPRsResponse:
        """Get risk-flagged pull requests (async)."""
        validate_id(project_id, "project")
        response = await self._request("GET", f"/projects/{project_id}/github/flagged-prs")
        return FlaggedPRsResponse.model_validate(response)

    async def get_pr_briefs(
        self,
        project_id: str,
        *,
        state: str = "open",
        pr_number: Optional[int] = None,
        limit: int = 20,
        min_quality_score: Optional[int] = None,
        max_quality_score: Optional[int] = None,
        agent: Optional[str] = None,
    ) -> PRBriefsResponse:
        """Get PR briefs with quality scores and risk signals (async).

        Args:
            project_id: Project UUID.
            state: Filter by PR state — 'open', 'closed', or 'all'.
            pr_number: Fetch brief for a specific PR number.
            limit: Max results to return (1–50).
            min_quality_score: Exclude PRs below this quality threshold (0–100).
            max_quality_score: Exclude PRs above this threshold — use to surface risky PRs.
            agent: Filter to PRs by a specific AI agent: 'claude', 'copilot', 'cursor', 'gemini'.
        """
        validate_id(project_id, "project")
        params: Dict[str, Any] = {"state": state, "limit": limit}
        if pr_number is not None:
            params["pr_number"] = pr_number
        if min_quality_score is not None:
            params["min_quality_score"] = min_quality_score
        if max_quality_score is not None:
            params["max_quality_score"] = max_quality_score
        if agent is not None:
            params["agent"] = agent
        response = await self._request(
            "GET", f"/projects/{project_id}/github/pr-briefs", params=params
        )
        return PRBriefsResponse.model_validate(response)

    async def get_cycle_time(self, project_id: str) -> CycleTimeResponse:
        """Get issue cycle time trends (async)."""
        validate_id(project_id, "project")
        response = await self._request("GET", f"/projects/{project_id}/github/cycle-time")
        return CycleTimeResponse.model_validate(response)

    async def get_agent_attribution(self, project_id: str) -> AgentAttributionResponse:
        """Get AI vs human commit/PR attribution breakdown (async)."""
        validate_id(project_id, "project")
        response = await self._request("GET", f"/projects/{project_id}/github/agent-attribution")
        return AgentAttributionResponse.model_validate(response)

    async def get_goal_progress(self, project_id: str) -> GoalProgressResponse:
        """Get goal progress driven by GitHub issue activity (async)."""
        validate_id(project_id, "project")
        response = await self._request("GET", f"/projects/{project_id}/github/goal-progress")
        return GoalProgressResponse.model_validate(response)

    async def get_goal_progress_history(
        self, project_id: str, limit: int = 20
    ) -> GoalProgressHistoryResponse:
        """Get chronological feed of GitHub-driven goal progress events (async)."""
        validate_id(project_id, "project")
        response = await self._request(
            "GET", f"/projects/{project_id}/github/goal-progress-history?limit={limit}"
        )
        return GoalProgressHistoryResponse.model_validate(response)

    async def update_connection(
        self,
        project_id: str,
        connection_id: str,
        *,
        pr_review_bot_enabled: Optional[bool] = None,
        sync_commits: Optional[bool] = None,
        sync_pull_requests: Optional[bool] = None,
        sync_issues: Optional[bool] = None,
    ) -> GitHubConnection:
        """Update a GitHub connection's settings (async)."""
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
        response = await self._request(
            "PATCH", f"/projects/{project_id}/github/{connection_id}", json=data
        )
        return GitHubConnection.model_validate(response)

    async def generate_narrative(
        self, project_id: str, *, window_days: int = 7
    ) -> GenerateNarrativeResponse:
        """Generate a narrative summary of recent GitHub activity (async)."""
        validate_id(project_id, "project")
        response = await self._request(
            "POST",
            f"/projects/{project_id}/github/narrative",
            json={"window_days": window_days},
        )
        return GenerateNarrativeResponse.model_validate(response)

    async def get_latest_narrative(self, project_id: str) -> LatestNarrativeResponse:
        """Get the latest generated narrative for a project (async)."""
        validate_id(project_id, "project")
        response = await self._request("GET", f"/projects/{project_id}/github/narrative")
        return LatestNarrativeResponse.model_validate(response)

    async def scan_repo(self, project_id: str, connection_id: str) -> ScanRepoResponse:
        """Trigger a full backfill scan of a linked GitHub repository (async)."""
        validate_id(project_id, "project")
        validate_id(connection_id, "connection")
        response = await self._request(
            "POST", f"/projects/{project_id}/github/{connection_id}/scan", json={}
        )
        return ScanRepoResponse.model_validate(response)

    async def delete_connection(self, project_id: str, connection_id: str) -> None:
        """Remove a GitHub repository link from a project (async)."""
        validate_id(project_id, "project")
        validate_id(connection_id, "connection")
        await self._request("DELETE", f"/projects/{project_id}/github/{connection_id}")

    # ── Phase 5: Code Quality Scanner + Repo Stats ────────────────────────

    async def generate_code_improvements(self, project_id: str) -> ImprovementGenerateResponse:
        """Trigger a code quality scan (Dependabot + code scanning + secret scanning + LLM)."""
        validate_id(project_id, "project")
        response = await self._request(
            "POST", f"/projects/{project_id}/github/improvements/generate", json={}
        )
        return ImprovementGenerateResponse.model_validate(response)

    async def get_code_improvements(
        self,
        project_id: str,
        *,
        category: Optional[str] = None,
        priority: Optional[str] = None,
        status: str = "open",
        file_path: Optional[str] = None,
    ) -> CodeImprovementsResponse:
        """List code improvement suggestions with optional filters (async).

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
        response = await self._request(
            "GET", f"/projects/{project_id}/github/improvements", params=params
        )
        return CodeImprovementsResponse.model_validate(response)

    async def create_issue_from_suggestion(
        self, project_id: str, suggestion_id: str
    ) -> Dict[str, Any]:
        """Push a code quality finding to GitHub Issues and mark it in_progress (async)."""
        validate_id(project_id, "project")
        validate_id(suggestion_id, "suggestion")
        return await self._request(
            "POST",
            f"/projects/{project_id}/github/improvements/{suggestion_id}/create-issue",
        )

    async def update_code_improvement_status(
        self, project_id: str, suggestion_id: str, status: str
    ) -> CodeImprovement:
        """Update the status of a code improvement suggestion (async)."""
        validate_id(project_id, "project")
        validate_id(suggestion_id, "suggestion")
        response = await self._request(
            "PATCH",
            f"/projects/{project_id}/github/improvements/{suggestion_id}",
            json={"status": status},
        )
        return CodeImprovement.model_validate(response["suggestion"])

    async def get_improvements_summary(self, project_id: str) -> List[ImprovementSummaryRow]:
        """Get priority/category summary counts for open suggestions (async)."""
        validate_id(project_id, "project")
        response = await self._request("GET", f"/projects/{project_id}/github/improvements/summary")
        return [ImprovementSummaryRow.model_validate(r) for r in response.get("summary", [])]

    async def get_improvements_history(self, project_id: str) -> List[ImprovementsHistoryItem]:
        """Get historical code quality metric snapshots (async)."""
        validate_id(project_id, "project")
        response = await self._request("GET", f"/projects/{project_id}/github/improvements/history")
        return [ImprovementsHistoryItem.model_validate(r) for r in response.get("history", [])]

    async def get_repo_stats(self, project_id: str) -> RepoStatsResponse:
        """Fetch live repo stats: stars, languages, contributors, LOC, README preview (async)."""
        validate_id(project_id, "project")
        response = await self._request("GET", f"/projects/{project_id}/github/improvements/stats")
        return RepoStatsResponse.model_validate(response)

    async def get_review_stats(self, project_id: str) -> ReviewStats:
        """Get PR review analytics: approval rate + top reviewers (last 30 days) (async)."""
        validate_id(project_id, "project")
        response = await self._request("GET", f"/projects/{project_id}/github/review-stats")
        return ReviewStats.model_validate(response)

    async def get_weekly_activity(self, project_id: str) -> List[WeeklyActivityDay]:
        """Get daily commit/PR/issue counts for the last 52 weeks (heatmap data) (async)."""
        validate_id(project_id, "project")
        response = await self._request("GET", f"/projects/{project_id}/github/activity/weekly")
        return [
            WeeklyActivityDay.model_validate(d)
            for d in (response if isinstance(response, list) else [])
        ]

    async def get_code_debt(self, project_id: str) -> TechnicalDebt:
        """Get technical debt aggregated by category (minutes + hours) (async)."""
        validate_id(project_id, "project")
        response = await self._request("GET", f"/projects/{project_id}/github/improvements/debt")
        return TechnicalDebt.model_validate(response)

    async def get_quality_gate(self, project_id: str) -> QualityGate:
        """Evaluate quality gate — returns pass/fail with per-check detail (async)."""
        validate_id(project_id, "project")
        response = await self._request(
            "GET", f"/projects/{project_id}/github/improvements/quality-gate"
        )
        return QualityGate.model_validate(response)

    async def query_code(self, project_id: str, query: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a CQL query over code metrics (files or functions) (async)."""
        validate_id(project_id, "project")
        return await self._request("POST", f"/projects/{project_id}/github/query", json=query)

    async def review_pr(
        self,
        project_id: str,
        connection_id: str,
        pr_number: int,
        *,
        event: str = "COMMENT",
        dry_run: bool = False,
    ) -> PRReviewResult:
        """Run an agent PR review and post a structured comment to GitHub (async)."""
        validate_id(project_id, "project")
        response = await self._request(
            "POST",
            f"/projects/{project_id}/github/review-pr",
            json={
                "connection_id": connection_id,
                "pr_number": pr_number,
                "event": event,
                "dry_run": dry_run,
            },
        )
        return PRReviewResult.model_validate(response)

    async def create_pr(
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
        """Create a GitHub PR with agent-authored file changes (max 50 files) (async)."""
        validate_id(project_id, "project")
        response = await self._request(
            "POST",
            f"/projects/{project_id}/github/create-pr",
            json={
                "connection_id": connection_id,
                "branch_name": branch_name,
                "base_branch": base_branch,
                "commit_message": commit_message,
                "pr_title": pr_title,
                "pr_body": pr_body,
                "changes": changes,
            },
        )
        return AgentPRResult.model_validate(response)

    async def scan_code(self, project_id: str, *, file_path: str, content: str) -> ScanCodeResult:
        """Scan arbitrary file content with all SAST + secret scanners (no GitHub auth needed) (async)."""
        validate_id(project_id, "project")
        response = await self._request(
            "POST",
            f"/projects/{project_id}/github/scan-code",
            json={"file_path": file_path, "content": content},
        )
        return ScanCodeResult.model_validate(response)

    async def get_code_summary(self, project_id: str) -> CodeSummaryResult:
        """Combined code health snapshot — quality gate, debt, hotspots, smells, languages (async)."""
        validate_id(project_id, "project")
        return CodeSummaryResult.model_validate(
            await self._request("GET", f"/projects/{project_id}/github/code-summary")
        )

    async def get_clone_groups(self, project_id: str) -> CloneGroupsResult:
        """Structural code clone groups (async)."""
        validate_id(project_id, "project")
        return CloneGroupsResult.model_validate(
            await self._request("GET", f"/projects/{project_id}/github/clone-groups")
        )

    async def get_dead_exports(self, project_id: str) -> DeadExportsResult:
        """Unused exported symbols in JS/TS files (async)."""
        validate_id(project_id, "project")
        return DeadExportsResult.model_validate(
            await self._request("GET", f"/projects/{project_id}/github/dead-exports")
        )

    async def get_test_coverage(self, project_id: str) -> TestCoverageResult:
        """Test file coverage by naming convention (async)."""
        validate_id(project_id, "project")
        return TestCoverageResult.model_validate(
            await self._request("GET", f"/projects/{project_id}/github/test-coverage")
        )

    async def get_load_bearing_functions(
        self, project_id: str, *, min_callers: int = 3
    ) -> LoadBearingResult:
        """High callerCount functions — risky to change (async)."""
        validate_id(project_id, "project")
        return LoadBearingResult.model_validate(
            await self._request(
                "GET", f"/projects/{project_id}/github/load-bearing?min_callers={min_callers}"
            )
        )

    async def get_bug_density(self, project_id: str) -> BugDensityResult:
        """Per-file issue density — open suggestions per 1,000 LOC (async)."""
        validate_id(project_id, "project")
        return BugDensityResult.model_validate(
            await self._request("GET", f"/projects/{project_id}/github/bug-density")
        )

    async def get_pr_quality_trend(self, project_id: str) -> List[PRQualityWeek]:
        """Weekly PR quality score trend — 12-week rolling window (async).

        Returns one data point per week that had at least one reviewed PR.
        Use this to track whether code quality is improving or declining over time.
        """
        validate_id(project_id, "project")
        data = await self._request("GET", f"/projects/{project_id}/github/pr-quality-trend")
        return [PRQualityWeek.model_validate(w) for w in data]

    async def get_active_branches(self, project_id: str) -> ActiveBranchesResult:
        """Active branches derived from commit memories with staleness detection (>14 days) (async)."""
        validate_id(project_id, "project")
        return ActiveBranchesResult.model_validate(
            await self._request("GET", f"/projects/{project_id}/github/branches")
        )

    async def get_contributor_quality(self, project_id: str) -> ContributorQualityResult:
        """Per-contributor PR quality stats — avg score, test coverage %, PR count (async)."""
        validate_id(project_id, "project")
        return ContributorQualityResult.model_validate(
            await self._request("GET", f"/projects/{project_id}/github/contributor-quality")
        )

    async def get_pr_aging(self, project_id: str) -> PrAgingResult:
        """Open PRs sorted oldest-first with ageDays + isStale flag (async)."""
        validate_id(project_id, "project")
        return PrAgingResult.model_validate(
            await self._request("GET", f"/projects/{project_id}/github/pr-aging")
        )

    async def get_pr_size_distribution(self, project_id: str) -> PrSizeDistributionResult:
        """PR size distribution (Small/Medium/Large/Extra-large) with quality + test coverage (async)."""
        validate_id(project_id, "project")
        return PrSizeDistributionResult.model_validate(
            await self._request("GET", f"/projects/{project_id}/github/pr-size-distribution")
        )

    async def get_review_turnaround(self, project_id: str) -> ReviewTurnaroundResult:
        """Review turnaround time — avg hours from PR open to first review (async)."""
        validate_id(project_id, "project")
        return ReviewTurnaroundResult.model_validate(
            await self._request("GET", f"/projects/{project_id}/github/review-turnaround")
        )

    async def get_work_queue(self, project_id: str) -> WorkQueueResult:
        """Prioritized work queue — synthesizes all GitHub signals into action items (async)."""
        validate_id(project_id, "project")
        return WorkQueueResult.model_validate(
            await self._request("GET", f"/projects/{project_id}/github/work-queue")
        )

    async def get_reviewer_workload(self, project_id: str) -> ReviewerWorkloadResult:
        """Reviewer workload — pending review queue and historical speed per reviewer (async)."""
        validate_id(project_id, "project")
        return ReviewerWorkloadResult.model_validate(
            await self._request("GET", f"/projects/{project_id}/github/reviewer-workload")
        )

    async def get_approved_prs(self, project_id: str) -> ApprovedPRsResult:
        """Approved-but-not-merged PRs — open PRs with ≥1 approval, ready to ship (async)."""
        validate_id(project_id, "project")
        return ApprovedPRsResult.model_validate(
            await self._request("GET", f"/projects/{project_id}/github/approved-prs")
        )

    async def get_issue_backlog(self, project_id: str) -> IssueBacklogResult:
        """Issue backlog health — unassigned/unlabeled counts, label distribution, oldest issues (async)."""
        validate_id(project_id, "project")
        return IssueBacklogResult.model_validate(
            await self._request("GET", f"/projects/{project_id}/github/issue-backlog")
        )

    async def get_review_coverage(self, project_id: str) -> ReviewCoverageResult:
        """PR review coverage — % of merged PRs (last 90d) that received at least one review (async)."""
        validate_id(project_id, "project")
        return ReviewCoverageResult.model_validate(
            await self._request("GET", f"/projects/{project_id}/github/review-coverage")
        )

    async def get_label_velocity(self, project_id: str, days: int = 30) -> LabelVelocityResult:
        """Issue label velocity — opened vs closed per label, worst-accumulating first (async)."""
        validate_id(project_id, "project")
        return LabelVelocityResult.model_validate(
            await self._request("GET", f"/projects/{project_id}/github/label-velocity?days={days}")
        )

    async def get_commit_leaders(self, project_id: str, days: int = 30) -> CommitLeadersResult:
        """Commit leaders — top contributors by commit count over the last N days (async)."""
        validate_id(project_id, "project")
        return CommitLeadersResult.model_validate(
            await self._request("GET", f"/projects/{project_id}/github/commit-leaders?days={days}")
        )

    async def get_issue_assignees(self, project_id: str) -> IssueAssigneesResult:
        """Issue assignee workload — open issue counts per contributor, most overloaded first (async)."""
        validate_id(project_id, "project")
        return IssueAssigneesResult.model_validate(
            await self._request("GET", f"/projects/{project_id}/github/issue-assignees")
        )

    async def get_milestones(self, project_id: str) -> MilestonesResult:
        """Milestone progress — open/closed issue counts per GitHub milestone, least-complete first (async)."""
        validate_id(project_id, "project")
        return MilestonesResult.model_validate(
            await self._request("GET", f"/projects/{project_id}/github/milestones")
        )

    async def get_week_over_week(self, project_id: str) -> WeekOverWeekResult:
        """Week-over-week velocity comparison — PRs merged, issues closed, and commits
        in the current 7-day window vs the previous 7-day window (async)."""
        validate_id(project_id, "project")
        return WeekOverWeekResult.model_validate(
            await self._request("GET", f"/projects/{project_id}/github/week-over-week")
        )

    async def get_issue_triage(self, project_id: str, days: int = 7) -> IssueTriageResult:
        """Issue triage — recently-opened issues missing labels, assignee, or milestone (async).

        Args:
            days: Lookback window in days (default 7; options: 7, 14, 30)
        """
        validate_id(project_id, "project")
        return IssueTriageResult.model_validate(
            await self._request("GET", f"/projects/{project_id}/github/issue-triage?days={days}")
        )

    async def get_issue_flow(self, project_id: str, days: int = 30) -> IssueFlowResult:
        """Daily issue open/close flow — backlog burn-down visibility (async).

        Args:
            days: Lookback window in days (default 30; range: 7-90)
        """
        validate_id(project_id, "project")
        return IssueFlowResult.model_validate(
            await self._request("GET", f"/projects/{project_id}/github/issue-flow?days={days}")
        )

    async def get_issue_cycle_time(self, project_id: str, days: int = 90) -> IssueCycleTimeResult:
        """Get issue cycle time by label (avg/median days open to close)."""
        return await self._client.get(
            f"/v1/projects/{project_id}/github/issue-cycle-time",
            params={"days": days},
            response_model=IssueCycleTimeResult,
        )

    async def get_issue_throughput(self, project_id: str, weeks: int = 8) -> IssueThroughputResult:
        """Get weekly closed issue throughput trend (delivery tracker)."""
        return await self._client.get(
            f"/v1/projects/{project_id}/github/issue-throughput",
            params={"weeks": weeks},
            response_model=IssueThroughputResult,
        )

    async def get_issue_resolvers(self, project_id: str, days: int = 30) -> IssueResolversResult:
        """Get issue resolver leaderboard — top contributors by closed issue count."""
        return await self._client.get(
            f"/v1/projects/{project_id}/github/issue-resolvers",
            params={"days": days},
            response_model=IssueResolversResult,
        )

    async def get_cycle_time_trend(self, project_id: str, weeks: int = 8) -> CycleTimeTrendResult:
        """Get weekly average issue cycle time trend — are we getting faster or slower?"""
        return await self._client.get(
            f"/v1/projects/{project_id}/github/cycle-time-trend",
            params={"weeks": weeks},
            response_model=CycleTimeTrendResult,
        )

    async def get_pr_merge_time(self, project_id: str, days: int = 90) -> PrMergeTimeResult:
        """Get PR open→merge time distribution: p25/p50/p75/p95, buckets, per-author avg."""
        return await self._client.get(
            f"/v1/projects/{project_id}/github/pr-merge-time",
            params={"days": days},
            response_model=PrMergeTimeResult,
        )

    async def get_contributor_momentum(
        self, project_id: str, days: int = 28
    ) -> ContributorMomentumResult:
        """Get contributor commit momentum: accelerating/stable/fading vs prior period."""
        return await self._client.get(
            f"/v1/projects/{project_id}/github/contributor-momentum",
            params={"days": days},
            response_model=ContributorMomentumResult,
        )

    async def get_agent_audit_trail(self, project_id: str, days: int = 90) -> AgentAuditResult:
        """Get AI coding assistant attribution audit trail for a project."""
        return await self._client.get(
            f"/v1/projects/{project_id}/github/agent-audit",
            params={"days": days},
            response_model=AgentAuditResult,
        )

    async def get_scope_creep(self, project_id: str, days: int = 90) -> ScopeCreepResult:
        """Get scope creep detection report — PRs that changed >20 or >50 files."""
        return await self._client.get(
            f"/v1/projects/{project_id}/github/scope-creep",
            params={"days": days},
            response_model=ScopeCreepResult,
        )

    async def get_assignee_cycle_time(
        self, project_id: str, days: int = 90
    ) -> AssigneeCycleTimeResult:
        """Get per-assignee issue cycle time with trend vs prior half-period."""
        return await self._client.get(
            f"/v1/projects/{project_id}/github/assignee-cycle-time",
            params={"days": days},
            response_model=AssigneeCycleTimeResult,
        )

    async def get_pr_task_alignment(self, project_id: str, days: int = 90) -> PRTaskAlignmentResult:
        """Detect semantic drift between PRs and their linked issues."""
        return await self._client.get(
            f"/v1/projects/{project_id}/github/pr-task-alignment",
            params={"days": days},
            response_model=PRTaskAlignmentResult,
        )

    async def get_test_gap(self, project_id: str, days: int = 90) -> TestGapResult:
        """Test coverage gap — merged PRs without test changes, by author and week (async)."""
        return await self._client.get(
            f"/v1/projects/{project_id}/github/test-gap",
            params={"days": days},
            response_model=TestGapResult,
        )

    async def get_dora_metrics(self, project_id: str, days: int = 90) -> DORAResult:
        """DORA engineering excellence metrics — deploy frequency, lead time, CFR, MTTR (async)."""
        return await self._client.get(
            f"/v1/projects/{project_id}/github/dora-metrics",
            params={"days": days},
            response_model=DORAResult,
        )

    async def get_ai_vs_human_quality(self, project_id: str, days: int = 90) -> AIvsHumanResult:
        """Compare PR quality scores between AI-authored and human-authored PRs (async)."""
        return await self._client.get(
            f"/v1/projects/{project_id}/github/ai-vs-human-quality",
            params={"days": days},
            response_model=AIvsHumanResult,
        )

    async def get_bus_factor(self, project_id: str, days: int = 90) -> BusFactorResult:
        """Identify knowledge concentration risk — repos and files dominated by a single contributor (async)."""
        return await self._client.get(
            f"/v1/projects/{project_id}/github/bus-factor",
            params={"days": days},
            response_model=BusFactorResult,
        )
