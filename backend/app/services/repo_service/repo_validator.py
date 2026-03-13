import re
from urllib.parse import urlparse
from dataclasses import dataclass


GITHUB_REPO_PATTERN = re.compile(
    r"^https://github\.com/(?P<owner>[a-zA-Z0-9_.-]+)/(?P<name>[a-zA-Z0-9_.-]+?)(?:\.git)?/?$"
)


@dataclass
class ParsedRepoURL:
    owner: str
    name: str
    url: str


class RepoValidationError(ValueError):
    pass


def validate_and_parse(repo_url: str) -> ParsedRepoURL:
    repo_url = repo_url.strip().rstrip("/")

    parsed = urlparse(repo_url)
    if parsed.scheme not in ("https", "http"):
        raise RepoValidationError("Only HTTP/HTTPS URLs are supported.")

    if parsed.netloc not in ("github.com", "www.github.com"):
        raise RepoValidationError("Only GitHub repositories are supported.")

    match = GITHUB_REPO_PATTERN.match(repo_url)
    if not match:
        raise RepoValidationError(
            "Invalid GitHub repository URL. Expected format: https://github.com/owner/repo"
        )

    owner = match.group("owner")
    name = match.group("name")

    if len(owner) > 100 or len(name) > 100:
        raise RepoValidationError("Repository owner or name exceeds maximum length.")

    normalized_url = f"https://github.com/{owner}/{name}"

    return ParsedRepoURL(owner=owner, name=name, url=normalized_url)