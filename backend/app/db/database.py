from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from backend.app.config import settings


class Base(DeclarativeBase):
    pass


engine: AsyncEngine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
)


async def init_db() -> None:
    import backend.app.models.repository  # noqa: F401
    import backend.app.models.analysis_job  # noqa: F401
    import backend.app.models.file_record  # noqa: F401
    import backend.app.models.dependency  # noqa: F401
    import backend.app.models.architecture  # noqa: F401

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)