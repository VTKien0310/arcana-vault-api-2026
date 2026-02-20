from .models import *
from .session import DbSessionDep, create_db_and_tables
from abc import ABC


class DbRepository(ABC):
    def __init__(self, db_session: DbSessionDep):
        self._db_session = db_session
