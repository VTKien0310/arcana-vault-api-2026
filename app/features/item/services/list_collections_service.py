from typing import Annotated
from fastapi import Depends
from app.data import Collection
from app.features.authentication.entities.user_entity import User
from app.features.item.entities import (
    CollectionRepositoryDep,
)


class ListCollectionsService:
    def __init__(self, collection_repository: CollectionRepositoryDep):
        self.__collection_repository = collection_repository

    async def handle(self, user: User) -> list[Collection]:
        return await self.__collection_repository.list_by_user_id(user.id)


ListCollectionsServiceDep = Annotated[ListCollectionsService, Depends()]
