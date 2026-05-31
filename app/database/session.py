from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends
from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncEngine
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


async def _get_db_transaction_session() -> AsyncGenerator[AsyncSession, None]:
    async with _async_session_maker() as session:
        async with session.begin():
            yield session


DbTransactionSessionDep = Annotated[AsyncSession, Depends(_get_db_transaction_session)]


class DbSessionManager:
    def __init__(self, engine: AsyncEngine) -> None:
        self._engine = engine
        self._session_maker = async_sessionmaker(
            bind=self._engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )

    @asynccontextmanager
    async def session(self) -> AsyncGenerator[AsyncSession, None]:
        async with self._session_maker() as session:
            yield session

    @asynccontextmanager
    async def transaction(self) -> AsyncGenerator[AsyncSession, None]:
        async with self._session_maker() as session:
            async with session.begin():
                yield session

    async def dispose(self) -> None:
        await self._engine.dispose()


_db_session_manager = DbSessionManager(_async_engine)


def get_db_session_manager() -> DbSessionManager:
    return _db_session_manager


DbSessionManagerDep = Annotated[
    DbSessionManager,
    Depends(get_db_session_manager),
]
