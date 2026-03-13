EXTENSION_MAP: dict[str, str] = {
    # Python
    ".py": "Python",
    ".pyi": "Python",
    ".pyw": "Python",

    # JavaScript
    ".js": "JavaScript",
    ".mjs": "JavaScript",
    ".cjs": "JavaScript",

    # TypeScript
    ".ts": "TypeScript",
    ".tsx": "TypeScript",

    # JSX
    ".jsx": "JavaScript",

    # Java
    ".java": "Java",

    # Kotlin
    ".kt": "Kotlin",
    ".kts": "Kotlin",

    # Go
    ".go": "Go",

    # Rust
    ".rs": "Rust",

    # C / C++
    ".c": "C",
    ".h": "C",
    ".cpp": "C++",
    ".cc": "C++",
    ".cxx": "C++",
    ".hpp": "C++",
    ".hxx": "C++",

    # C#
    ".cs": "C#",

    # Ruby
    ".rb": "Ruby",
    ".rake": "Ruby",
    ".gemspec": "Ruby",

    # PHP
    ".php": "PHP",

    # Swift
    ".swift": "Swift",

    # Scala
    ".scala": "Scala",
    ".sc": "Scala",

    # R
    ".r": "R",
    ".R": "R",

    # Shell
    ".sh": "Shell",
    ".bash": "Shell",
    ".zsh": "Shell",

    # PowerShell
    ".ps1": "PowerShell",
    ".psm1": "PowerShell",

    # Dart
    ".dart": "Dart",

    # Elixir
    ".ex": "Elixir",
    ".exs": "Elixir",

    # Haskell
    ".hs": "Haskell",
    ".lhs": "Haskell",

    # Lua
    ".lua": "Lua",

    # MATLAB
    ".m": "MATLAB",

    # SQL
    ".sql": "SQL",

    # HTML / CSS
    ".html": "HTML",
    ".htm": "HTML",
    ".css": "CSS",
    ".scss": "SCSS",
    ".sass": "SASS",
    ".less": "LESS",

    # Config / Data
    ".json": "JSON",
    ".yaml": "YAML",
    ".yml": "YAML",
    ".toml": "TOML",
    ".xml": "XML",
    ".env": "ENV",
    ".ini": "INI",
    ".cfg": "INI",

    # Markdown / Docs
    ".md": "Markdown",
    ".mdx": "Markdown",
    ".rst": "reStructuredText",
    ".txt": "Text",

    # Docker / Infra
    ".dockerfile": "Dockerfile",
    ".tf": "Terraform",
    ".hcl": "HCL",
    ".proto": "Protobuf",

    # GraphQL
    ".graphql": "GraphQL",
    ".gql": "GraphQL",
}

FILENAME_MAP: dict[str, str] = {
    "Dockerfile": "Dockerfile",
    "Makefile": "Makefile",
    "Jenkinsfile": "Groovy",
    ".gitignore": "GitIgnore",
    ".dockerignore": "GitIgnore",
}

UNKNOWN = "Unknown"


class LanguageDetector:
    def __init__(
        self,
        extension_map: dict[str, str] | None = None,
        filename_map: dict[str, str] | None = None,
    ):
        self._extensions = extension_map or EXTENSION_MAP
        self._filenames = filename_map or FILENAME_MAP

    def detect_language(self, extension: str, filename: str | None = None) -> str:
        if filename and filename in self._filenames:
            return self._filenames[filename]

        if not extension:
            return UNKNOWN

        return self._extensions.get(extension.lower(), UNKNOWN)