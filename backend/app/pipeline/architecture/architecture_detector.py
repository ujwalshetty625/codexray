import logging
from pathlib import Path

from backend.app.pipeline.architecture.architecture_classifier import ArchitectureClassifier

logger = logging.getLogger(__name__)


class ArchitectureDetector:
    def __init__(self, classifier: ArchitectureClassifier | None = None):
        self._classifier = classifier or ArchitectureClassifier()

    def detect_architecture(self, repo_path: Path) -> dict:
        logger.info("Running architecture detection on %s", repo_path)

        result = self._classifier.classify_from_folders(repo_path)

        logger.info(
            "Architecture detected: %s (confidence: %.2f)",
            result["architecture"],
            result["confidence"],
        )

        return result