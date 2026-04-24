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

