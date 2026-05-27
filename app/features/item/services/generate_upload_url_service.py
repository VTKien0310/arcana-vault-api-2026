from typing import Annotated
from fastapi import Depends
from storage3.exceptions import StorageApiError

from app.core import AppException
from app.features.item.entities import CollectionRepositoryDep
from app.features.authentication.entities import User
from app.ports import SupabasePortDep


class GenerateUploadUrlService:
    def __init__(
        self,
        spb_port: SupabasePortDep,
        collection_repository: CollectionRepositoryDep,
    ):
        self.__spb_port = spb_port
        self.__collection_repository = collection_repository

    async def handle(self, user: User, filename: str, folder: str) -> dict[str, str]:
        path = await self.__make_file_path(user, filename, folder)

        try:
            return self.__spb_port.storage_vault().create_signed_upload_url(path)
        except StorageApiError as storage_api_error:
            if storage_api_error.status == 409:
                raise AppException(
                    status_code=409,
                    code="item_path_duplicate",
                    message="Item with this path already exists",
                ) from storage_api_error

            raise storage_api_error

    async def __make_file_path(self, user: User, filename: str, folder: str) -> str:
        if folder == "":
            return f"{user.id}/{filename}"

        await self.__collection_repository.find_or_create(folder, user.id)

        return f"{user.id}/{folder}/{filename}"


GenerateUploadUrlServiceDep = Annotated[GenerateUploadUrlService, Depends()]
