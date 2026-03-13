import logging
from pathlib import Path

from backend.app.pipeline.parser.parser_registry import ParserRegistry
from backend.app.pipeline.parser.python_parser import PythonParser

logger = logging.getLogger(__name__)


def _build_default_registry() -> ParserRegistry:
    registry = ParserRegistry()
    registry.register_parser("python", PythonParser())
    return registry


class ParserEngine:
    def __init__(self, registry: ParserRegistry | None = None):
        self._registry = registry or _build_default_registry()

    def parse_repository(self, repo_path: Path, file_records: list[dict]) -> dict:
        if not file_records:
            logger.warning("parse_repository called with empty file records.")
            return {}

        results: dict[str, list[str]] = {}
        skipped = 0

        for record in file_records:
            file_path_str = record.get("path")
            language = record.get("language")

            if not file_path_str or not language:
                logger.debug("Skipping incomplete file record: %s", record)
                skipped += 1
                continue

            parser = self._registry.get_parser(language)
            if parser is None:
                logger.debug("No parser registered for language '%s', skipping %s.", language, file_path_str)
                skipped += 1
                continue

            full_path = repo_path / file_path_str

            if not full_path.exists():
                logger.warning("File not found, skipping: %s", full_path)
                skipped += 1
                continue

            imports = parser.parse_file(full_path)

            if imports:
                results[file_path_str] = imports

        logger.info(
            "Parsing complete. Parsed %d files, skipped %d.",
            len(results),
            skipped,
        )

        return results