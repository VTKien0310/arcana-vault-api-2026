from typing import Annotated
from fastapi import Depends
from sqlmodel import Session, SQLModel, create_engine
from sqlalchemy.engine import URL
from app.core.config import settings

_engine = create_engine(
    URL.create(
        drivername="postgresql",
        username=settings.DB_USER,
        password=settings.DB_PASSWORD,
        host=settings.DB_HOST,
        port=settings.DB_PORT,
        database=settings.DB_NAME,
    ),
    pool_pre_ping=True,
)


def create_db_and_tables():
    SQLModel.metadata.create_all(_engine)


def _get_db_session():
    with Session(_engine) as session:
        yield session


DbSessionDep = Annotated[Session, Depends(_get_db_session)]
