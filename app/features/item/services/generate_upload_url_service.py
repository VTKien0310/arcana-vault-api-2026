from typing import Annotated
from fastapi import Depends

from app.core import AppException
from app.features.item.entities import CollectionRepositoryDep
from app.features.authentication.entities import User
from app.features.item.services import GetItemByNameInCollectionServiceDep
from app.ports import SupabasePortDep


class GenerateUploadUrlService:
    def __init__(
        self,
        spb_port: SupabasePortDep,
        collection_repository: CollectionRepositoryDep,
        get_item_by_name_in_collection_service: GetItemByNameInCollectionServiceDep,
    ):
        self.__spb_port = spb_port
        self.__collection_repository = collection_repository
        self.__get_item_by_name_in_collection_service = (
            get_item_by_name_in_collection_service
        )

    def handle(self, user: User, filename: str, folder: str) -> dict[str, str]:
        path = self.__make_file_path(user, filename, folder)

        has_name_duplication = (
            self.__get_item_by_name_in_collection_service.handle(
                user.id, filename, folder
            )
            is not None
        )
        if has_name_duplication:
            raise AppException(
                status_code=409,
                code="item_name_duplication",
                message="Item with the same name already exists in the collection",
            )

        return self.__spb_port.storage_vault().create_signed_upload_url(path)

    def __make_file_path(self, user: User, filename: str, folder: str) -> str:
        if folder == "":
            return f"{user.id}/{filename}"

        self.__collection_repository.find_or_create(folder, user.id)

        return f"{user.id}/{folder}/{filename}"


GenerateUploadUrlServiceDep = Annotated[GenerateUploadUrlService, Depends()]
