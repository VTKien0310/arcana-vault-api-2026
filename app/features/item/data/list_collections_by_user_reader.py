from typing import Annotated
from fastapi import Depends
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.database import Collection


class ListCollectionsByUserReader:
    @classmethod
    async def handle(cls, db_session: AsyncSession, user_id: str) -> list[Collection]:
        statement = (
            select(Collection)
            .where(Collection.user_id == user_id)
            .order_by(Collection.name)
        )
        result = await db_session.exec(statement)
        collections = result.all()
        return list(collections)


ListCollectionsByUserReaderDep = Annotated[ListCollectionsByUserReader, Depends()]
