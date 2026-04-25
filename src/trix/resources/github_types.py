"""Pydantic type models for the GitHub integration resource (ADR-152 Phases 1–5)."""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel


# ── Connections ────────────────────────────────────────────────────────────


class GitHubConnection(BaseModel):
    id: str
    project_id: str
    repo_full_name: str
    webhook_active: bool
    sync_commits: bool
    sync_pull_requests: bool
    sync_issues: bool
    last_webhook_at: Optional[str] = None


class GitHubConnectionsResponse(BaseModel):
    connections: List[GitHubConnection]
    count: int


class LinkRepoResponse(BaseModel):
    connection: GitHubConnection
    webhook_url: str
    webhook_secret: str


# ── Activity ───────────────────────────────────────────────────────────────


class ActivityMemory(BaseModel):
    id: str
    content: str
    type: str
    created_at: str
    metadata: Optional[Dict[str, Any]] = None


class ActivityResponse(BaseModel):
    memories: List[ActivityMemory]
    total: int
    count: int


# ── Churn & Complexity ─────────────────────────────────────────────────────


class ChurnFile(BaseModel):
    file_path: str
    repo_full_name: str
    touch_count: int
    last_touched_at: str


class ChurnFilesResponse(BaseModel):
    files: List[ChurnFile]
    count: int


class FunctionComplexityMetric(BaseModel):
    """Per-function complexity breakdown from tree-sitter AST analysis."""

    name: str
    start_line: int
    end_line: int
    loc: int
    cyclomatic: int
    cognitive: int
    caller_count: Optional[int] = None  # files that call this fn (load-bearing indicator)
    clone_count: Optional[int] = None   # structurally identical functions found
    clone_hash: Optional[str] = None
    clone_partners: Optional[List[str]] = None


class TestCoverageInfo(BaseModel):
    status: str  # "covered" | "uncovered" | "unknown"
    test_file: Optional[str] = None


class FileComplexityMetric(BaseModel):
    file_path: str
    repo_full_name: str
    language: Optional[str] = None
    cyclomatic_complexity: Optional[int] = None
    cognitive_complexity: Optional[int] = None
    loc: Optional[int] = None
    hotspot_score: Optional[float] = None
    complexity_level: Optional[str] = None  # "ok" | "warning" | "critical"
    computed_at: Optional[str] = None
    functions: Optional[List[FunctionComplexityMetric]] = None
    unused_exports: Optional[List[str]] = None
    test_coverage: Optional[TestCoverageInfo] = None


class FileComplexityResponse(BaseModel):
    files: List[FileComplexityMetric]
    count: int


class QualitySummary(BaseModel):
    total_files_tracked: int
    hotspot_count: int
    hotspot_ratio: int


class QualitySummaryResponse(BaseModel):
    summary: QualitySummary
    top_hotspots: List[ChurnFile]


# ── Symbols ────────────────────────────────────────────────────────────────


class CodeSymbol(BaseModel):
    file_path: str
    repo_full_name: str
    symbol_name: str
    symbol_kind: str
    line_start: Optional[int] = None
    language: Optional[str] = None
    churn_score: float


class SymbolsResponse(BaseModel):
    symbols: List[CodeSymbol]
    count: int


# ── Analytics (Phases 3–4) ─────────────────────────────────────────────────


class VelocityResponse(BaseModel):
    merged_last_7_days: int
    merged_last_30_days: int
    avg_cycle_time_hours: Optional[float] = None
    avg_cycle_time_days: Optional[float] = None


class FlaggedPR(BaseModel):
    id: str
    summary: str
    flags: List[str]
    created_at: str


class FlaggedPRsResponse(BaseModel):
    prs: List[FlaggedPR]


class PRBrief(BaseModel):
    id: str
    pr_number: Optional[int] = None
    pr_url: Optional[str] = None
    repo: Optional[str] = None
    title: str
    brief_content: str
    risk_flags: List[str]
    quality_score: Optional[float] = None
    agent: Optional[str] = None  # 'claude', 'copilot', 'cursor', 'gemini' or None
    is_open: bool
    has_tests: bool
    touches_hotspots: bool
    touches_load_bearing: bool
    touches_clones: bool
    scope_creep: bool
    semantic_drift: bool
    created_at: str


class PRBriefsResponse(BaseModel):
    briefs: List[PRBrief]
    total: int
    state: str


class CycleTimeResponse(BaseModel):
    avg_cycle_days_last_30: Optional[float] = None
    avg_cycle_days_30_60: Optional[float] = None
    avg_open_age_days: Optional[float] = None
    open_issue_count: int
    closed_last_30: int
    trend: str


class AgentAttributionResponse(BaseModel):
    total_commits: int
    total_prs: int
    agent_breakdown: Dict[str, int]
    agent_total: int
    human_total: int
    agent_ratio: float
    agent_quality_scores: Dict[str, Optional[float]] = {}
    """Average PR quality score (0-100) per AI tool, keyed by agent name."""
    human_avg_quality: Optional[float] = None
    """Average PR quality score (0-100) for human-authored PRs."""


class LinkedGoal(BaseModel):
    id: str
    title: str
    progress: float
    status: str
    progress_type: str
    last_github_progress: Optional[float] = None
    last_github_updated_at: Optional[str] = None


class GoalProgressResponse(BaseModel):
    goals: List[LinkedGoal]


class GoalProgressEvent(BaseModel):
    id: str
    goal_id: str
    goal_title: str
    goal_status: str
    previous_progress: float
    new_progress: float
    note: Optional[str] = None
    created_at: str


class GoalProgressHistoryResponse(BaseModel):
    history: List[GoalProgressEvent]


class ReleaseReadinessSignals(BaseModel):
    open_prs: int
    blocking_tasks: int
    goal_completion_pct: int
    scope_creep_prs: int


class ReleaseReadinessResponse(BaseModel):
    score: int
    ready: bool
    signals: ReleaseReadinessSignals
    details: Dict[str, Any]


class GenerateNarrativeResponse(BaseModel):
    """Response from POST /narrative (generate)."""

    narrative: str
    stored: bool
    window_days: int


class StoredNarrative(BaseModel):
    """Stored narrative memory record."""

    id: str
    content: str
    created_at: str
    metadata: Optional[Dict[str, Any]] = None


class LatestNarrativeResponse(BaseModel):
    """Response from GET /narrative (fetch latest)."""

    narrative: Optional[StoredNarrative] = None


class ScanRepoResponse(BaseModel):
    """Response from POST /:connectionId/scan."""

    scanned: bool
    commits: int
    prs: int
    issues: int
    files: int
    hotspots: int
    pr_briefs: int
    errors: Optional[List[str]] = None


# ── Phase 5: Code Quality Scanner ─────────────────────────────────────────


class CodeImprovement(BaseModel):
    id: str
    category: str  # dependency|security|performance|refactor|maintenance
    priority: str  # critical|high|medium|low
    title: str
    description: str
    file_path: Optional[str] = None
    evidence: Dict[str, Any] = {}
    status: str  # open|dismissed|in_progress|resolved
    generated_by: str  # rule|llm
    generated_at: str


class CodeImprovementsResponse(BaseModel):
    suggestions: List[CodeImprovement]


class ImprovementGenerateResponse(BaseModel):
    generated: int
    repo: str


class ImprovementSummaryRow(BaseModel):
    category: str
    priority: str
    cnt: str


class ImprovementsHistoryItem(BaseModel):
    id: str
    snapshotted_at: str
    suggestion_count: int
    critical_count: int
    warning_count: int
    total_files: int
    hotspot_count: int


class RepoLanguage(BaseModel):
    name: str
    bytes: int
    pct: float


class RepoContributor(BaseModel):
    login: str
    avatar_url: str
    profile_url: str
    contributions: int


class RepoMeta(BaseModel):
    full_name: str
    description: Optional[str] = None
    stars: int = 0
    forks: int = 0
    open_issues: int = 0
    primary_language: Optional[str] = None
    license: Optional[str] = None
    is_private: bool = False
    size_kb: int = 0


class LocalMetrics(BaseModel):
    analyzed_files: int = 0
    total_loc: int = 0
    hotspot_count: int = 0
    critical_files: int = 0
    warning_files: int = 0


class RepoStatsData(BaseModel):
    repo: Optional[RepoMeta] = None
    languages: List[RepoLanguage] = []
    contributors: List[RepoContributor] = []
    readme: Optional[str] = None
    open_pr_count: Optional[int] = None
    local_metrics: LocalMetrics = LocalMetrics()


class RepoStatsResponse(BaseModel):
    stats: RepoStatsData


class ReviewerStat(BaseModel):
    reviewer: str
    total: int
    approvals: int
    changes_requested: int


class ReviewStats(BaseModel):
    total_reviews: int
    total_approvals: int
    total_changes_requested: int
    approval_rate: Optional[float] = None
    top_reviewers: List[ReviewerStat] = []


class WeeklyActivityDay(BaseModel):
    day: str  # ISO date YYYY-MM-DD
    commits: int
    prs: int
    issues: int
    total: int


class DebtCategory(BaseModel):
    category: str
    count: int
    minutes: int


class TechnicalDebt(BaseModel):
    total_minutes: int = 0
    total_hours: float = 0.0
    by_category: List[DebtCategory] = []


class QualityCheck(BaseModel):
    id: str
    label: str
    passed: bool
    value: Optional[float] = None
    threshold: float
    unit: Optional[str] = None


class QualityGate(BaseModel):
    passed: bool
    checks: List[QualityCheck] = []
    score: int = 0


class PRQualityWeek(BaseModel):
    """One data point in the 12-week PR quality score trend."""

    week_start: str
    """ISO date (YYYY-MM-DD) for the Monday of this week."""
    avg_quality: int
    """Average PR quality score (0-100) across reviewed PRs that week."""
    pr_count: int
    """Number of PRs with a quality score that week."""


class AgentPRResult(BaseModel):
    pr_number: int
    pr_url: str
    branch_name: str
    sha: str


class SecurityFinding(BaseModel):
    category: str
    priority: str
    title: str
    description: str
    file_path: Optional[str] = None
    evidence: Dict[str, Any] = {}
    generated_by: str = "rule"


class DepVulnEvidence(BaseModel):
    vuln_id: str = ""
    package: str = ""
    ecosystem: str = ""
    cvss: Optional[float] = None
    fix_version: Optional[str] = None
    url: Optional[str] = None


class DepVuln(BaseModel):
    category: str = "dependency"
    priority: str
    title: str
    description: str
    file_path: Optional[str] = None
    evidence: DepVulnEvidence = DepVulnEvidence()


class PRFileMetric(BaseModel):
    path: str
    cc: Optional[int] = None
    cogc: Optional[int] = None
    mi: Optional[int] = None
    loc: Optional[int] = None
    test_coverage: Optional[Dict[str, Any]] = None
    unused_exports: List[str] = []


class PRReviewResult(BaseModel):
    review: Dict[str, Any]
    quality_score: int = 100
    signals: List[Dict[str, Any]] = []
    smells: List[Dict[str, Any]] = []
    security_findings: List[SecurityFinding] = []
    dep_vulns: List[DepVuln] = []
    file_metrics: List[PRFileMetric] = []
    inline_comments: int = 0
    files_analyzed: int = 0
    unsupported_files: int = 0
    posted: bool = False


class ScanCodeSummary(BaseModel):
    secrets: int = 0
    security: int = 0
    critical: int = 0
    high: int = 0
    safe: bool = True


class ScanCodeResult(BaseModel):
    file_path: str
    findings: List[SecurityFinding] = []
    summary: ScanCodeSummary = ScanCodeSummary()


# ── Code health analytics (Session 15–16) ────────────────────────────────────


class CodeSummaryDebt(BaseModel):
    total_minutes: int = 0
    total_hours: float = 0.0
    top_categories: List[Dict[str, Any]] = []


class CodeSummaryResult(BaseModel):
    quality_gate: Dict[str, Any] = {}
    debt: CodeSummaryDebt = CodeSummaryDebt()
    hotspots: List[Dict[str, Any]] = []
    open_counts: Dict[str, int] = {}
    top_smells: List[Dict[str, Any]] = []
    languages: List[Dict[str, Any]] = []
    last_scanned_at: Optional[str] = None


class CloneInstance(BaseModel):
    file_path: str
    repo_full_name: str
    fn_name: str
    start_line: Optional[int] = None
    loc: Optional[int] = None
    language: Optional[str] = None


class CloneGroup(BaseModel):
    clone_hash: str
    instance_count: int
    max_loc: Optional[int] = None
    instances: List[CloneInstance] = []


class CloneGroupsResult(BaseModel):
    groups: List[CloneGroup] = []
    total_groups: int = 0


class DeadExportFile(BaseModel):
    file_path: str
    repo_full_name: str
    language: Optional[str] = None
    dead_count: int = 0
    symbols: List[str] = []


class DeadExportsResult(BaseModel):
    files: List[DeadExportFile] = []
    total_files: int = 0
    total_dead_symbols: int = 0


class TestCoverageFile(BaseModel):
    file_path: str
    repo_full_name: str
    language: Optional[str] = None
    hotspot_score: Optional[float] = None
    cyclomatic_complexity: Optional[int] = None
    test_file: Optional[str] = None


class TestCoverageResult(BaseModel):
    uncovered: List[TestCoverageFile] = []
    covered: List[TestCoverageFile] = []
    total_files: int = 0
    uncovered_count: int = 0
    covered_count: int = 0
    coverage_ratio: int = 0


class LoadBearingFunction(BaseModel):
    file_path: str
    repo_full_name: str
    language: Optional[str] = None
    fn_name: str
    caller_count: int = 0
    cyclomatic: Optional[int] = None
    loc: Optional[int] = None
    start_line: Optional[int] = None
    clone_count: int = 0


class LoadBearingResult(BaseModel):
    functions: List[LoadBearingFunction] = []
    count: int = 0
    min_callers: int = 3


class BugDensityFile(BaseModel):
    file_path: str
    repo_full_name: str
    language: Optional[str] = None
    loc: int = 0
    hotspot_score: Optional[float] = None
    issue_count: int = 0
    critical_count: int = 0
    high_count: int = 0
    density_per_kloc: float = 0.0


class BugDensityResult(BaseModel):
    files: List[BugDensityFile] = []
    count: int = 0



# ── Health Snapshot ─────────────────────────────────────────────────────────


class HealthSnapshotRisk(BaseModel):
    type: str
    label: str


class HealthSnapshotQualityGate(BaseModel):
    passed: Optional[bool] = None
    avg_maintainability_index: Optional[int] = None
    total_files: int = 0
    critical_files: int = 0


class HealthSnapshotSuggestions(BaseModel):
    critical: int = 0
    high: int = 0
    total: int = 0


class HealthSnapshotVelocity(BaseModel):
    merged_last_7_days: int = 0
    merged_last_30_days: int = 0


class HealthSnapshotOpenPRs(BaseModel):
    total: int = 0
    risky: int = 0
    avg_quality_score: Optional[int] = None


class HealthSnapshotPRQualityTrend(BaseModel):
    direction: Optional[str] = None  # 'improving' | 'stable' | 'declining' | None
    current_avg: Optional[int] = None
    week_delta: Optional[int] = None


class HealthSnapshotReviewTurnaround(BaseModel):
    avg_hours: Optional[int] = None
    unreviewed_count: int = 0


class HealthSnapshotUrgentItems(BaseModel):
    critical: int = 0
    urgent_total: int = 0


class HealthSnapshotIssueBacklog(BaseModel):
    total_open: int = 0
    unassigned_count: int = 0


class HealthSnapshotReviewCoverage(BaseModel):
    total_merged: int = 0
    coverage_pct: Optional[int] = None
    lookback_days: int = 30


class HealthSnapshotResponse(BaseModel):
    quality_gate: HealthSnapshotQualityGate
    suggestions: HealthSnapshotSuggestions
    velocity: HealthSnapshotVelocity
    open_prs: HealthSnapshotOpenPRs
    top_risks: List[HealthSnapshotRisk] = []
    pr_quality_trend: Optional[HealthSnapshotPRQualityTrend] = None
    review_turnaround: Optional[HealthSnapshotReviewTurnaround] = None
    urgent_items: Optional[HealthSnapshotUrgentItems] = None
    issue_backlog: Optional[HealthSnapshotIssueBacklog] = None
    review_coverage: Optional[HealthSnapshotReviewCoverage] = None


class BranchInfo(BaseModel):
    name: str
    repo_full_name: Optional[str] = None
    last_commit_at: Optional[str] = None
    commit_count: int = 0
    open_pr_number: Optional[int] = None
    open_pr_url: Optional[str] = None
    is_default: bool = False
    is_stale: bool = False


class ActiveBranchesResult(BaseModel):
    branches: List[BranchInfo] = []
    count: int = 0


class ContributorQualityStat(BaseModel):
    author: str
    pr_count: int = 0
    avg_quality: Optional[float] = None
    with_tests_count: int = 0
    test_coverage_pct: int = 0
    avg_merge_days: Optional[float] = None
    last_active_at: Optional[str] = None
    reviews_given: int = 0
    approvals: int = 0


class ContributorQualityResult(BaseModel):
    contributors: List[ContributorQualityStat] = []
    count: int = 0


class OpenPRAging(BaseModel):
    pr_number: Optional[int] = None
    title: Optional[str] = None
    author: Optional[str] = None
    url: Optional[str] = None
    repo: Optional[str] = None
    head_branch: Optional[str] = None
    requested_reviewers: List[str] = []
    opened_at: Optional[str] = None
    last_updated_at: Optional[str] = None
    age_days: int = 0
    is_stale: bool = False
    has_review: bool = False


class PrAgingResult(BaseModel):
    prs: List[OpenPRAging] = []
    count: int = 0
    stale_days: int = 7


class PRSizeBucket(BaseModel):
    size: str
    key: str
    count: int = 0
    pct: int = 0
    avg_quality: Optional[float] = None
    test_coverage_pct: int = 0


class PrSizeDistributionResult(BaseModel):
    distribution: List[PRSizeBucket] = []
    total: int = 0


class ReviewAuthorStat(BaseModel):
    author: str
    reviewed_count: int = 0
    avg_hours: Optional[float] = None
    within_24h_count: int = 0
    within_24h_pct: int = 0


class ReviewTurnaroundResult(BaseModel):
    avg_hours: Optional[float] = None
    reviewed_within_24h_pct: int = 0
    total_reviewed: int = 0
    unreviewed_count: int = 0
    author_stats: List[ReviewAuthorStat] = []


class WorkQueueItem(BaseModel):
    type: str
    priority: str
    title: str
    detail: str
    url: Optional[str] = None


class WorkQueueResult(BaseModel):
    items: List[WorkQueueItem] = []
    count: int = 0

class ReviewerPendingPR(BaseModel):
    pr_number: Optional[int] = None
    title: Optional[str] = None
    url: Optional[str] = None


class ReviewerWorkloadStat(BaseModel):
    reviewer: str
    pending_count: int = 0
    avg_pending_age_hours: Optional[int] = None
    pending_prs: List[ReviewerPendingPR] = []
    total_reviews: int = 0
    approvals: int = 0
    avg_response_hours: Optional[float] = None


class ReviewerWorkloadResult(BaseModel):
    reviewers: List[ReviewerWorkloadStat] = []
    count: int = 0


class ApprovedPR(BaseModel):
    pr_number: Optional[int] = None
    title: Optional[str] = None
    author: Optional[str] = None
    url: Optional[str] = None
    repo: Optional[str] = None
    age_days: int = 0
    approval_count: int = 0
    approvers: List[str] = []
    has_changes_requested: bool = False


class ApprovedPRsResult(BaseModel):
    prs: List[ApprovedPR] = []
    count: int = 0


class IssueLabelCount(BaseModel):
    label: str
    count: int = 0


class BacklogIssue(BaseModel):
    issue_number: Optional[int] = None
    title: str = ""
    author: Optional[str] = None
    url: Optional[str] = None
    assignees: List[str] = []
    labels: List[str] = []
    milestone: Optional[str] = None
    age_days: int = 0


class IssueBacklogResult(BaseModel):
    total_open: int = 0
    unassigned_count: int = 0
    unlabeled_count: int = 0
    oldest_age_days: int = 0
    avg_age_days: int = 0
    label_distribution: List[IssueLabelCount] = []
    oldest_issues: List[BacklogIssue] = []


class AuthorReviewCoverage(BaseModel):
    author: str
    merged_count: int = 0
    reviewed_count: int = 0
    unreviewed_count: int = 0
    coverage_pct: int = 0


class ReviewCoverageResult(BaseModel):
    total_merged: int = 0
    reviewed_count: int = 0
    unreviewed_count: int = 0
    coverage_pct: Optional[int] = None
    lookback_days: int = 90
    by_author: List[AuthorReviewCoverage] = []


# ── Commit Leaders ──────────────────────────────────────────────────────────


class CommitLeader(BaseModel):
    author: str
    commit_count: int = 0
    active_days: int = 0
    repos: int = 0


class CommitLeadersResult(BaseModel):
    leaders: List[CommitLeader] = []
    total_commits: int = 0
    lookback_days: int = 30


# ── Issue Assignee Workload ─────────────────────────────────────────────────


class AssigneeStat(BaseModel):
    assignee: str
    open_count: int = 0
    oldest_days: int = 0
    avg_days: int = 0


class IssueAssigneesResult(BaseModel):
    assignees: List[AssigneeStat] = []
    total_assignees: int = 0


# ── Milestone Progress ──────────────────────────────────────────────────────


class MilestoneStat(BaseModel):
    name: str
    open_count: int = 0
    closed_count: int = 0
    total_count: int = 0
    progress_pct: int = 0


class MilestonesResult(BaseModel):
    milestones: List[MilestoneStat] = []
    total_milestones: int = 0
