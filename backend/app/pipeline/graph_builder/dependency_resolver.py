import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class DependencyResolver:
    def __init__(self, repo_files: list[str]):
        self._index = self._build_index(repo_files)

    def resolve_import(self, import_name: str, repo_files: list[str] | None = None) -> str | None:
        # dotted import → path candidates: "utils.helpers" → "utils/helpers"
        as_path = import_name.replace(".", "/")

        candidates = [
            f"{as_path}.py",
            f"{as_path}/__init__.py",
            f"src/{as_path}.py",
            f"src/{as_path}/__init__.py",
            f"lib/{as_path}.py",
            f"app/{as_path}.py",
            f"app/{as_path}/__init__.py",
        ]

        for candidate in candidates:
            normalized = str(Path(candidate).as_posix())
            if normalized in self._index:
                logger.debug("Resolved '%s' → '%s'", import_name, normalized)
                return normalized

        # Fallback: match by filename stem only
        stem = Path(as_path).name
        fallback = self._index.get(stem)
        if fallback:
            logger.debug("Stem-matched '%s' → '%s'", import_name, fallback)
            return fallback

        logger.debug("Could not resolve import '%s'.", import_name)
        return None

    def _build_index(self, repo_files: list[str]) -> dict[str, str]:
        index: dict[str, str] = {}

        for f in repo_files:
            normalized = str(Path(f).as_posix())
            index[normalized] = normalized

            # Also index by stem for fallback matching
            stem = Path(f).stem
            if stem not in index:
                index[stem] = normalized

        return index