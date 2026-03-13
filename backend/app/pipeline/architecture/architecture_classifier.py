import logging
from pathlib import Path

logger = logging.getLogger(__name__)

UNKNOWN_RESULT = {"architecture": "Unknown", "confidence": 0.0}


FOLDER_PATTERNS = [
    (
        "MVC",
        0.9,
        [["models", "views", "controllers"], ["models", "views", "templates"]],
    ),
    (
        "Layered",
        0.85,
        [["service", "repository", "controller"], ["services", "repositories", "controllers"]],
    ),
    (
        "Microservices",
        0.85,
        [["services", "gateway"], ["services", "broker"], ["services", "consumer"]],
    ),
    (
        "Serverless",
        0.85,
        [["functions", "handlers"], ["lambdas", "handlers"]],
    ),
    (
        "Event-Driven",
        0.8,
        [["events", "listeners"], ["publishers", "consumers"], ["events", "handlers"]],
    ),
]

MONOLITHIC_FOLDERS = {"app", "core", "common", "shared", "utils", "src", "lib"}


class ArchitectureClassifier:
    def classify_from_folders(self, repo_path: Path) -> dict:
        try:
            folders = self._get_top_level_folders(repo_path)
        except OSError as e:
            logger.warning("Could not read repo directory: %s", e)
            return UNKNOWN_RESULT

        if not folders:
            return UNKNOWN_RESULT

        logger.debug("Top-level folders: %s", folders)

        for pattern_name, confidence, signal_groups in FOLDER_PATTERNS:
            for group in signal_groups:
                if all(f in folders for f in group):
                    logger.info("Matched pattern '%s' via folders %s.", pattern_name, group)
                    return {"architecture": pattern_name, "confidence": confidence}

        # Partial match — score by how many known layer folders are present
        layered_hits = sum(1 for f in ["service", "services", "repository", "repositories", "controller", "controllers"] if f in folders)
        if layered_hits >= 2:
            return {"architecture": "Layered", "confidence": round(0.5 + layered_hits * 0.08, 2)}

        mvc_hits = sum(1 for f in ["models", "views", "templates", "controllers"] if f in folders)
        if mvc_hits >= 2:
            return {"architecture": "MVC", "confidence": round(0.5 + mvc_hits * 0.08, 2)}

        monolithic_hits = sum(1 for f in folders if f in MONOLITHIC_FOLDERS)
        if monolithic_hits >= 1:
            return {"architecture": "Monolithic", "confidence": round(0.4 + monolithic_hits * 0.05, 2)}

        return UNKNOWN_RESULT

    @staticmethod
    def _get_top_level_folders(repo_path: Path) -> set[str]:
        return {
            entry.name.lower()
            for entry in repo_path.iterdir()
            if entry.is_dir() and not entry.name.startswith(".")
        }