from app.database import DbRepository, Collection
from typing import Annotated
from fastapi import Depends
from sqlmodel import select


class CollectionRepository(DbRepository):
    async def find_or_create(self, name: str, user_id: str) -> Collection:
        statement = (
            select(Collection)
            .where(Collection.name == name, Collection.user_id == user_id)
            .limit(1)
        )
        result = await self._db_session.exec(statement)
        collection = result.first()

        if collection is None:
            collection = Collection(name=name, user_id=user_id)
            self._db_session.add(collection)
            await self._db_session.commit()
            await self._db_session.refresh(collection)

        return collection

    async def list_by_user_id(self, user_id: str) -> list[Collection]:
        statement = (
            select(Collection)
            .where(Collection.user_id == user_id)
            .order_by(Collection.name)
        )
        result = await self._db_session.exec(statement)
        collections = result.all()
        return list(collections)


CollectionRepositoryDep = Annotated[CollectionRepository, Depends()]
