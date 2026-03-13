import logging
from pathlib import Path
from backend.app.pipeline.file_indexer.language_detector import LanguageDetector

logger = logging.getLogger(__name__)


class FileRegistryError(Exception):
    pass


class FileRegistry:
    def __init__(self, language_detector: LanguageDetector | None = None):
        self._detector = language_detector or LanguageDetector()

    def build_registry(self, files: list[dict]) -> list[dict]:
        if not files:
            logger.warning("build_registry called with empty file list.")
            return []

        registry = []

        for entry in files:
            try:
                record = self._build_record(entry)
            except (KeyError, TypeError) as e:
                logger.warning("Skipping malformed file entry %s: %s", entry, e)
                continue

            registry.append(record)

        logger.info("Built file registry with %d records.", len(registry))
        return registry

    def _build_record(self, entry: dict) -> dict:
        raw_path = entry["path"]
        extension = entry["extension"]
        size = entry["size"]

        filename = Path(raw_path).name
        language = self._detector.detect_language(
            extension=extension,
            filename=filename,
        )

        return {
            "path": self._normalize_path(raw_path),
            "extension": extension,
            "language": language,
            "size": size,
        }

    @staticmethod
    def _normalize_path(path: str) -> str:
        # Collapse any redundant separators or relative components
        return str(Path(path).as_posix())