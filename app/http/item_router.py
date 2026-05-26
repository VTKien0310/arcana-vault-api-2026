from fastapi import APIRouter
from app.features.authentication.guards import (
    CurrentAuthenticatedUserDep,
    AuthenticatedGuardDep,
    SecretJwtGuardDep,
)
from app.features.item.entities import Item
from app.features.item.requests import ItemRequest, ItemDeleteMultipleRequest
from app.features.item.services import (
    GenerateUploadUrlServiceDep,
    ListItemInCollectionServiceDep,
    GenerateViewUrlServiceDep,
    DeleteMultipleItemsServiceDep,
)
from app.http.request import ListResourceParamsDep

router = APIRouter(
    prefix="/items",
    tags=["item"],
    dependencies=[AuthenticatedGuardDep, SecretJwtGuardDep],
)


@router.post("/upload-url")
def generate_upload_url(
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


@router.post("/view-url")
def generate_view_url(
    request: ItemRequest,
    current_user: CurrentAuthenticatedUserDep,
    generate_view_url_service: GenerateViewUrlServiceDep,
):
    signed_url = generate_view_url_service.handle(
        current_user, request.item, request.collection
    )

    return {
        "url": signed_url,
    }


@router.post("/delete-multiple")
def delete_multiple(
    request: ItemDeleteMultipleRequest,
    current_user: CurrentAuthenticatedUserDep,
    delete_multiple_items_service: DeleteMultipleItemsServiceDep,
):
    deleted_count = delete_multiple_items_service.handle(
        user=current_user, items=request.items, collection=request.collection
    )

    return {"deleted_count": deleted_count}


@router.get("")
def list_items(
    list_params: ListResourceParamsDep,
    current_user: CurrentAuthenticatedUserDep,
    list_item_in_collection_service: ListItemInCollectionServiceDep,
) -> list[Item]:
    sort_condition = (
        None
        if not list_params["sort_conditions"]
        else list_params["sort_conditions"].pop()
    )

    collection = next(
        (
            f["value"]
            for f in list_params["filter_conditions"]
            if f["field"] == "collection"
        ),
        "",
    )

    items = list_item_in_collection_service.handle(
        current_user, collection=collection, sort_condition=sort_condition
    )

    return items
