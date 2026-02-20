from typing import Annotated

from fastapi import Depends

from app.features.item.entities import CollectionRepositoryDep
from app.features.user.entities import User
from app.ports import SupabasePortDep


class GenerateUploadUrlService:
    def __init__(
        self, spb_port: SupabasePortDep, collection_repository: CollectionRepositoryDep
    ):
        self.__spb_port = spb_port
        self.__collection_repository = collection_repository

    def handle(self, user: User, filename: str, folder: str) -> dict[str, str]:
        if folder == "":
            path = f"{user.id}/{filename}"
        else:
            self.__collection_repository.find_or_create(folder, user.id)
            path = f"{user.id}/{folder}/{filename}"

        return self.__spb_port.storage_vault().create_signed_upload_url(path)


GenerateUploadUrlServiceDep = Annotated[GenerateUploadUrlService, Depends()]
