from typing import Annotated
from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from app.database import Key
from datetime import datetime, timezone


class UpdateKeyWriter:
    @classmethod
    async def handle(cls, db_session: AsyncSession, key: Key) -> Key:
        key.updated_at = datetime.now(timezone.utc)

        db_session.add(key)
        await db_session.commit()
        await db_session.refresh(key)

        return key


UpdateKeyWriterDep = Annotated[UpdateKeyWriter, Depends()]
