import secrets
from datetime import datetime, timezone, timedelta
from typing import Annotated
from fastapi import Depends
from app.core.config import settings
from app.features.authentication.data import UpdateKeyWriterDep
from app.database import Key, DbSessionManagerDep
from .get_user_key_service import GetUserKeyServiceDep


class RefreshUserKeyService:
    def __init__(
        self,
        get_user_key_service: GetUserKeyServiceDep,
        update_key_writer: UpdateKeyWriterDep,
        db_session_manager: DbSessionManagerDep,
    ):
        self.__get_user_key_service = get_user_key_service
        self.__update_key_writer = update_key_writer
        self.__db_session_manager = db_session_manager

    async def handle(self, user_id: str) -> Key:
        key = await self.__get_user_key_service.handle(user_id)

        if key.expiration > datetime.now(timezone.utc):
            return key

        key.expiration = datetime.now(timezone.utc) + timedelta(
            minutes=settings.KEY_EXPIRATION_MINUTES
        )
        key.value = str(secrets.randbelow(100000000)).zfill(8)

        async with self.__db_session_manager.session() as db_session:
            key = await self.__update_key_writer.handle(db_session, key)

        return key


RefreshUserKeyServiceDep = Annotated[RefreshUserKeyService, Depends()]
