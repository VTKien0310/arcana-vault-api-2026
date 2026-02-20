from typing import Annotated
import jwt
from fastapi import Depends, Request, status

from app.core import AppException
from app.core.config import settings
from app.features.authentication.services import KeyJwtPayload


def decode_secret_jwt(request: Request) -> KeyJwtPayload:
    token = request.headers.get("X-SECRET-JWT")

    if not token:
        raise AppException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            message="Missing X-SECRET-JWT header",
            code="missing_secret_jwt_header",
        )

    try:
        payload = jwt.decode(
            token,
            settings.JWT_PUBLIC_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )
        return payload
    except jwt.ExpiredSignatureError as exc:
        raise AppException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            message="JWT has expired",
            code="jwt_expired",
        ) from exc
    except jwt.InvalidTokenError as exc:
        raise AppException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            message="Invalid JWT",
            code="invalid_jwt",
        ) from exc


SecretJwtGuardDep = Depends(decode_secret_jwt)
SecretJwtPayloadDep = Annotated[KeyJwtPayload, Depends(decode_secret_jwt)]
