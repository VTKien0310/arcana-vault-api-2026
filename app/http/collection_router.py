from fastapi import APIRouter
from app.data import Collection
from app.features.authentication.guards import (
    CurrentAuthenticatedUserDep,
    AuthenticatedGuardDep,
    SecretJwtGuardDep,
)
from app.features.item.services import ListCollectionsServiceDep

router = APIRouter(
    prefix="/collections",
    tags=["collection"],
    dependencies=[AuthenticatedGuardDep, SecretJwtGuardDep],
)


@router.get("")
async def list_collections(
    current_user: CurrentAuthenticatedUserDep,
    list_collections_service: ListCollectionsServiceDep,
) -> list[Collection]:
    collections = await list_collections_service.handle(current_user)

    return collections
