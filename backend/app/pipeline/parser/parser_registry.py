import logging
from typing import Protocol, runtime_checkable

logger = logging.getLogger(__name__)


@runtime_checkable
class LanguageParser(Protocol):
    def extract_dependencies(self, file_path: str, source_code: str) -> list[dict]:
        ...


class ParserRegistry:
    def __init__(self):
        self._parsers: dict[str, LanguageParser] = {}

    def register_parser(self, language: str, parser: LanguageParser) -> None:
        if not isinstance(parser, LanguageParser):
            raise TypeError(
                f"Parser for '{language}' must implement the LanguageParser protocol."
            )

        normalized = self._normalize(language)

        if normalized in self._parsers:
            logger.warning("Overwriting existing parser for language '%s'.", language)

        self._parsers[normalized] = parser
        logger.debug("Registered parser for language '%s'.", language)

    def get_parser(self, language: str) -> LanguageParser | None:
        return self._parsers.get(self._normalize(language))

    def registered_languages(self) -> list[str]:
        return list(self._parsers.keys())

    @staticmethod
    def _normalize(language: str) -> str:
        return language.strip().lower()