from typing import Annotated
from fastapi import Depends, HTTPException, status
from app.database import DbSessionManagerDep
from app.features.authentication.data import FindByUserIdReaderDep
from app.database import Key


class GetUserKeyService:
    def __init__(
        self,
        db_session_manager: DbSessionManagerDep,
        find_by_user_id_reader: FindByUserIdReaderDep,
    ):
        self.__db_session_manager = db_session_manager
        self.__find_by_user_id_reader = find_by_user_id_reader

    async def handle(self, user_id: str) -> Key:
        async with self.__db_session_manager.session() as db_session:
            key = await self.__find_by_user_id_reader.handle(db_session, user_id)

        if key is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Cannot find key for user with ID {user_id}",
            )

        return key


GetUserKeyServiceDep = Annotated[GetUserKeyService, Depends()]
