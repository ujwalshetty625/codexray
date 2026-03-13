import subprocess
import shutil
import logging
from pathlib import Path

from backend.app.pipeline.ingestion.workspace_manager import WorkspaceManager, WorkspaceError

logger = logging.getLogger(__name__)

CLONE_TIMEOUT = 120


class RepoCloneError(Exception):
    pass


class RepositoryCloner:
    def __init__(self, workspace_manager: WorkspaceManager | None = None):
        self._workspace = workspace_manager or WorkspaceManager()

    def clone_repository(self, repo_url: str, repo_id: str) -> str:
        target_dir = self._workspace.get_repo_workspace(repo_id)

        if target_dir.exists():
            logger.info("Removing existing directory before clone: %s", target_dir)
            shutil.rmtree(target_dir)

        cmd = [
            "git", "clone",
            "--depth", "1",
            "--single-branch",
            "--no-tags",
            repo_url,
            str(target_dir),
        ]

        logger.info("Cloning %s into %s", repo_url, target_dir)

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=CLONE_TIMEOUT,
            )
        except subprocess.TimeoutExpired:
            shutil.rmtree(target_dir, ignore_errors=True)
            raise RepoCloneError(f"Clone timed out after {CLONE_TIMEOUT}s for repo '{repo_id}'.")
        except FileNotFoundError:
            raise RepoCloneError("git is not installed or not available in PATH.")

        if result.returncode != 0:
            shutil.rmtree(target_dir, ignore_errors=True)
            raise RepoCloneError(
                f"git clone failed for '{repo_url}':\n{result.stderr.strip()}"
            )

        logger.info("Successfully cloned repo '%s'.", repo_id)
        return str(target_dir)

    def cleanup_repository(self, repo_id: str) -> None:
        self._workspace.cleanup_repo_workspace(repo_id)
