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
    clone_count: Optional[int] = None  # structurally identical functions found
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


class ReleaseReadinessBlocker(BaseModel):
    issue_number: str
    title: str
    url: str
    author: str
    labels: List[str]
    age_days: int


class ReleaseReadinessUnreviewedPR(BaseModel):
    pr_number: str
    title: str
    url: str
    author: str
    age_days: int
    requested_reviewers: List[str]


class ReleaseReadinessStalePR(BaseModel):
    pr_number: str
    title: str
    url: str
    author: str
    age_days: int


class ReleaseReadinessHotspot(BaseModel):
    file_path: str
    repo: str
    hotspot_score: float


class ReleaseReadinessOpenIssues(BaseModel):
    count: int
    blocker_count: int
    blockers: List[ReleaseReadinessBlocker]


class ReleaseReadinessOpenPRs(BaseModel):
    count: int
    unreviewed_count: int
    stale_count: int
    unreviewed: List[ReleaseReadinessUnreviewedPR]
    stale_prs: List[ReleaseReadinessStalePR]


class ReleaseReadinessResponse(BaseModel):
    readiness_score: int
    open_issues: ReleaseReadinessOpenIssues
    open_prs: ReleaseReadinessOpenPRs
    recent_merges: Dict[str, Any]
    top_hotspots: List[ReleaseReadinessHotspot]


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


class HealthSnapshotIssueFlow(BaseModel):
    opened_last_7d: int = 0
    closed_last_7d: int = 0
    net_flow_7d: int = 0


class HealthSnapshotIssueThroughput(BaseModel):
    avg_per_week: float = 0
    trend: str = "stable"  # 'improving' | 'stable' | 'declining'


class HealthSnapshotSlowestCycleLabel(BaseModel):
    label: str
    avg_days: float


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
    issue_flow: Optional[HealthSnapshotIssueFlow] = None
    issue_throughput: Optional[HealthSnapshotIssueThroughput] = None
    slowest_cycle_label: Optional[HealthSnapshotSlowestCycleLabel] = None


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


# ── Label Velocity ──────────────────────────────────────────────────────────


class LabelVelocity(BaseModel):
    label: str
    opened_count: int = 0
    closed_count: int = 0
    total_count: int = 0
    net_flow: int = 0


class LabelVelocityResult(BaseModel):
    labels: List[LabelVelocity] = []
    lookback_days: int = 30


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
    predicted_date: Optional[str] = None


class MilestonesResult(BaseModel):
    milestones: List[MilestoneStat] = []
    total_milestones: int = 0


# ── Week-over-Week Velocity ────────────────────────────────────────────────────

from typing import Literal


class WeekStat(BaseModel):
    label: str
    this_week: int = 0
    last_week: int = 0
    delta: int = 0
    trend: Literal["up", "down", "flat"] = "flat"


class WeekOverWeekResult(BaseModel):
    prs: WeekStat
    issues: WeekStat
    commits: WeekStat


# ── Issue Triage ───────────────────────────────────────────────────────────────


class TriageIssue(BaseModel):
    issue_number: str
    title: str
    url: Optional[str] = None
    repo: Optional[str] = None
    author: Optional[str] = None
    age_hours: int = 0
    missing: List[Literal["labels", "assignee", "milestone"]] = []


class IssueTriageResult(BaseModel):
    issues: List[TriageIssue] = []
    count: int = 0
    lookback_days: int = 7


# ── Issue Flow ─────────────────────────────────────────────────────────────────


class IssueFlowDay(BaseModel):
    day: str
    opened: int = 0
    closed: int = 0
    net: int = 0


class IssueFlowResult(BaseModel):
    data: List[IssueFlowDay] = []
    total_opened: int = 0
    total_closed: int = 0
    net_flow: int = 0
    lookback_days: int = 30


class CycleTimeByLabel(BaseModel):
    """Cycle time stats for a single GitHub label."""

    label: str
    issue_count: int
    avg_days: float
    median_days: float
    min_days: float
    max_days: float


class IssueCycleTimeResult(BaseModel):
    """Issue cycle time by label — average/median days from open to close."""

    by_label: List["CycleTimeByLabel"]
    lookback_days: int


class IssueThroughputWeek(BaseModel):
    """One week of issue throughput data."""

    week_start: str
    closed_count: int
    opened_count: int


class IssueThroughputResult(BaseModel):
    """Weekly issue throughput trend."""

    weeks: List["IssueThroughputWeek"]
    avg_closed_per_week: float
    trend: str  # 'improving' | 'stable' | 'declining'
    lookback_weeks: int


# ── Issue Resolver Leaderboard (Phase 4) ──────────────────────────────────────


class IssueResolver(BaseModel):
    """One entry in the issue resolver leaderboard."""

    login: str
    closed_count: int
    pct: float


class IssueResolversResult(BaseModel):
    """Issue resolver leaderboard — top contributors by closed issue count."""

    resolvers: List["IssueResolver"]
    total_closed: int
    lookback_days: int


# ── Cycle Time Trend (Phase 4: Estimation Accuracy Tracker) ──────────────────


class CycleTimeTrendWeek(BaseModel):
    """One week of cycle time data."""

    week_start: str
    avg_days: Optional[float] = None
    issue_count: int


class CycleTimeTrendResult(BaseModel):
    """Weekly average issue cycle time trend."""

    weeks: List["CycleTimeTrendWeek"]
    trend: str  # 'improving' | 'stable' | 'declining'
    overall_avg_days: Optional[float] = None
    lookback_weeks: int


class MergeTimeBucket(BaseModel):
    """Count of PRs in a merge-time bucket."""

    label: str
    key: str
    count: int


class MergeTimeAuthor(BaseModel):
    """Per-author PR merge time stats."""

    author: str
    pr_count: int
    avg_hours: Optional[float] = None


class PrMergeTimeResult(BaseModel):
    """PR open→merge cycle time distribution."""

    p25: Optional[float] = None
    p50: Optional[float] = None
    p75: Optional[float] = None
    p95: Optional[float] = None
    avg_hours: Optional[float] = None
    total_merged: int
    lookback_days: int
    distribution: List["MergeTimeBucket"]
    author_stats: List["MergeTimeAuthor"]


class ContributorMomentum(BaseModel):
    """Per-contributor commit momentum vs prior period."""

    author: str
    recent_commits: int
    previous_commits: int
    pct_change: Optional[int] = None
    trend: str  # 'accelerating' | 'stable' | 'fading'


class ContributorMomentumResult(BaseModel):
    """Contributor commit momentum comparison."""

    contributors: List["ContributorMomentum"]
    period_days: int


class AgentBreakdown(BaseModel):
    """Per-AI-assistant PR attribution count."""

    agent: str
    tag: str
    label: str
    count: int
    pct: int


class AgentWeeklyTrend(BaseModel):
    """Weekly AI-attributed PR trend data point."""

    week: str
    total: int
    agent_count: int
    agent_pct: int


class AgentAuditResult(BaseModel):
    """AI coding assistant audit trail for a project."""

    total_prs: int
    agent_prs: int
    agent_pct: int
    lookback_days: int
    by_agent: List["AgentBreakdown"]
    weekly_trend: List["AgentWeeklyTrend"]


class ScopeCreepSummary(BaseModel):
    """Summary counts for scope creep detection."""

    total_prs: int
    scope_creep_count: int
    large_count: int
    flagged_count: int
    flagged_pct: int


class ScopeCreepPR(BaseModel):
    """A PR that exceeded the scope creep threshold."""

    title: str
    author: str
    url: str
    repo: str
    changed_files: int
    additions: int
    deletions: int
    severity: str
    created_at: str


class ScopeCreepAuthor(BaseModel):
    """Per-author scope creep statistics."""

    author: str
    total_prs: int
    scope_creep_count: int
    large_count: int
    avg_files: int


class ScopeCreepWeek(BaseModel):
    """Weekly scope creep trend data point."""

    week: str
    scope_creep_count: int
    large_count: int


class ScopeCreepResult(BaseModel):
    """Scope creep detection report for a project."""

    summary: ScopeCreepSummary
    lookback_days: int
    top_prs: List["ScopeCreepPR"]
    by_author: List["ScopeCreepAuthor"]
    weekly_trend: List["ScopeCreepWeek"]


class AssigneeStatItem(BaseModel):
    """Per-assignee issue cycle time with trend."""

    assignee: str
    closed_count: int
    avg_days: Optional[float] = None
    prev_avg_days: Optional[float] = None
    trend: str
    pct_change: Optional[int] = None


class AssigneeCycleTimeResult(BaseModel):
    """Per-assignee issue cycle time comparison result."""

    assignees: List["AssigneeStatItem"]
    team_avg_days: Optional[float] = None
    lookback_days: int


class AlignmentEntry(BaseModel):
    pr_number: str
    pr_title: str
    pr_url: str
    author: str
    issue_number: str
    issue_title: str
    similarity: float
    signal: str  # 'aligned' | 'partial' | 'drifted'


class PRTaskAlignmentSummary(BaseModel):
    analyzed: int
    aligned_count: int
    partial_count: int
    drifted_count: int
    unchecked_count: int


class PRTaskAlignmentResult(BaseModel):
    summary: PRTaskAlignmentSummary
    drifted: List[AlignmentEntry]
    partial: List[AlignmentEntry]
    lookback_days: int


# ── DORA Metrics (ADR-152 Phase 4 extension) ──────────────────────────────────


class DORADeployFreqWeek(BaseModel):
    """One week of deployment frequency data."""

    week: str
    merges: int


class DORALeadTimeWeek(BaseModel):
    """One week of lead time data."""

    week: str
    avg_hours: Optional[int] = None


class DORAcfrWeek(BaseModel):
    """One week of change failure rate data."""

    week: str
    total: int
    failures: int
    pct: int


class DORADeployFrequency(BaseModel):
    per_day: float
    per_week: float
    total_merges: int
    rating: str  # 'elite' | 'high' | 'medium' | 'low'


class DORALeadTime(BaseModel):
    median_hours: Optional[int] = None
    avg_hours: Optional[int] = None
    sample_size: int
    rating: Optional[str] = None


class DORAChangeFailureRate(BaseModel):
    pct: int
    failure_merges: int
    total_merges: int
    rating: str


class DORAMttr(BaseModel):
    median_hours: Optional[int] = None
    sample_size: int
    rating: Optional[str] = None


class DORAWeeklyTrend(BaseModel):
    deploy_freq: List[DORADeployFreqWeek] = []
    lead_time: List[DORALeadTimeWeek] = []
    change_failure_rate: List[DORAcfrWeek] = []


class DORAResult(BaseModel):
    """DORA engineering excellence metrics — deploy frequency, lead time, CFR, MTTR."""

    deployment_frequency: DORADeployFrequency
    lead_time: DORALeadTime
    change_failure_rate: DORAChangeFailureRate
    mttr: DORAMttr
    weekly_trend: DORAWeeklyTrend
    lookback_days: int


# ── Test Gap (ADR-152 Phase 4) ─────────────────────────────────────────────


class TestGapPR(BaseModel):
    """A merged PR that had no associated test changes."""

    prNumber: str
    title: str
    url: str
    author: str
    repo: str
    agent: Optional[str] = None
    createdAt: str


class TestGapAuthor(BaseModel):
    """Per-author test gap statistics."""

    author: str
    totalPRs: int
    noTestsCount: int
    hasTestsCount: int
    noTestsPct: int


class TestGapWeek(BaseModel):
    """Weekly test gap trend data point."""

    week: str
    total: int
    noTestsCount: int
    noTestsPct: int


class TestGapSummary(BaseModel):
    """Aggregate test gap summary counts."""

    totalBriefs: int
    noTestsCount: int
    hasTestsCount: int
    noTestsPct: int


class TestGapResult(BaseModel):
    """Test coverage gap report — PRs merged without any test changes."""

    summary: TestGapSummary
    topGaps: List[TestGapPR]
    byAuthor: List[TestGapAuthor]
    weeklyTrend: List[TestGapWeek]
    lookbackDays: int


# ── AI vs Human Code Quality (ADR-152 Phase 4 Extension) ──────────────────────


class AIvsHumanByAgent(BaseModel):
    """Per-AI-tool quality breakdown."""

    agent: str
    avgScore: float
    prCount: int
    topScore: float


class AIvsHumanWeek(BaseModel):
    """Weekly side-by-side AI vs human quality data point."""

    week: str
    aiAvg: Optional[float] = None
    humanAvg: Optional[float] = None
    aiCount: int = 0
    humanCount: int = 0


class AIvsHumanTopPR(BaseModel):
    """Highest-quality AI-authored PR entry."""

    prNumber: str
    title: str
    url: str
    author: str
    agent: str
    qualityScore: float
    createdAt: str


class AIvsHumanSummary(BaseModel):
    """Aggregate AI vs human quality comparison summary."""

    aiAvgScore: Optional[float] = None
    humanAvgScore: Optional[float] = None
    scoreDelta: Optional[float] = None
    aiPrCount: int = 0
    humanPrCount: int = 0


class AIvsHumanResult(BaseModel):
    """AI vs human code quality comparison result."""

    summary: AIvsHumanSummary
    byAgent: List[AIvsHumanByAgent] = []
    weeklyTrend: List[AIvsHumanWeek] = []
    topAIPRs: List[AIvsHumanTopPR] = []
    lookbackDays: int


# ── Bus Factor / Knowledge Concentration Risk (ADR-152) ───────────────────────


class BusFactorAtRiskFile(BaseModel):
    """A hotspot file in an at-risk repo with single-author dominance."""

    filePath: str
    repo: str
    owner: str
    ownerPct: float
    totalCommits: int
    uniqueAuthors: int
    hotspotScore: float
    loc: int


class BusFactorContributor(BaseModel):
    """A contributor who dominates one or more repos."""

    contributor: str
    dominatedRepos: List[str]
    avgDominancePct: float
    totalCommits: int


class BusFactorSummary(BaseModel):
    """Aggregate bus factor risk summary across all repos."""

    totalRepos: int
    atRiskRepos: int
    singleAuthorRepos: int
    avgAuthorsPerRepo: float
    threshold: int


class BusFactorResult(BaseModel):
    """Bus factor knowledge concentration risk report."""

    summary: BusFactorSummary
    atRisk: List[BusFactorAtRiskFile] = []
    byContributor: List[BusFactorContributor] = []
    lookbackDays: int


# ── Review Collaboration Network ──────────────────────────────────────────────


class ReviewEdge(BaseModel):
    """A directional reviewer→author relationship with review count."""

    reviewer: str
    author: str
    reviewCount: int


class ReviewContributor(BaseModel):
    """Per-contributor summary of review activity."""

    name: str
    reviewsGiven: int
    reviewsReceived: int
    uniqueAuthors: int
    uniqueReviewers: int


class ReviewNetworkResult(BaseModel):
    """Team code review collaboration graph."""

    edges: List[ReviewEdge] = []
    contributors: List[ReviewContributor] = []
    lookbackDays: int


class ReviewDepthSummary(BaseModel):
    """Summary of team-wide reviewer thoroughness."""

    totalReviews: int
    totalReviewers: int
    avgScrutinyRate: int
    rubberstampCount: int
    rigorousCount: int


class ReviewerDepthStat(BaseModel):
    """Per-reviewer breakdown of review state distribution."""

    reviewer: str
    totalReviews: int
    approvals: int
    changesRequested: int
    commentsOnly: int
    scrutinyRate: int
    uniquePrs: int


class ReviewDepthResult(BaseModel):
    """Reviewer thoroughness analytics — scrutiny rate and rubber-stamp detection."""

    summary: ReviewDepthSummary
    reviewers: List[ReviewerDepthStat] = []
    lookbackDays: int


class PRCodeReviewSmell(BaseModel):
    """A code smell found during PR review."""

    kind: Optional[str] = None
    severity: Optional[str] = None
    filePath: Optional[str] = None
    line: Optional[int] = None
    message: Optional[str] = None
    file: Optional[str] = None


class PRCodeReviewSecurityFinding(BaseModel):
    """A security finding from OWASP pattern scanning."""

    title: Optional[str] = None
    description: Optional[str] = None
    file_path: Optional[str] = None
    line: Optional[int] = None
    file: Optional[str] = None


class PRCodeReviewFindings(BaseModel):
    """Aggregated findings from PR code review."""

    smells: List[PRCodeReviewSmell] = []
    security: List[PRCodeReviewSecurityFinding] = []
    secrets: List[Any] = []


class PRCodeReviewComplexityDelta(BaseModel):
    """Cyclomatic complexity change for a function across a PR."""

    file: str
    function: str
    ccDelta: int
    locDelta: int


class PRCodeReviewFormatted(BaseModel):
    """GitHub-ready formatted review body and event."""

    body: str
    event: str  # 'APPROVE' | 'COMMENT' | 'REQUEST_CHANGES'


class PRCodeReviewPR(BaseModel):
    """PR metadata returned by PR code review."""

    number: int
    title: str
    url: str
    author: Optional[str] = None
    additions: int
    deletions: int
    changedFiles: int


class PRCodeReviewResult(BaseModel):
    """AST-level PR code review — quality score, grade, smells, and security findings."""

    pr: PRCodeReviewPR
    qualityScore: int
    grade: str  # 'A' | 'B' | 'C' | 'D' | 'F'
    findings: PRCodeReviewFindings
    structuralDiff: List[Any] = []
    complexityDeltas: List[PRCodeReviewComplexityDelta] = []
    analyzedFiles: int
    skippedFiles: int
    formatted: Optional[PRCodeReviewFormatted] = None


class SubmitPRReviewResult(BaseModel):
    """Result of posting a PR review to GitHub."""

    reviewId: Optional[int] = None
    reviewUrl: Optional[str] = None
    event: str  # 'APPROVE' | 'COMMENT' | 'REQUEST_CHANGES'
    grade: str
    qualityScore: int
    analyzedFiles: int
    inlineComments: int
    dryRun: Optional[bool] = None


class QualityGateCondition(BaseModel):
    """A single quality gate condition evaluation."""

    label: str
    actual: Any
    limit: Any
    passed: bool
    mode: str


class QualityGateResult(BaseModel):
    """Result of evaluating a PR against a quality gate."""

    passed: bool
    status: str  # 'PASSED' | 'FAILED'
    grade: str
    qualityScore: int
    conditions: List[QualityGateCondition] = []
    blockers: List[QualityGateCondition] = []
    prNumber: Optional[int] = None
    repo: Optional[str] = None
    analyzedFiles: Optional[int] = None


# ── Batch Scan Code ────────────────────────────────────────────────────────────


class BatchScanFileInput(BaseModel):
    file_path: str
    content: str


class BatchScanFileSummary(BaseModel):
    secrets: int = 0
    security: int = 0
    critical: int = 0
    high: int = 0
    filesScanned: int = 0
    safe: bool = True
    grade: str = "A"


class BatchScanFileResult(BaseModel):
    file_path: str
    findings: List[SecurityFinding] = []
    secrets: int = 0
    security: int = 0
    critical: int = 0
    high: int = 0


class BatchScanCodeResult(BaseModel):
    files: List[BatchScanFileResult] = []
    summary: BatchScanFileSummary = BatchScanFileSummary()


# ── Analyze Code Complexity ────────────────────────────────────────────────────


class CodeComplexityMetrics(BaseModel):
    cyclomatic: int = 0
    cognitive: int = 0
    loc: int = 0
    supported: bool = True


class CodeSmellItem(BaseModel):
    type: str
    severity: str  # 'critical' | 'high' | 'medium' | 'low'
    message: str
    line: Optional[int] = None
    function: Optional[str] = None


class CodeComplexitySummary(BaseModel):
    functionCount: int = 0
    smellCount: int = 0
    designIssues: int = 0
    critical: int = 0
    high: int = 0
    avgCyclomatic: Optional[str] = None


class DesignFinding(BaseModel):
    category: str = ""
    priority: str = "medium"
    title: str = ""
    description: str = ""
    file_path: str = ""
    evidence: Dict[str, Any] = {}
    generated_by: str = "rule"


class AnalyzeCodeComplexityResult(BaseModel):
    file_path: str
    language: str
    metrics: CodeComplexityMetrics = CodeComplexityMetrics()
    functions: List[Dict[str, Any]] = []
    smells: List[CodeSmellItem] = []
    design: List[DesignFinding] = []
    summary: CodeComplexitySummary = CodeComplexitySummary()


# ── CQL (Code Query Language) types ───────────────────────────────────────────

CqlFromMode = Literal[
    "files",
    "functions",
    "suggestions",
    "ast_pattern",
    "hotspots",
    "patterns",
    "dead_code",
    "clones",
    "metrics",
    "coverage",
    "summary",
    "history",
]


class CqlWhereCondition(BaseModel):
    contains: Optional[str] = None
    startsWith: Optional[str] = None
    eq: Optional[Any] = None
    gte: Optional[Any] = None
    lte: Optional[Any] = None
    gt: Optional[Any] = None
    lt: Optional[Any] = None


class CqlQuery(BaseModel):
    """Typed CQL query object for query_code()."""

    from_: Optional[CqlFromMode] = None
    where: Optional[Dict[str, Dict[str, Any]]] = None
    order_by: Optional[str] = None
    order_dir: Optional[Literal["asc", "desc"]] = None
    limit: Optional[int] = None
    language: Optional[str] = None
    pattern: Optional[str] = None
    patterns: Optional[List[str]] = None
    risk: Optional[Literal["high", "medium", "all"]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to API-ready dict (maps from_ → from)."""
        d = self.model_dump(exclude_none=True)
        if "from_" in d:
            d["from"] = d.pop("from_")
        return d
