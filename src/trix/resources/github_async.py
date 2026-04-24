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
    ScanRepoResponse,
    SymbolsResponse,
    VelocityResponse,
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
        data = {"connection_id": connection_id, "repo_id": repo_id, "repo_full_name": repo_full_name}
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
        response = await self._request(
            "GET", f"/projects/{project_id}/github/churn", params=params
        )
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

    async def get_flagged_prs(self, project_id: str) -> FlaggedPRsResponse:
        """Get risk-flagged pull requests (async)."""
        validate_id(project_id, "project")
        response = await self._request("GET", f"/projects/{project_id}/github/flagged-prs")
        return FlaggedPRsResponse.model_validate(response)

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
        response = await self._request(
            "GET", f"/projects/{project_id}/github/improvements/summary"
        )
        return [ImprovementSummaryRow.model_validate(r) for r in response.get("summary", [])]

    async def get_improvements_history(self, project_id: str) -> List[ImprovementsHistoryItem]:
        """Get historical code quality metric snapshots (async)."""
        validate_id(project_id, "project")
        response = await self._request(
            "GET", f"/projects/{project_id}/github/improvements/history"
        )
        return [ImprovementsHistoryItem.model_validate(r) for r in response.get("history", [])]

    async def get_repo_stats(self, project_id: str) -> RepoStatsResponse:
        """Fetch live repo stats: stars, languages, contributors, LOC, README preview (async)."""
        validate_id(project_id, "project")
        response = await self._request(
            "GET", f"/projects/{project_id}/github/improvements/stats"
        )
        return RepoStatsResponse.model_validate(response)
