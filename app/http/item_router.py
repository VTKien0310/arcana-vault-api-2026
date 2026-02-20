from fastapi import APIRouter
from app.features.authentication.guards import (
    CurrentAuthenticatedUserDep,
    AuthenticatedGuardDep,
    SecretJwtGuardDep,
)
from app.features.item.requests import ItemRequest
from app.features.item.services import (
    GenerateUploadUrlServiceDep,
    ListItemInCollectionServiceDep,
)

router = APIRouter(
    prefix="/items",
    tags=["item"],
    dependencies=[AuthenticatedGuardDep, SecretJwtGuardDep],
)


@router.post("/upload-url")
async def generate_upload_url(
    request: ItemRequest,
    current_user: CurrentAuthenticatedUserDep,
    generate_upload_url_service: GenerateUploadUrlServiceDep,
):
    signed_url = generate_upload_url_service.handle(
        current_user, request.item, request.collection
    )

    return {
        "url": signed_url["signedUrl"],
        "path": signed_url["path"],
        "token": signed_url["token"],
    }


@router.get("/")
async def list_items(
    current_user: CurrentAuthenticatedUserDep,
    list_item_in_collection_service: ListItemInCollectionServiceDep,
):
    items = list_item_in_collection_service.handle(current_user)

    return items
