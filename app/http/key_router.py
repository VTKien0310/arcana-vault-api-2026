from fastapi import APIRouter
from app.features.authentication.guards import (
    CurrentAuthenticatedUserDep,
    AuthenticatedGuardDep,
)
from app.features.authentication.services import (
    IssueKeyJwtServiceDep,
    RefreshUserKeyServiceDep,
)
from app.features.authentication.requests import KeyValueRequest

router = APIRouter(prefix="/key", tags=["key"], dependencies=[AuthenticatedGuardDep])


@router.post("/refresh")
def refresh(
    current_user: CurrentAuthenticatedUserDep,
    refresh_user_key_service: RefreshUserKeyServiceDep,
):
    key = refresh_user_key_service.handle(current_user.id)

    return {"expiration": key.expiration, "channels": key.channels}


@router.post("/submit")
def submit(
    request: KeyValueRequest,
    current_user: CurrentAuthenticatedUserDep,
    issue_key_jwt_service: IssueKeyJwtServiceDep,
):
    jwt = issue_key_jwt_service.handle(current_user.id, request.value)

    return {"secret": jwt}
