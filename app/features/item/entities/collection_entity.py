from app.data import DbRepository, Collection
from typing import Annotated
from fastapi import Depends
from sqlmodel import select


class CollectionRepository(DbRepository):
    def find_or_create(self, name: str, user_id: str) -> Collection:
        statement = (
            select(Collection)
            .where(Collection.name == name, Collection.user_id == user_id)
            .limit(1)
        )
        collection = self._db_session.exec(statement).first()

        if collection is None:
            collection = Collection(name=name, user_id=user_id)
            self._db_session.add(collection)
            self._db_session.commit()
            self._db_session.refresh(collection)

        return collection

    def list_by_user_id(self, user_id: str) -> list[Collection]:
        statement = (
            select(Collection)
            .where(Collection.user_id == user_id)
            .order_by(Collection.name)
        )
        collections = self._db_session.exec(statement).all()
        return list(collections)


CollectionRepositoryDep = Annotated[CollectionRepository, Depends()]
