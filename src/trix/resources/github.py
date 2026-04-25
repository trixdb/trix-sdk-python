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
        data = {
            "connection_id": connection_id,
            "repo_id": repo_id,
            "repo_full_name": repo_full_name,
        }
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
        agent: Optional[str] = None,
    ) -> PRBriefsResponse:
        """Get PR briefs with quality scores and risk signals.

        Args:
            project_id: Project UUID.
            state: Filter by PR state — 'open', 'closed', or 'all'.
            pr_number: Fetch brief for a specific PR number.
            limit: Max results to return (1–50).
            min_quality_score: Exclude PRs below this quality threshold (0–100).
            max_quality_score: Exclude PRs above this quality threshold — use to surface risky PRs.
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
        response = self._request("GET", f"/projects/{project_id}/github/pr-briefs", params=params)
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

    def get_goal_progress_history(
        self, project_id: str, limit: int = 20
    ) -> GoalProgressHistoryResponse:
        """Get chronological feed of GitHub-driven goal progress events."""
        validate_id(project_id, "project")
        response = self._request(
            "GET", f"/projects/{project_id}/github/goal-progress-history?limit={limit}"
        )
        return GoalProgressHistoryResponse.model_validate(response)

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
        response = self._request(
            "PATCH", f"/projects/{project_id}/github/{connection_id}", json=data
        )
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

    def create_issue_from_suggestion(self, project_id: str, suggestion_id: str) -> Dict[str, Any]:
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
        return [
            WeeklyActivityDay.model_validate(d)
            for d in (response if isinstance(response, list) else [])
        ]

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

    def query_code(self, project_id: str, query: "Dict[str, Any] | CqlQuery") -> Dict[str, Any]:
        """Execute a CQL query over code metrics.

        Accepts either a raw dict or a typed CqlQuery instance.
        Supports 12 from: modes: files, functions, suggestions, ast_pattern,
        hotspots, patterns, dead_code, clones, metrics, coverage, summary, history.
        """
        validate_id(project_id, "project")
        body = query.to_dict() if isinstance(query, CqlQuery) else query
        return self._request("POST", f"/projects/{project_id}/github/query", json=body)

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
            json={
                "connection_id": connection_id,
                "pr_number": pr_number,
                "event": event,
                "dry_run": dry_run,
            },
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

    def scan_code(self, project_id: str, *, file_path: str, content: str) -> ScanCodeResult:
        """Scan arbitrary file content with all SAST + secret scanners (no GitHub auth needed)."""
        validate_id(project_id, "project")
        response = self._request(
            "POST",
            f"/projects/{project_id}/github/scan-code",
            json={"file_path": file_path, "content": content},
        )
        return ScanCodeResult.model_validate(response)

    def batch_scan_code(
        self, project_id: str, *, files: List[BatchScanFileInput]
    ) -> BatchScanCodeResult:
        """Batch SAST + secret scan up to 20 files — ideal pre-flight check before creating a PR."""
        validate_id(project_id, "project")
        response = self._request(
            "POST",
            f"/projects/{project_id}/github/batch-scan-code",
            json={"files": [f.model_dump() for f in files]},
        )
        return BatchScanCodeResult.model_validate(response)

    def analyze_code_complexity(
        self,
        project_id: str,
        *,
        file_path: str,
        content: str,
        language: Optional[str] = None,
    ) -> AnalyzeCodeComplexityResult:
        """Compute per-function cyclomatic + cognitive complexity and code smells."""
        validate_id(project_id, "project")
        body: Dict[str, Any] = {"file_path": file_path, "content": content}
        if language:
            body["language"] = language
        response = self._request(
            "POST",
            f"/projects/{project_id}/github/analyze-complexity",
            json=body,
        )
        return AnalyzeCodeComplexityResult.model_validate(response)

    def pre_flight_pr(
        self,
        project_id: str,
        *,
        changes: List[BatchScanFileInput],
    ) -> Dict[str, Any]:
        """Pre-flight quality gate: SAST+secrets+complexity+design check before creating a PR.

        Returns a PASS/WARN/BLOCK verdict with structured blockers and warnings.
        Call this before create_pr to catch issues early.
        """
        validate_id(project_id, "project")
        response = self._request(
            "POST",
            f"/projects/{project_id}/github/pre-flight-pr",
            json={"changes": [f.model_dump() for f in changes]},
        )
        return response

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
            self._request(
                "GET", f"/projects/{project_id}/github/load-bearing?min_callers={min_callers}"
            )
        )

    def get_bug_density(self, project_id: str) -> BugDensityResult:
        """Per-file issue density — open suggestions per 1,000 LOC, ranked by density."""
        validate_id(project_id, "project")
        return BugDensityResult.model_validate(
            self._request("GET", f"/projects/{project_id}/github/bug-density")
        )

    def get_pr_quality_trend(self, project_id: str) -> List[PRQualityWeek]:
        """Weekly PR quality score trend (12-week rolling window).

        Returns one data point per week that had at least one reviewed PR.
        Use this to track whether code quality is improving or declining over time.
        """
        validate_id(project_id, "project")
        data = self._request("GET", f"/projects/{project_id}/github/pr-quality-trend")
        return [PRQualityWeek.model_validate(w) for w in data]

    def get_active_branches(self, project_id: str) -> ActiveBranchesResult:
        """Active branches derived from commit memories with staleness detection (>14 days)."""
        validate_id(project_id, "project")
        return ActiveBranchesResult.model_validate(
            self._request("GET", f"/projects/{project_id}/github/branches")
        )

    def get_contributor_quality(self, project_id: str) -> ContributorQualityResult:
        """Per-contributor PR quality stats — avg score, test coverage %, PR count."""
        validate_id(project_id, "project")
        return ContributorQualityResult.model_validate(
            self._request("GET", f"/projects/{project_id}/github/contributor-quality")
        )

    def get_pr_aging(self, project_id: str) -> PrAgingResult:
        """Open PRs sorted oldest-first with ageDays + isStale flag (>7 days without update)."""
        validate_id(project_id, "project")
        return PrAgingResult.model_validate(
            self._request("GET", f"/projects/{project_id}/github/pr-aging")
        )

    def get_pr_size_distribution(self, project_id: str) -> PrSizeDistributionResult:
        """PR size distribution (Small/Medium/Large/Extra-large) with quality + test coverage."""
        validate_id(project_id, "project")
        return PrSizeDistributionResult.model_validate(
            self._request("GET", f"/projects/{project_id}/github/pr-size-distribution")
        )

    def get_review_turnaround(self, project_id: str) -> ReviewTurnaroundResult:
        """Review turnaround time — avg hours from PR open to first review."""
        validate_id(project_id, "project")
        return ReviewTurnaroundResult.model_validate(
            self._request("GET", f"/projects/{project_id}/github/review-turnaround")
        )

    def get_work_queue(self, project_id: str) -> WorkQueueResult:
        """Prioritized work queue — synthesizes all GitHub signals into action items."""
        validate_id(project_id, "project")
        return WorkQueueResult.model_validate(
            self._request("GET", f"/projects/{project_id}/github/work-queue")
        )

    def get_reviewer_workload(self, project_id: str) -> ReviewerWorkloadResult:
        """Reviewer workload — pending review queue and historical speed per reviewer."""
        validate_id(project_id, "project")
        return ReviewerWorkloadResult.model_validate(
            self._request("GET", f"/projects/{project_id}/github/reviewer-workload")
        )

    def get_approved_prs(self, project_id: str) -> ApprovedPRsResult:
        """Approved-but-not-merged PRs — open PRs with ≥1 approval, ready to ship."""
        validate_id(project_id, "project")
        return ApprovedPRsResult.model_validate(
            self._request("GET", f"/projects/{project_id}/github/approved-prs")
        )

    def get_issue_backlog(self, project_id: str) -> IssueBacklogResult:
        """Issue backlog health — unassigned/unlabeled counts, label distribution, oldest issues."""
        validate_id(project_id, "project")
        return IssueBacklogResult.model_validate(
            self._request("GET", f"/projects/{project_id}/github/issue-backlog")
        )

    def get_review_coverage(self, project_id: str) -> ReviewCoverageResult:
        """PR review coverage — % of merged PRs (last 90d) that received at least one review."""
        validate_id(project_id, "project")
        return ReviewCoverageResult.model_validate(
            self._request("GET", f"/projects/{project_id}/github/review-coverage")
        )

    def get_label_velocity(self, project_id: str, days: int = 30) -> LabelVelocityResult:
        """Issue label velocity — opened vs closed per label, worst-accumulating first."""
        validate_id(project_id, "project")
        return LabelVelocityResult.model_validate(
            self._request("GET", f"/projects/{project_id}/github/label-velocity?days={days}")
        )

    def get_commit_leaders(self, project_id: str, days: int = 30) -> CommitLeadersResult:
        """Commit leaders — top contributors by commit count over the last N days."""
        validate_id(project_id, "project")
        return CommitLeadersResult.model_validate(
            self._request("GET", f"/projects/{project_id}/github/commit-leaders?days={days}")
        )

    def get_issue_assignees(self, project_id: str) -> IssueAssigneesResult:
        """Issue assignee workload — open issue counts per contributor, most overloaded first."""
        validate_id(project_id, "project")
        return IssueAssigneesResult.model_validate(
            self._request("GET", f"/projects/{project_id}/github/issue-assignees")
        )

    def get_milestones(self, project_id: str) -> MilestonesResult:
        """Milestone progress — open/closed issue counts per GitHub milestone, least-complete first."""
        validate_id(project_id, "project")
        return MilestonesResult.model_validate(
            self._request("GET", f"/projects/{project_id}/github/milestones")
        )

    def get_week_over_week(self, project_id: str) -> WeekOverWeekResult:
        """Week-over-week velocity comparison — PRs merged, issues closed, and commits
        in the current 7-day window vs the previous 7-day window."""
        validate_id(project_id, "project")
        return WeekOverWeekResult.model_validate(
            self._request("GET", f"/projects/{project_id}/github/week-over-week")
        )

    def get_issue_triage(self, project_id: str, days: int = 7) -> IssueTriageResult:
        """Issue triage — recently-opened issues missing labels, assignee, or milestone.

        Args:
            days: Lookback window in days (default 7; options: 7, 14, 30)
        """
        validate_id(project_id, "project")
        return IssueTriageResult.model_validate(
            self._request("GET", f"/projects/{project_id}/github/issue-triage?days={days}")
        )

    def get_issue_flow(self, project_id: str, days: int = 30) -> IssueFlowResult:
        """Daily issue open/close flow — backlog burn-down visibility.

        Args:
            days: Lookback window in days (default 30; range: 7-90)
        """
        validate_id(project_id, "project")
        return IssueFlowResult.model_validate(
            self._request("GET", f"/projects/{project_id}/github/issue-flow?days={days}")
        )

    def get_issue_cycle_time(self, project_id: str, days: int = 90) -> IssueCycleTimeResult:
        """Get issue cycle time by label (avg/median days open to close)."""
        return self._client.get(
            f"/v1/projects/{project_id}/github/issue-cycle-time",
            params={"days": days},
            response_model=IssueCycleTimeResult,
        )

    def get_issue_throughput(self, project_id: str, weeks: int = 8) -> IssueThroughputResult:
        """Get weekly closed issue throughput trend (delivery tracker)."""
        return self._client.get(
            f"/v1/projects/{project_id}/github/issue-throughput",
            params={"weeks": weeks},
            response_model=IssueThroughputResult,
        )

    def get_issue_resolvers(self, project_id: str, days: int = 30) -> IssueResolversResult:
        """Get issue resolver leaderboard — top contributors by closed issue count."""
        return self._client.get(
            f"/v1/projects/{project_id}/github/issue-resolvers",
            params={"days": days},
            response_model=IssueResolversResult,
        )

    def get_cycle_time_trend(self, project_id: str, weeks: int = 8) -> CycleTimeTrendResult:
        """Get weekly average issue cycle time trend — are we getting faster or slower?"""
        return self._client.get(
            f"/v1/projects/{project_id}/github/cycle-time-trend",
            params={"weeks": weeks},
            response_model=CycleTimeTrendResult,
        )

    def get_pr_merge_time(self, project_id: str, days: int = 90) -> PrMergeTimeResult:
        """Get PR open→merge time distribution: p25/p50/p75/p95, buckets, per-author avg."""
        return self._client.get(
            f"/v1/projects/{project_id}/github/pr-merge-time",
            params={"days": days},
            response_model=PrMergeTimeResult,
        )

    def get_contributor_momentum(
        self, project_id: str, days: int = 28
    ) -> ContributorMomentumResult:
        """Get contributor commit momentum: accelerating/stable/fading vs prior period."""
        return self._client.get(
            f"/v1/projects/{project_id}/github/contributor-momentum",
            params={"days": days},
            response_model=ContributorMomentumResult,
        )

    def get_agent_audit_trail(self, project_id: str, days: int = 90) -> AgentAuditResult:
        """Get AI coding assistant attribution audit trail for a project."""
        return self._client.get(
            f"/v1/projects/{project_id}/github/agent-audit",
            params={"days": days},
            response_model=AgentAuditResult,
        )

    def get_scope_creep(self, project_id: str, days: int = 90) -> ScopeCreepResult:
        """Get scope creep detection report — PRs that changed >20 or >50 files."""
        return self._client.get(
            f"/v1/projects/{project_id}/github/scope-creep",
            params={"days": days},
            response_model=ScopeCreepResult,
        )

    def get_assignee_cycle_time(self, project_id: str, days: int = 90) -> AssigneeCycleTimeResult:
        """Get per-assignee issue cycle time with trend vs prior half-period."""
        return self._client.get(
            f"/v1/projects/{project_id}/github/assignee-cycle-time",
            params={"days": days},
            response_model=AssigneeCycleTimeResult,
        )

    def get_pr_task_alignment(self, project_id: str, days: int = 90) -> PRTaskAlignmentResult:
        """Detect semantic drift between PRs and their linked issues."""
        return self._client.get(
            f"/v1/projects/{project_id}/github/pr-task-alignment",
            params={"days": days},
            response_model=PRTaskAlignmentResult,
        )

    def get_test_gap(self, project_id: str, days: int = 90) -> TestGapResult:
        """Test coverage gap — merged PRs without test changes, by author and week."""
        return self._client.get(
            f"/v1/projects/{project_id}/github/test-gap",
            params={"days": days},
            response_model=TestGapResult,
        )

    def get_dora_metrics(self, project_id: str, days: int = 90) -> DORAResult:
        """DORA engineering excellence metrics — deploy frequency, lead time, CFR, MTTR."""
        return self._client.get(
            f"/v1/projects/{project_id}/github/dora-metrics",
            params={"days": days},
            response_model=DORAResult,
        )

    def get_ai_vs_human_quality(self, project_id: str, days: int = 90) -> AIvsHumanResult:
        """Compare PR quality scores between AI-authored and human-authored PRs."""
        return self._client.get(
            f"/v1/projects/{project_id}/github/ai-vs-human-quality",
            params={"days": days},
            response_model=AIvsHumanResult,
        )

    def get_bus_factor(self, project_id: str, days: int = 90) -> BusFactorResult:
        """Identify knowledge concentration risk — repos and files dominated by a single contributor."""
        return self._client.get(
            f"/v1/projects/{project_id}/github/bus-factor",
            params={"days": days},
            response_model=BusFactorResult,
        )

    def get_review_network(self, project_id: str, days: int = 90) -> ReviewNetworkResult:
        """Map team code review collaboration — who reviews whose code, silo detection."""
        return self._client.get(
            f"/v1/projects/{project_id}/github/review-network",
            params={"days": days},
            response_model=ReviewNetworkResult,
        )

    def get_review_depth(self, project_id: str, days: int = 90) -> ReviewDepthResult:
        """Reviewer thoroughness analytics — scrutiny rate, rubber-stamp vs rigorous."""
        return self._client.get(
            f"/v1/projects/{project_id}/github/review-depth",
            params={"days": days},
            response_model=ReviewDepthResult,
        )

    def review_pr_code(
        self,
        project_id: str,
        pr_number: int,
        *,
        repo_full_name: Optional[str] = None,
        format: bool = False,
    ) -> PRCodeReviewResult:
        """AST-level PR code review — quality score (0-100), grade (A-F), smells, security."""
        body: Dict[str, Any] = {"prNumber": pr_number, "format": format}
        if repo_full_name is not None:
            body["repoFullName"] = repo_full_name
        return self._client.post(
            f"/v1/projects/{project_id}/github/pr-review",
            json=body,
            response_model=PRCodeReviewResult,
        )

    def submit_pr_review(
        self,
        project_id: str,
        pr_number: int,
        *,
        repo_full_name: Optional[str] = None,
        dry_run: bool = False,
    ) -> SubmitPRReviewResult:
        """Run AST analysis and post the review with inline comments to GitHub."""
        body: Dict[str, Any] = {"prNumber": pr_number, "dryRun": dry_run}
        if repo_full_name is not None:
            body["repoFullName"] = repo_full_name
        return self._client.post(
            f"/v1/projects/{project_id}/github/pr-submit-review",
            json=body,
            response_model=SubmitPRReviewResult,
        )

    def check_pr_quality_gate(
        self,
        project_id: str,
        pr_number: int,
        *,
        repo_full_name: Optional[str] = None,
        gate: Optional[Any] = None,
        post_status: bool = False,
    ) -> QualityGateResult:
        """Evaluate a PR against a quality gate — returns PASSED/FAILED with condition detail."""
        body: Dict[str, Any] = {"prNumber": pr_number, "postStatus": post_status}
        if repo_full_name is not None:
            body["repoFullName"] = repo_full_name
        if gate is not None:
            body["gate"] = gate
        return self._client.post(
            f"/v1/projects/{project_id}/github/pr-quality-gate",
            json=body,
            response_model=QualityGateResult,
        )

    def get_action_plan(self, project_id: str) -> ActionPlanResult:
        """Ranked code improvement action plan — SAST findings, worst functions, uncovered hotspots."""
        return self._client.get(
            f"/v1/projects/{project_id}/github/action-plan",
            response_model=ActionPlanResult,
        )

    def get_tech_debt(self, project_id: str) -> TechDebtResult:
        """SonarQube-style technical debt breakdown by category with remediation estimate and grade."""
        return self._client.get(
            f"/v1/projects/{project_id}/github/tech-debt",
            response_model=TechDebtResult,
        )

    def list_custom_rules(self, project_id: str) -> CustomRulesResponse:
        """List all user-defined tree-sitter SAST rules for a project."""
        return self._client.get(
            f"/v1/projects/{project_id}/github/custom-rules",
            response_model=CustomRulesResponse,
        )

    def create_custom_rule(self, project_id: str, **kwargs: Any) -> CustomRule:
        """Create a user-defined tree-sitter SAST rule."""
        return self._client.post(
            f"/v1/projects/{project_id}/github/custom-rules",
            json=kwargs,
            response_model=CustomRule,
        )

    def update_custom_rule(self, project_id: str, rule_id: str, **kwargs: Any) -> CustomRule:
        """Update fields on an existing custom rule."""
        return self._client.patch(
            f"/v1/projects/{project_id}/github/custom-rules/{rule_id}",
            json=kwargs,
            response_model=CustomRule,
        )

    def delete_custom_rule(self, project_id: str, rule_id: str) -> None:
        """Delete a custom rule permanently."""
        self._client.delete(f"/v1/projects/{project_id}/github/custom-rules/{rule_id}")

    def test_custom_rule(self, project_id: str, rule_id: str) -> CustomRuleTestResult:
        """Run a custom rule against the top hotspot files and return matches."""
        return self._client.post(
            f"/v1/projects/{project_id}/github/custom-rules/{rule_id}/test",
            json={},
            response_model=CustomRuleTestResult,
        )
