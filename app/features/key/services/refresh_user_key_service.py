import secrets
from datetime import datetime, timezone, timedelta
from typing import Annotated
from fastapi import Depends
from app.core.config import settings
from app.features.key.entities.key_entity import Key, KeyRepositoryDep
from .get_user_key_service import GetUserKeyServiceDep


class RefreshUserKeyService:
    def __init__(
        self,
        key_repository: KeyRepositoryDep,
        get_user_key_service: GetUserKeyServiceDep,
    ):
        self.__key_repository = key_repository
        self.__get_user_key_service = get_user_key_service

    def handle(self, user_id: str) -> Key:
        key = self.__get_user_key_service.handle(user_id)

        if key.expiration > datetime.now(timezone.utc):
            return key

        key.expiration = datetime.now(timezone.utc) + timedelta(
            minutes=settings.KEY_EXPIRATION_MINUTES
        )
        key.value = str(secrets.randbelow(100000000)).zfill(8)

        return self.__key_repository.update(key)


RefreshUserKeyServiceDep = Annotated[RefreshUserKeyService, Depends()]
