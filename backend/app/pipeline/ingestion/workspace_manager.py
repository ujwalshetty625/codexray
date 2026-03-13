import shutil
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

DEFAULT_WORKSPACE_ROOT = Path("/workspace/repos")


class WorkspaceError(Exception):
    pass


class WorkspaceManager:
    def __init__(self, workspace_root: Path = DEFAULT_WORKSPACE_ROOT):
        self._root = workspace_root

    def get_workspace_root(self) -> Path:
        return self._root

    def get_repo_workspace(self, repo_id: str) -> Path:
        if not repo_id or not repo_id.strip():
            raise WorkspaceError("repo_id must be a non-empty string.")
        return self._root / repo_id

    def ensure_repo_workspace(self, repo_id: str) -> Path:
        repo_dir = self.get_repo_workspace(repo_id)

        try:
            repo_dir.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            raise WorkspaceError(
                f"Failed to create workspace for repo '{repo_id}': {e}"
            ) from e

        logger.debug("Workspace ready at %s", repo_dir)
        return repo_dir

    def cleanup_repo_workspace(self, repo_id: str) -> None:
        repo_dir = self.get_repo_workspace(repo_id)

        if not repo_dir.exists():
            logger.debug("Workspace for repo '%s' does not exist, skipping cleanup.", repo_id)
            return

        try:
            shutil.rmtree(repo_dir)
            logger.info("Removed workspace for repo '%s'.", repo_id)
        except OSError as e:
            raise WorkspaceError(
                f"Failed to remove workspace for repo '{repo_id}': {e}"
            ) from e