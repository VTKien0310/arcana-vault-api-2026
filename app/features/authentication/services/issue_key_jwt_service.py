from datetime import datetime, timezone
from typing import Annotated, TypedDict

import jwt
from fastapi import Depends, status

from app.core import AppException
from app.core.config import settings
from .get_user_key_service import GetUserKeyServiceDep


class KeyJwtPayload(TypedDict):
    sub: str
    iat: datetime
    exp: datetime
    kid: str


class IssueKeyJwtService:
    def __init__(self, get_user_key_service: GetUserKeyServiceDep):
        self.__get_user_key_service = get_user_key_service

    def handle(self, user_id: str, key_value: str) -> str:
        user_key = self.__get_user_key_service.handle(user_id)

        if user_key.value != key_value:
            raise AppException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                message=f"Invalid key for user with ID {user_id}",
                code="invalid_key_for_user",
            )

        payload: KeyJwtPayload = {
            "sub": user_id,
            "iat": datetime.now(timezone.utc),
            "exp": user_key.expiration,
            "kid": str(user_key.id),
        }

        return jwt.encode(
            payload, settings.JWT_PRIVATE_KEY, algorithm=settings.JWT_ALGORITHM
        )


IssueKeyJwtServiceDep = Annotated[IssueKeyJwtService, Depends()]
