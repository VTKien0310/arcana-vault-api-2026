from app.data import DbRepository, Key
from datetime import datetime, timezone
from typing import Annotated
from fastapi import Depends
from enum import Enum
from sqlmodel import select


class KeyChannel(Enum):
    EMAIL = 0
    TELEGRAM = 1
    SMS = 2


class KeyRepository(DbRepository):
    async def update(self, key: Key) -> Key:
        key.updated_at = datetime.now(timezone.utc)

        self._db_session.add(key)
        await self._db_session.commit()
        await self._db_session.refresh(key)

        return key

    async def find_by_user_id(self, user_id: str) -> Key | None:
        statement = select(Key).where(Key.user_id == user_id).limit(1)
        result = await self._db_session.exec(statement)

        return result.first()


KeyRepositoryDep = Annotated[KeyRepository, Depends()]
