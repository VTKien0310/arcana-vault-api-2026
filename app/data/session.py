from abc import ABC
from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends
from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.config import settings


def _make_db_url(drivername: str) -> URL:
    return URL.create(
        drivername=drivername,
        username=settings.DB_USER,
        password=settings.DB_PASSWORD,
        host=settings.DB_HOST,
        port=settings.DB_PORT,
        database=settings.DB_NAME,
    )


def get_db_url() -> URL:
    return _make_db_url("postgresql")


def get_async_db_url() -> URL:
    return _make_db_url("postgresql+asyncpg")


_async_engine = create_async_engine(get_async_db_url(), pool_pre_ping=True)
_async_session_maker = async_sessionmaker(
    _async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def _get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with _async_session_maker() as session:
        yield session


DbSessionDep = Annotated[AsyncSession, Depends(_get_db_session)]


class DbRepository(ABC):
    def __init__(self, db_session: DbSessionDep):
        self._db_session = db_session
