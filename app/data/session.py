from abc import ABC
from typing import Annotated
from fastapi import Depends
from sqlmodel import Session, SQLModel, create_engine
from sqlalchemy.engine import URL
from app.core.config import settings


def get_db_url() -> URL:
    return URL.create(
        drivername="postgresql",
        username=settings.DB_USER,
        password=settings.DB_PASSWORD,
        host=settings.DB_HOST,
        port=settings.DB_PORT,
        database=settings.DB_NAME,
    )


_engine = create_engine(get_db_url(), pool_pre_ping=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(_engine)


def _get_db_session():
    with Session(_engine) as session:
        yield session


DbSessionDep = Annotated[Session, Depends(_get_db_session)]


class DbRepository(ABC):
    def __init__(self, db_session: DbSessionDep):
        self._db_session = db_session
