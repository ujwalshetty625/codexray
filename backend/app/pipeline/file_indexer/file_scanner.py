import logging
from pathlib import Path

logger = logging.getLogger(__name__)

IGNORED_DIRS = {
    ".git",
    ".github",
    ".idea",
    ".vscode",
    "__pycache__",
    "node_modules",
    "venv",
    ".venv",
    "env",
    ".env",
    "dist",
    "build",
    ".next",
    ".nuxt",
    "coverage",
    ".pytest_cache",
    ".mypy_cache",
    "eggs",
    ".eggs",
    "*.egg-info",
}

IGNORED_EXTENSIONS = {
    ".pyc",
    ".pyo",
    ".pyd",
    ".so",
    ".dll",
    ".class",
    ".lock",
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".svg",
    ".ico",
    ".woff",
    ".woff2",
    ".ttf",
    ".eot",
    ".mp4",
    ".mp3",
    ".zip",
    ".tar",
    ".gz",
}

MAX_FILE_SIZE_BYTES = 5 * 1024 * 1024  # 5MB


class FileScanError(Exception):
    pass


class FileScanner:
    def __init__(
        self,
        ignored_dirs: set[str] | None = None,
        ignored_extensions: set[str] | None = None,
        max_file_size: int = MAX_FILE_SIZE_BYTES,
    ):
        self._ignored_dirs = ignored_dirs or IGNORED_DIRS
        self._ignored_extensions = ignored_extensions or IGNORED_EXTENSIONS
        self._max_file_size = max_file_size

    def scan_repository(self, repo_path: Path) -> list[dict]:
        if not repo_path.exists():
            raise FileScanError(f"Repository path does not exist: {repo_path}")
        if not repo_path.is_dir():
            raise FileScanError(f"Expected a directory, got: {repo_path}")

        results = []

        for entry in self._walk(repo_path):
            try:
                size = entry.stat().st_size
            except OSError:
                logger.warning("Could not stat file, skipping: %s", entry)
                continue

            if size > self._max_file_size:
                logger.debug("Skipping oversized file (%d bytes): %s", size, entry)
                continue

            results.append({
                "path": str(entry.relative_to(repo_path)),
                "size": size,
                "extension": entry.suffix.lower(),
            })

        logger.info("Scanned %d files in %s", len(results), repo_path)
        return results

    def _walk(self, root: Path):
        for entry in root.iterdir():
            if entry.is_dir():
                if self._is_ignored_dir(entry):
                    logger.debug("Skipping directory: %s", entry.name)
                    continue
                yield from self._walk(entry)
            elif entry.is_file():
                if entry.suffix.lower() in self._ignored_extensions:
                    continue
                yield entry

    def _is_ignored_dir(self, path: Path) -> bool:
        name = path.name
        if name in self._ignored_dirs:
            return True
        # catch patterns like *.egg-info
        return any(
            name.endswith(pattern.lstrip("*"))
            for pattern in self._ignored_dirs
            if pattern.startswith("*")
        )