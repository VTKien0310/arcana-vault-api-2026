from typing import Annotated
from fastapi import Depends, HTTPException, status
from app.features.authentication.entities import KeyRepositoryDep
from app.database import Key


class GetUserKeyService:
    def __init__(self, key_repository: KeyRepositoryDep):
        self.__key_repository = key_repository

    async def handle(self, user_id: str) -> Key:
        key = await self.__key_repository.find_by_user_id(user_id)
        if key is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Cannot find key for user with ID {user_id}",
            )

        return key


GetUserKeyServiceDep = Annotated[GetUserKeyService, Depends()]
