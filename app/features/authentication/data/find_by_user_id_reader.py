from typing import Annotated
from fastapi import Depends
from sqlmodel import select
from app.database import Key
from sqlmodel.ext.asyncio.session import AsyncSession


class FindByUserIdReader:
    @classmethod
    async def handle(cls, db_session: AsyncSession, user_id: str) -> Key | None:
        statement = select(Key).where(Key.user_id == user_id).limit(1)
        result = await db_session.exec(statement)

        return result.first()


FindByUserIdReaderDep = Annotated[FindByUserIdReader, Depends()]
