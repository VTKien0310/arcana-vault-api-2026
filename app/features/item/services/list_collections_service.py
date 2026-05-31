from typing import Annotated
from fastapi import Depends
from app.database import Collection, DbSessionManagerDep
from app.features.authentication.entities.user_entity import User
from app.features.item.data import ListCollectionsByUserReaderDep


class ListCollectionsService:
    def __init__(
        self,
        db_session_manager: DbSessionManagerDep,
        list_collections_by_user_reader: ListCollectionsByUserReaderDep,
    ):
        self.__db_session_manager = db_session_manager
        self.__list_collections_by_user_reader = list_collections_by_user_reader

    async def handle(self, user: User) -> list[Collection]:
        async with self.__db_session_manager.session() as db_session:
            return await self.__list_collections_by_user_reader.handle(
                db_session, user.id
            )


ListCollectionsServiceDep = Annotated[ListCollectionsService, Depends()]
