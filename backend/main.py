import logging
import logging.config
from contextlib import asynccontextmanager
from urllib.parse import urlsplit, urlunsplit

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from backend.app.api.router import api_router
from backend.app.config import settings
from backend.app.db.database import engine, init_db


logging.config.dictConfig(
    {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "default",
            },
        },
        "root": {
            "level": settings.LOG_LEVEL,
            "handlers": ["console"],
        },
    }
)

logger = logging.getLogger(__name__)


def _mask_database_url(url: str) -> str:
    parsed = urlsplit(url)
    if not parsed.password:
        return url

    netloc = parsed.hostname or ""
    if parsed.username:
        netloc = f"{parsed.username}:***@{netloc}"
    if parsed.port:
        netloc = f"{netloc}:{parsed.port}"

    return urlunsplit((parsed.scheme, netloc, parsed.path, parsed.query, parsed.fragment))


@asynccontextmanager
async def lifespan(app: FastAPI):
    masked_url = _mask_database_url(settings.DATABASE_URL)
    logger.info("CodeXRay starting up [env=%s]", settings.ENV)
    logger.info("Using database: %s", masked_url)

    await init_db()

    async with engine.begin() as conn:
        await conn.execute(text("SELECT 1"))

    logger.info("Database connection verified and tables ready.")
    yield
    logger.info("CodeXRay shutting down.")
    await engine.dispose()


app = FastAPI(
    title="CodeXRay",
    description="AI-powered codebase intelligence platform.",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)


@app.get("/", tags=["Root"])
async def root():
    return {"service": "CodeXRay", "status": "running"}