"""GitHub project integration resource for Trix SDK (ADR-152)."""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel

from .base import BaseAsyncResource, BaseSyncResource
from ..utils.security import validate_id


# ── Types ──────────────────────────────────────────────────────────────────


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


class ChurnFile(BaseModel):
    file_path: str
    repo_full_name: str
    touch_count: int
    last_touched_at: str


class ChurnFilesResponse(BaseModel):
    files: List[ChurnFile]
    count: int


class QualitySummary(BaseModel):
    total_files_tracked: int
    hotspot_count: int
    hotspot_ratio: int


class QualitySummaryResponse(BaseModel):
    summary: QualitySummary
    top_hotspots: List[ChurnFile]


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


# ── Async resource ─────────────────────────────────────────────────────────


class AsyncGitHubResource(BaseAsyncResource):
    """Async resource for GitHub project integration."""

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
