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
    ReviewNetworkResult,
    ReviewDepthResult,
    PRCodeReviewResult,
    SubmitPRReviewResult,
    QualityGateResult,
    ActionPlanResult,
    TechDebtResult,
    CustomRule,
    CustomRulesResponse,
    CustomRuleTestResult,
    BatchScanFileInput,
    BatchScanCodeResult,
    AnalyzeCodeComplexityResult,
    CqlQuery,
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

    async def query_code(self, project_id: str, query: "Dict[str, Any] | CqlQuery") -> Dict[str, Any]:
        """Execute a CQL query over code metrics (async).

        Accepts either a raw dict or a typed CqlQuery instance.
        Supports 12 from: modes: files, functions, suggestions, ast_pattern,
        hotspots, patterns, dead_code, clones, metrics, coverage, summary, history.
        """
        validate_id(project_id, "project")
        body = query.to_dict() if isinstance(query, CqlQuery) else query
        return await self._request("POST", f"/projects/{project_id}/github/query", json=body)

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

    async def batch_scan_code(
        self, project_id: str, *, files: List[BatchScanFileInput]
    ) -> BatchScanCodeResult:
        """Batch SAST + secret scan up to 20 files — pre-flight check before creating a PR (async)."""
        validate_id(project_id, "project")
        response = await self._request(
            "POST",
            f"/projects/{project_id}/github/batch-scan-code",
            json={"files": [f.model_dump() for f in files]},
        )
        return BatchScanCodeResult.model_validate(response)

    async def analyze_code_complexity(
        self,
        project_id: str,
        *,
        file_path: str,
        content: str,
        language: Optional[str] = None,
    ) -> AnalyzeCodeComplexityResult:
        """Compute per-function cyclomatic + cognitive complexity and code smells (async)."""
        validate_id(project_id, "project")
        body: Dict[str, Any] = {"file_path": file_path, "content": content}
        if language:
            body["language"] = language
        response = await self._request(
            "POST",
            f"/projects/{project_id}/github/analyze-complexity",
            json=body,
        )
        return AnalyzeCodeComplexityResult.model_validate(response)

    async def pre_flight_pr(
        self,
        project_id: str,
        *,
        changes: List[BatchScanFileInput],
    ) -> Dict[str, Any]:
        """Pre-flight quality gate: SAST+secrets+complexity+design before creating a PR (async)."""
        validate_id(project_id, "project")
        return await self._request(
            "POST",
            f"/projects/{project_id}/github/pre-flight-pr",
            json={"changes": [f.model_dump() for f in changes]},
        )

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

    async def get_review_network(self, project_id: str, days: int = 90) -> ReviewNetworkResult:
        """Map team code review collaboration — who reviews whose code, silo detection (async)."""
        return await self._client.get(
            f"/v1/projects/{project_id}/github/review-network",
            params={"days": days},
            response_model=ReviewNetworkResult,
        )

    async def get_review_depth(self, project_id: str, days: int = 90) -> ReviewDepthResult:
        """Reviewer thoroughness analytics — scrutiny rate, rubber-stamp vs rigorous (async)."""
        return await self._client.get(
            f"/v1/projects/{project_id}/github/review-depth",
            params={"days": days},
            response_model=ReviewDepthResult,
        )

    async def review_pr_code(
        self,
        project_id: str,
        pr_number: int,
        *,
        repo_full_name: Optional[str] = None,
        format: bool = False,
    ) -> PRCodeReviewResult:
        """AST-level PR code review — quality score (0-100), grade (A-F), smells, security (async)."""
        body: Dict[str, Any] = {"prNumber": pr_number, "format": format}
        if repo_full_name is not None:
            body["repoFullName"] = repo_full_name
        return await self._client.post(
            f"/v1/projects/{project_id}/github/pr-review",
            json=body,
            response_model=PRCodeReviewResult,
        )

    async def submit_pr_review(
        self,
        project_id: str,
        pr_number: int,
        *,
        repo_full_name: Optional[str] = None,
        dry_run: bool = False,
    ) -> SubmitPRReviewResult:
        """Run AST analysis and post the review with inline comments to GitHub (async)."""
        body: Dict[str, Any] = {"prNumber": pr_number, "dryRun": dry_run}
        if repo_full_name is not None:
            body["repoFullName"] = repo_full_name
        return await self._client.post(
            f"/v1/projects/{project_id}/github/pr-submit-review",
            json=body,
            response_model=SubmitPRReviewResult,
        )

    async def check_pr_quality_gate(
        self,
        project_id: str,
        pr_number: int,
        *,
        repo_full_name: Optional[str] = None,
        gate: Optional[Any] = None,
        post_status: bool = False,
    ) -> QualityGateResult:
        """Evaluate a PR against a quality gate — returns PASSED/FAILED with condition detail (async)."""
        body: Dict[str, Any] = {"prNumber": pr_number, "postStatus": post_status}
        if repo_full_name is not None:
            body["repoFullName"] = repo_full_name
        if gate is not None:
            body["gate"] = gate
        return await self._client.post(
            f"/v1/projects/{project_id}/github/pr-quality-gate",
            json=body,
            response_model=QualityGateResult,
        )

    async def get_action_plan(self, project_id: str) -> ActionPlanResult:
        """Ranked code improvement action plan — SAST findings, worst functions, uncovered hotspots."""
        return await self._client.get(
            f"/v1/projects/{project_id}/github/action-plan",
            response_model=ActionPlanResult,
        )

    async def get_tech_debt(self, project_id: str) -> TechDebtResult:
        """SonarQube-style technical debt breakdown by category with remediation estimate and grade."""
        return await self._client.get(
            f"/v1/projects/{project_id}/github/tech-debt",
            response_model=TechDebtResult,
        )

    async def list_custom_rules(self, project_id: str) -> CustomRulesResponse:
        """List all user-defined tree-sitter SAST rules for a project."""
        return await self._client.get(
            f"/v1/projects/{project_id}/github/custom-rules",
            response_model=CustomRulesResponse,
        )

    async def create_custom_rule(self, project_id: str, **kwargs: Any) -> CustomRule:
        """Create a user-defined tree-sitter SAST rule."""
        return await self._client.post(
            f"/v1/projects/{project_id}/github/custom-rules",
            json=kwargs,
            response_model=CustomRule,
        )

    async def update_custom_rule(self, project_id: str, rule_id: str, **kwargs: Any) -> CustomRule:
        """Update fields on an existing custom rule."""
        return await self._client.patch(
            f"/v1/projects/{project_id}/github/custom-rules/{rule_id}",
            json=kwargs,
            response_model=CustomRule,
        )

    async def delete_custom_rule(self, project_id: str, rule_id: str) -> None:
        """Delete a custom rule permanently."""
        await self._client.delete(f"/v1/projects/{project_id}/github/custom-rules/{rule_id}")

    async def test_custom_rule(self, project_id: str, rule_id: str) -> CustomRuleTestResult:
        """Run a custom rule against the top hotspot files and return matches."""
        return await self._client.post(
            f"/v1/projects/{project_id}/github/custom-rules/{rule_id}/test",
            json={},
            response_model=CustomRuleTestResult,
        )

    async def get_quality_profile(self, project_id: str) -> Dict[str, Any]:
        """Fetch the stored quality gate profile (preset + thresholds) for a project."""
        return await self._client.get(f"/v1/projects/{project_id}/github/quality-profile")

    async def set_quality_profile(
        self,
        project_id: str,
        preset_name: str,
        conditions: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Save per-project quality gate thresholds. preset_name: strict/standard/relaxed/custom."""
        body: Dict[str, Any] = {"preset_name": preset_name}
        if conditions is not None:
            body["conditions"] = conditions
        return await self._client.put(
            f"/v1/projects/{project_id}/github/quality-profile", json=body
        )

    async def update_finding_status(
        self,
        project_id: str,
        suggestion_id: str,
        status: str,
        fp_reason: Optional[str] = None,
        lifecycle_note: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Update lifecycle status of a SAST finding (false_positive/confirmed/resolved/open)."""
        body: Dict[str, Any] = {"status": status}
        if fp_reason is not None:
            body["fp_reason"] = fp_reason
        if lifecycle_note is not None:
            body["lifecycle_note"] = lifecycle_note
        return await self._client.patch(
            f"/v1/projects/{project_id}/github/improvements/{suggestion_id}", json=body
        )

    async def suggest_reviewers(
        self,
        project_id: str,
        file_paths: Optional[List[str]] = None,
        days: int = 90,
        limit: int = 5,
    ) -> Dict[str, Any]:
        """Suggest PR reviewers ranked by commit-level file expertise."""
        query: Dict[str, Any] = {"from": "code_ownership", "days": days, "limit": limit}
        if file_paths:
            query["where"] = {"file_paths": file_paths}
        return await self._client.post(f"/v1/projects/{project_id}/github/query", json=query)

    async def get_refactor_candidates(
        self,
        project_id: str,
        language: Optional[str] = None,
        limit: int = 15,
    ) -> Dict[str, Any]:
        """Return files ranked by refactor ROI: CC×2 + CogC×1.5 + smells×10 + issues×5 + hotspot×0.5."""
        query: Dict[str, Any] = {"from": "refactor_candidates", "limit": limit}
        if language:
            query["language"] = language
        return await self._client.post(f"/v1/projects/{project_id}/github/query", json=query)

    async def deep_pr_review(
        self,
        project_id: str,
        pr_number: int,
        repo_full_name: Optional[str] = None,
        limit_files: int = 30,
        include_inline_smells: bool = True,
    ) -> Dict[str, Any]:
        """One-call CQL PR review using stored metrics (pr_impact + smells + MI)."""
        body: Dict[str, Any] = {"prNumber": pr_number, "limitFiles": limit_files, "includeInlineSmells": include_inline_smells}
        if repo_full_name:
            body["repoFullName"] = repo_full_name
        return await self._client.post(f"/v1/projects/{project_id}/github/deep-pr-review", json=body)

    async def orchestrate_pr_review(
        self,
        project_id: str,
        pr_number: int,
        repo_full_name: Optional[str] = None,
        limit_files: int = 30,
        include_inline_smells: bool = True,
    ) -> Dict[str, Any]:
        """Most comprehensive one-call PR review — 4 CQL signals in parallel."""
        body: Dict[str, Any] = {"prNumber": pr_number, "limitFiles": limit_files, "includeInlineSmells": include_inline_smells}
        if repo_full_name:
            body["repoFullName"] = repo_full_name
        return await self._client.post(f"/v1/projects/{project_id}/github/orchestrate-pr-review", json=body)

    async def generate_pr_description(
        self,
        project_id: str,
        file_paths: Optional[List[str]] = None,
        pr_number: Optional[int] = None,
        repo_full_name: Optional[str] = None,
        commit_messages: Optional[List[str]] = None,
        pr_title: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Generate a professional PR description using LLM + CQL code metrics."""
        if not file_paths and not pr_number:
            raise ValueError("Either file_paths or pr_number is required")
        body: Dict[str, Any] = {}
        if file_paths:
            body["filePaths"] = file_paths
        if pr_number:
            body["prNumber"] = pr_number
        if repo_full_name:
            body["repoFullName"] = repo_full_name
        if commit_messages:
            body["commitMessages"] = commit_messages
        if pr_title:
            body["prTitle"] = pr_title
        return await self._client.post(f"/v1/projects/{project_id}/github/generate-pr-description", json=body)

    async def generate_ci_workflow(
        self,
        project_id: str,
        workflow_type: str = "full",
        gate: str = "standard",
        main_branch: str = "main",
        post_inline_comments: bool = True,
        block_on_fail: bool = True,
    ) -> Dict[str, Any]:
        """Generate GitHub Actions CI workflow YAML files for Trix quality gates."""
        return await self._client.post(
            f"/v1/projects/{project_id}/github/generate-ci-workflow",
            json={"type": workflow_type, "gate": gate, "mainBranch": main_branch, "postInlineComments": post_inline_comments, "blockOnFail": block_on_fail},
        )

    async def get_test_coverage_gap(
        self,
        project_id: str,
        mode: str = "files",
        min_cc: int = 1,
        language: Optional[str] = None,
        file_contains: Optional[str] = None,
        limit: int = 25,
    ) -> Dict[str, Any]:
        """Risk-weighted test coverage gap — gap_risk = (1-covered) × CC × (1 + hotspot/10)."""
        query: Dict[str, Any] = {"from": "test_coverage_gap", "mode": mode, "min_cc": min_cc, "limit": limit}
        if language:
            query["language"] = language
        if file_contains:
            query["file_contains"] = file_contains
        return await self._client.post(f"/v1/projects/{project_id}/github/query", json=query)

    async def get_change_risk(
        self,
        project_id: str,
        file_paths: List[str],
        include_actions: bool = True,
    ) -> Dict[str, Any]:
        """Pre-change blast radius risk assessment — CC + MI + hotspot + debt + coverage gap."""
        return await self._client.post(
            f"/v1/projects/{project_id}/github/query",
            json={"from": "change_risk", "file_paths": file_paths, "include_actions": include_actions},
        )

    async def get_module_complexity(
        self,
        project_id: str,
        mode: str = "summary",
        depth: int = 1,
        module: Optional[str] = None,
        sort_by: str = "module_score",
        language: Optional[str] = None,
        limit: int = 20,
    ) -> Dict[str, Any]:
        """Directory-level complexity aggregation — SonarQube-style module quality view."""
        query: Dict[str, Any] = {"from": "module_complexity", "mode": mode, "depth": depth, "sort_by": sort_by, "limit": limit}
        if module:
            query["module"] = module
        if language:
            query["language"] = language
        return await self._client.post(f"/v1/projects/{project_id}/github/query", json=query)

    async def get_toxic_files(
        self,
        project_id: str,
        mode: str = "files",
        min_score: int = 3,
        language: Optional[str] = None,
        limit: int = 25,
        cc_threshold: Optional[int] = None,
        mi_threshold: Optional[int] = None,
        hotspot_threshold: Optional[float] = None,
        debt_threshold: Optional[int] = None,
        loc_threshold: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Multi-dimensional hall of shame — files failing multiple quality dimensions.

        Each dimension scores 1 point: high_cc, low_mi, high_hotspot, high_debt, no_test, large_file.
        mode: 'files' (ranked) | 'summary' (buckets + top dims + worst_5)
        min_score: 1-6, default 3
        """
        query: Dict[str, Any] = {"from": "toxic_files", "mode": mode, "min_score": min_score, "limit": limit}
        if language:
            query["language"] = language
        if cc_threshold is not None:
            query["cc_threshold"] = cc_threshold
        if mi_threshold is not None:
            query["mi_threshold"] = mi_threshold
        if hotspot_threshold is not None:
            query["hotspot_threshold"] = hotspot_threshold
        if debt_threshold is not None:
            query["debt_threshold"] = debt_threshold
        if loc_threshold is not None:
            query["loc_threshold"] = loc_threshold
        return await self._client.post(f"/v1/projects/{project_id}/github/query", json=query)

    async def evaluate_quality_gate(
        self,
        project_id: str,
        preset: str = "standard",
        conditions: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """SonarQube-style quality gate — PASSED / FAILED verdict with per-condition breakdown.

        preset: 'strict' | 'standard' (default) | 'relaxed'
        conditions: override specific thresholds e.g. {'avg_cc_lte': 12}
        Returns gate_status, conditions_evaluated[], blocking_conditions[].
        """
        query: Dict[str, Any] = {"from": "quality_gate", "preset": preset}
        if conditions:
            query["conditions"] = conditions
        return await self._client.post(f"/v1/projects/{project_id}/github/query", json=query)

    async def get_complexity_trend(
        self,
        project_id: str,
        mode: str = "summary",
        min_delta: int = 0,
        limit: int = 20,
    ) -> Dict[str, Any]:
        """Per-file complexity regression detection across two scan snapshots.

        mode: 'regressing' | 'recovering' | 'all' | 'summary' (default)
        Returns regressing_count, recovering_count, worst_5, best_5.
        """
        return await self._client.post(
            f"/v1/projects/{project_id}/github/query",
            json={"from": "complexity_trend", "mode": mode, "min_delta": min_delta, "limit": limit},
        )

    async def get_contributor_risk(
        self,
        project_id: str,
        mode: str = "summary",
        min_risk: str = "",
        depth: int = 2,
        limit: int = 20,
    ) -> Dict[str, Any]:
        """Bus factor and knowledge concentration risk per module.

        departure_risk: HIGH (bus_factor=1), MEDIUM (=2), LOW (>=3).
        mode: 'modules' | 'files' | 'summary' (default)
        """
        query: Dict[str, Any] = {
            "from": "contributor_risk",
            "mode": mode,
            "depth": depth,
            "limit": limit,
        }
        if min_risk:
            query["min_risk"] = min_risk
        return await self._client.post(f"/v1/projects/{project_id}/github/query", json=query)

    async def get_smell_density(
        self,
        project_id: str,
        mode: str = "summary",
        min_grade: str = "",
        depth: int = 2,
        limit: int = 20,
    ) -> Dict[str, Any]:
        """Normalized smell density — smells per KLOC and per function.

        Grades: CRITICAL (>=50/kloc or >=2.0/fn), HIGH (>=20), MEDIUM (>=10), LOW.
        mode: 'files' | 'modules' | 'summary' (default)
        """
        query: Dict[str, Any] = {
            "from": "smell_density",
            "mode": mode,
            "depth": depth,
            "limit": limit,
        }
        if min_grade:
            query["min_grade"] = min_grade
        return await self._client.post(
            f"/v1/projects/{project_id}/github/query-code", json=query
        )

    async def pre_pr_checklist(
        self,
        project_id: str,
        file_paths: List[str],
        gate_preset: str = "standard",
        include_smells: bool = True,
    ) -> Dict[str, Any]:
        """One-call pre-PR health check — GO / CAUTION / HOLD verdict.

        Runs 5 checks in parallel: change_risk, quality_gate, test_coverage_gap,
        toxic_files, function_smells.
        Returns verdict + blocking_checks[] + recommended_actions[].
        """
        return await self._client.post(
            f"/v1/projects/{project_id}/github/query-code",
            json={
                "from": "pre_pr_checklist",
                "file_paths": file_paths,
                "gate_preset": gate_preset,
                "include_smells": include_smells,
            },
        )

    async def get_project_health_score(
        self,
        project_id: str,
        mode: str = "summary",
    ) -> Dict[str, Any]:
        """Composite project health score (0–100) with A–F grade.

        mode: 'summary' | 'breakdown' (per-signal scores with weights)
        """
        return await self._client.post(
            f"/v1/projects/{project_id}/github/query-code",
            json={"from": "project_health_score", "mode": mode},
        )

    async def get_test_smell(
        self,
        project_id: str,
        mode: str = "files",
        kind: str = "",
        language: str = "",
        limit: int = 25,
    ) -> Dict[str, Any]:
        """Detect antipatterns in test code (test smells).

        Detects: GOD_TEST_CLASS, COMPLEX_TEST_LOGIC, LARGE_TEST, ASSERTION_ROULETTE.
        mode: 'files' | 'summary'
        """
        query: Dict[str, Any] = {"from": "test_smell", "mode": mode, "limit": limit}
        if kind:
            query["kind"] = kind
        if language:
            query["language"] = language
        return await self._client.post(f"/v1/projects/{project_id}/github/query", json=query)

    async def get_smell_trend(
        self,
        project_id: str,
        mode: str = "regressing",
        min_delta: int = 0,
        language: str = "",
        limit: int = 25,
    ) -> Dict[str, Any]:
        """Per-file smell count delta across two scan snapshots.

        trend_score = smell_delta × 3 + suggestion_delta.
        mode: 'regressing' | 'improving' | 'all' | 'summary'
        """
        query: Dict[str, Any] = {"from": "smell_trend", "mode": mode, "min_delta": min_delta, "limit": limit}
        if language:
            query["language"] = language
        return await self._client.post(f"/v1/projects/{project_id}/github/query", json=query)

    async def get_top_rules(
        self,
        project_id: str,
        mode: str = "rules",
        category: str = "",
        severity: str = "",
        limit: int = 25,
    ) -> Dict[str, Any]:
        """SAST rule/kind breakdown ranked by occurrence.

        mode: 'rules' | 'files'. category/severity for filtering.
        """
        query: Dict[str, Any] = {"from": "top_rules", "mode": mode, "limit": limit}
        if category:
            query["category"] = category
        if severity:
            query["severity"] = severity
        return await self._client.post(f"/v1/projects/{project_id}/github/query", json=query)

    async def get_module_smell_heat(
        self,
        project_id: str,
        mode: str = "modules",
        depth: int = 2,
        language: str = "",
        limit: int = 25,
    ) -> Dict[str, Any]:
        """Directory-level smell heat map.

        smell_score = severity-weighted smells per file (critical×4, high×3, medium×2, low×1).
        mode: 'modules' | 'summary'. depth: 1-5 directory grouping depth.
        """
        query: Dict[str, Any] = {"from": "module_smell_heat", "mode": mode, "depth": depth, "limit": limit}
        if language:
            query["language"] = language
        return await self._client.post(f"/v1/projects/{project_id}/github/query", json=query)

    async def get_refactor_priority(
        self,
        project_id: str,
        mode: str = "files",
        language: str = "",
        min_score: float = 0,
        limit: int = 25,
    ) -> Dict[str, Any]:
        """Composite refactoring urgency ranking (0-100).

        Signals: smell_density(30%) + coupling fan-in(25%) + hotspot(20%) + CC(15%) + no_test(10%).
        mode: 'files' | 'summary'
        """
        query: Dict[str, Any] = {"from": "refactor_priority", "mode": mode, "min_score": min_score, "limit": limit}
        if language:
            query["language"] = language
        return await self._client.post(f"/v1/projects/{project_id}/github/query", json=query)

    async def get_hotspot_matrix(
        self,
        project_id: str,
        mode: str = "files",
        quadrant: str = "",
        language: str = "",
        limit: int = 25,
    ) -> Dict[str, Any]:
        """2D risk matrix: churn frequency × cyclomatic complexity.

        Quadrants: DANGER_ZONE, WORKHORSE, SLEEPING_GIANT, SAFE.
        mode: 'files' | 'summary'
        """
        query: Dict[str, Any] = {"from": "hotspot_matrix", "mode": mode, "limit": limit}
        if quadrant:
            query["quadrant"] = quadrant
        if language:
            query["language"] = language
        return await self._client.post(f"/v1/projects/{project_id}/github/query", json=query)

    async def get_coupling_analysis(
        self,
        project_id: str,
        mode: str = "bottlenecks",
        language: str = "",
        limit: int = 25,
    ) -> Dict[str, Any]:
        """File-level coupling analysis — fan-in bottlenecks.

        Fan-in = sum of callerCounts across all functions in the file.
        Tiers: CRITICAL (≥30), HIGH (≥15), MODERATE (≥5), LOW (<5).
        mode: 'bottlenecks' | 'all' | 'summary'
        """
        query: Dict[str, Any] = {"from": "coupling_analysis", "mode": mode, "limit": limit}
        if language:
            query["language"] = language
        return await self._client.post(f"/v1/projects/{project_id}/github/query", json=query)

    async def batch_mark_findings(
        self,
        project_id: str,
        findings: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """Mark multiple SAST findings concurrently.

        Each finding: {suggestion_id, status, fp_reason?, lifecycle_note?}
        Returns: {succeeded, failed, total}
        """
        import asyncio
        results = {"succeeded": 0, "failed": 0, "total": len(findings)}
        tasks = [
            self.update_finding_status(
                project_id,
                f["suggestion_id"],
                f["status"],
                f.get("fp_reason"),
                f.get("lifecycle_note"),
            )
            for f in findings
        ]
        settled = await asyncio.gather(*tasks, return_exceptions=True)
        for r in settled:
            if isinstance(r, Exception):
                results["failed"] += 1
            else:
                results["succeeded"] += 1
        return results

    async def get_naming_violations(
        self,
        project_id: str,
        rule: str = "all",
        language: str = "",
        repo_full_name: str = "",
        limit: int = 25,
    ) -> Dict[str, Any]:
        """Naming convention violations (async) — nondescript, numbered, generic, inconsistent.

        rule: all | nondescript | numbered | generic | inconsistent
        Returns files ranked by violation_score with violations[] per file.
        """
        query: Dict[str, Any] = {
            "from": "naming_violations",
            "rule": rule,
            "limit": limit,
        }
        if language:
            query["language"] = language
        if repo_full_name:
            query["repoFullName"] = repo_full_name
        return await self._client.post(f"/v1/projects/{project_id}/github/query", json=query)

    async def get_solid_analysis(
        self,
        project_id: str,
        principle: str = "all",
        min_severity: str = "warning",
        repo_full_name: str = "",
        limit: int = 25,
    ) -> Dict[str, Any]:
        """SOLID principle violations + OOP anti-patterns (async).

        principle: all | srp | ocp | isp | dip | lsp
        min_severity: info | warning | critical
        Returns violations[] with principle, kind, severity, file_path, message, refactoring.
        """
        query: Dict[str, Any] = {
            "from": "solid_analysis",
            "principle": principle,
            "minSeverity": min_severity,
            "limit": limit,
        }
        if repo_full_name:
            query["repoFullName"] = repo_full_name
        return await self._client.post(f"/v1/projects/{project_id}/github/query", json=query)

    async def get_clean_code(
        self,
        project_id: str,
        mode: str = "summary",
        min_score: int = 90,
        rule: str = "",
        language: str = "",
        limit: int = 20,
    ) -> Any:
        """Measure Clean Code adherence (function length, param count, naming quality, SRP)."""
        query: Dict[str, Any] = {
            "from": "clean_code",
            "mode": mode,
            "min_score": min_score,
            "limit": limit,
        }
        if rule and rule != "all":
            query["rule"] = rule
        if language:
            query["language"] = language
        return await self._client.post(f"/v1/projects/{project_id}/github/query", json=query)

    async def get_design_patterns(
        self,
        project_id: str,
        kind: str = "all",
        pattern: str = "",
        confidence: str = "",
        limit: int = 30,
    ) -> Any:
        """Detect design patterns and anti-patterns from stored code metrics.

        kind: 'all' | 'pattern' | 'anti_pattern'
        pattern: factory|observer|singleton|god_object|spaghetti_code|magic_numbers|golden_hammer|lava_flow
        confidence: 'high' | 'medium' | 'low' (minimum)
        """
        query: Dict[str, Any] = {"from": "design_patterns", "kind": kind, "limit": limit}
        if pattern:
            query["pattern"] = pattern
        if confidence:
            query["confidence"] = confidence
        return await self._client.post(f"/v1/projects/{project_id}/github/query", json=query)

    async def get_function_profile(
        self,
        project_id: str,
        mode: str = "all",
        min_risk: int = 0,
        language: str = "",
        file_path_contains: str = "",
        limit: int = 50,
    ) -> Any:
        """Deep per-function quality profile combining CC, cognitive, LOC, params, callers, clones, and naming.

        mode: 'all' (global ranking) | 'summary' (distribution + worst_10) | 'files' (worst fn per file)
        min_risk: only return functions with risk_score >= this (0-100)
        """
        query: Dict[str, Any] = {"from": "function_profile", "mode": mode, "limit": limit}
        if min_risk > 0:
            query["min_risk"] = min_risk
        if language:
            query["language"] = language
        if file_path_contains:
            query["file_path_contains"] = file_path_contains
        return await self._client.post(f"/v1/projects/{project_id}/github/query", json=query)

    async def get_testability(
        self,
        project_id: str,
        mode: str = "files",
        language: str = "",
        file_path_contains: str = "",
        limit: int = 30,
    ) -> Any:
        """Score how easy each file is to test (0-100, 100 = very easy to test).

        mode: 'files' (worst-first) | 'summary' (grade dist + worst_5) | 'critical' (score < 40 only)
        Returns: { results[], count } — each result has testability_score, grade, barriers[]
        """
        query: Dict[str, Any] = {"from": "testability", "mode": mode, "limit": limit}
        if language:
            query["language"] = language
        if file_path_contains:
            query["file_path_contains"] = file_path_contains
        return await self._client.post(f"/v1/projects/{project_id}/github/query", json=query)

    async def get_api_surface(
        self,
        project_id: str,
        mode: str = "all",
        min_callers: int = 3,
        language: str = "",
        file_path_contains: str = "",
        limit: int = 50,
    ) -> Any:
        """Analyze public API surface — functions with many callers — and rate their design quality.

        mode: 'all' (by callerCount) | 'summary' (risk dist + worst_5) | 'risky' (high breaking_change_risk)
        Returns: { results[], count } — each result has design_score, breaking_change_risk, issues[]
        """
        query: Dict[str, Any] = {
            "from": "api_surface", "mode": mode, "min_callers": min_callers, "limit": limit
        }
        if language:
            query["language"] = language
        if file_path_contains:
            query["file_path_contains"] = file_path_contains
        return await self._client.post(f"/v1/projects/{project_id}/github/query", json=query)

    async def get_module_cohesion(
        self,
        project_id: str,
        mode: str = "files",
        language: str = "",
        limit: int = 30,
    ) -> Any:
        """Analyze module cohesion — identify files violating Single Responsibility Principle.

        mode: 'files' (sorted by cohesion score) | 'candidates' (split-recommended) | 'summary'
        Returns: { results[], count } — each result has cohesion_score, concern_groups, recommendation
        """
        query: Dict[str, Any] = {"from": "module_cohesion", "mode": mode, "limit": limit}
        if language:
            query["language"] = language
        return await self._client.post(f"/v1/projects/{project_id}/github/query", json=query)

    async def get_function_risk_delta(
        self,
        project_id: str,
        file_paths: Optional[List[str]] = None,
        dir: str = "",
        mode: str = "top",
        limit: int = 15,
    ) -> Any:
        """Score functions in PR-changed files by review attention priority.

        file_paths: list of changed file paths from a PR diff
        dir: directory prefix as alternative to file_paths
        mode: 'top' (highest priority) | 'all' (all scored) | 'summary' (per-file)
        Returns: functions ranked by review_attention_score with risk_factors and review_note
        """
        query: Dict[str, Any] = {
            "from": "function_risk_delta",
            "where": {"file_paths": file_paths or []},
            "mode": mode,
            "limit": limit,
        }
        if dir:
            query["where"]["dir"] = dir
        return await self._client.post(f"/v1/projects/{project_id}/github/query", json=query)

    async def get_function_outliers(
        self,
        project_id: str,
        mode: str = "files",
        threshold: float = 2.0,
        language: str = "",
        limit: int = 30,
    ) -> Any:
        """Find statistical complexity outliers within each file using Z-score analysis.

        mode: 'files' (all outliers) | 'by_file' (worst per file) | 'summary'
        threshold: Z-score cutoff (default 2.0; lower = more outliers)
        Returns: functions with outlier_dimensions[], z_scores, severity (triple/double/single)
        """
        query: Dict[str, Any] = {
            "from": "function_outliers", "mode": mode, "threshold": threshold, "limit": limit
        }
        if language:
            query["language"] = language
        return await self._client.post(f"/v1/projects/{project_id}/github/query", json=query)

    async def find_dead_code(
        self,
        project_id: str,
        mode: str = "functions",
        language: str = "",
        risk: str = "",
        limit: int = 50,
    ) -> Any:
        """Find unused public functions with callerCount=0 across all languages.

        mode: 'functions' (list) | 'files' (ranked by dead count) | 'summary'
        risk: filter by tier — 'high' (CC>5 or LOC>40), 'medium', 'low'
        Returns: function_name, file_path, risk, suggested_action
        """
        query: Dict[str, Any] = {
            "from": "dead_exports", "mode": mode, "limit": limit
        }
        if language:
            query["language"] = language
        if risk:
            query["risk"] = risk
        return await self._client.post(f"/v1/projects/{project_id}/github/query", json=query)

    async def analyze_contributor_quality(
        self,
        project_id: str,
        mode: str = "contributors",
        author: str = "",
        min_files: int = 2,
        limit: int = 30,
    ) -> Any:
        """Code quality metrics aggregated by primary contributor.

        mode: 'contributors' (ranked list) | 'summary' | 'files' (with author param)
        Returns: avg_cc, avg_mi, avg_hotspot, high_cc_count, low_mi_count, debt_score
        """
        query: Dict[str, Any] = {
            "from": "contributor_quality", "mode": mode, "min_files": min_files, "limit": limit
        }
        if author:
            query["author"] = author
        return await self._client.post(f"/v1/projects/{project_id}/github/query", json=query)
