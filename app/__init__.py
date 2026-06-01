from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastapi import FastAPI
from .core import bootstrap_application
from .database import get_db_session_manager
from .http import router_registry


@asynccontextmanager
async def lifespan_handler(app: FastAPI) -> AsyncGenerator[None, None]:
    app.state.db_session_manager = get_db_session_manager()

    yield

    # dispose the db session to prevent stray connections, this won't be needed for most cases, but it's good practice
    await app.state.db_session_manager.dispose()


def create_app() -> FastAPI:
    return bootstrap_application(
        router_registry=router_registry, lifespan_handler=lifespan_handler
    )
