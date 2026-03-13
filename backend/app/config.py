import os
from dataclasses import dataclass
from typing import List, Optional

from dotenv import load_dotenv

load_dotenv()

DEFAULT_DATABASE_URL = "postgresql+asyncpg://postgres:post123@127.0.0.1:5432/codexray"


@dataclass(frozen=True)
class Settings:
    DATABASE_URL: str
    WORKSPACE_ROOT: str
    GITHUB_TOKEN: Optional[str]
    ENV: str
    LOG_LEVEL: str
    ALLOWED_ORIGINS: List[str]


def _load_settings() -> Settings:
    database_url = os.environ.get("DATABASE_URL", DEFAULT_DATABASE_URL)
    allowed_origins_raw = os.environ.get("ALLOWED_ORIGINS", "*")
    allowed_origins = [
        origin.strip() for origin in allowed_origins_raw.split(",") if origin.strip()
    ]

    return Settings(
        DATABASE_URL=database_url,
        WORKSPACE_ROOT=os.environ.get("WORKSPACE_ROOT", "/workspace/repos"),
        GITHUB_TOKEN=os.environ.get("GITHUB_TOKEN"),
        ENV=os.environ.get("ENV", "development"),
        LOG_LEVEL=os.environ.get("LOG_LEVEL", "INFO"),
        ALLOWED_ORIGINS=allowed_origins,
    )


settings = _load_settings()