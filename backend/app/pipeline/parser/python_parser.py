import ast
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class PythonParser:
    def parse_file(self, file_path: Path) -> list[str]:
        try:
            source = file_path.read_text(encoding="utf-8", errors="ignore")
        except OSError as e:
            logger.warning("Could not read file %s: %s", file_path, e)
            return []

        try:
            tree = ast.parse(source, filename=str(file_path))
        except SyntaxError as e:
            logger.warning("Syntax error in %s at line %s: %s", file_path, e.lineno, e.msg)
            return []
        except ValueError as e:
            logger.warning("Could not parse %s: %s", file_path, e)
            return []

        return self._extract_imports(tree)

    def extract_dependencies(self, file_path: str, source_code: str) -> list[dict]:
        try:
            tree = ast.parse(source_code, filename=file_path)
        except (SyntaxError, ValueError) as e:
            logger.warning("Could not parse %s: %s", file_path, e)
            return []

        imports = self._extract_imports(tree)
        return [{"module": mod} for mod in imports]

    def _extract_imports(self, tree: ast.AST) -> list[str]:
        imports = []

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)

            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.append(node.module)

        return imports