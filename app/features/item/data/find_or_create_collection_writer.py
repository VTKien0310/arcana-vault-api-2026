from typing import Annotated
from fastapi import Depends
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.database import Collection


class FindOrCreateCollectionWriter:
    @classmethod
    async def handle(
        cls, db_session: AsyncSession, name: str, user_id: str
    ) -> Collection:
        statement = (
            select(Collection)
            .where(Collection.name == name, Collection.user_id == user_id)
            .limit(1)
        )
        result = await db_session.exec(statement)
        collection = result.first()

        if collection is None:
            collection = Collection(name=name, user_id=user_id)
            db_session.add(collection)
            await db_session.commit()
            await db_session.refresh(collection)

        return collection


FindOrCreateCollectionWriterDep = Annotated[FindOrCreateCollectionWriter, Depends()]
