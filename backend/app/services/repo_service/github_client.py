import httpx
from dataclasses import dataclass
from typing import Optional
from backend.app.services.repo_service.repo_validator import ParsedRepoURL


GITHUB_API_BASE = "https://api.github.com"
REQUEST_TIMEOUT = 10.0


@dataclass
class RepoMetadata:
    owner: str
    name: str
    full_name: str
    description: Optional[str]
    default_branch: str
    stars: int
    forks: int
    language: Optional[str]
    size_kb: int
    is_private: bool
    clone_url: str


class GitHubAPIError(Exception):
    def __init__(self, message: str, status_code: Optional[int] = None):
        super().__init__(message)
        self.status_code = status_code


class GitHubClient:
    def __init__(self, token: Optional[str] = None):
        headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        if token:
            headers["Authorization"] = f"Bearer {token}"

        self._client = httpx.AsyncClient(
            base_url=GITHUB_API_BASE,
            headers=headers,
            timeout=REQUEST_TIMEOUT,
        )

    async def fetch_repo_metadata(self, parsed: ParsedRepoURL) -> RepoMetadata:
        endpoint = f"/repos/{parsed.owner}/{parsed.name}"

        response = await self._client.get(endpoint)

        if response.status_code == 404:
            raise GitHubAPIError(
                f"Repository '{parsed.owner}/{parsed.name}' not found or is private.",
                status_code=404,
            )
        if response.status_code == 403:
            raise GitHubAPIError("GitHub API rate limit exceeded.", status_code=403)
        if response.status_code != 200:
            raise GitHubAPIError(
                f"Unexpected GitHub API response: {response.status_code}",
                status_code=response.status_code,
            )

        data = response.json()
        return _parse_metadata(data)

    async def close(self):
        await self._client.aclose()

    async def __aenter__(self):
        return self

    async def __aexit__(self, *_):
        await self.close()


def _parse_metadata(data: dict) -> RepoMetadata:
    return RepoMetadata(
        owner=data["owner"]["login"],
        name=data["name"],
        full_name=data["full_name"],
        description=data.get("description"),
        default_branch=data.get("default_branch", "main"),
        stars=data.get("stargazers_count", 0),
        forks=data.get("forks_count", 0),
        language=data.get("language"),
        size_kb=data.get("size", 0),
        is_private=data.get("private", False),
        clone_url=data["clone_url"],
    )