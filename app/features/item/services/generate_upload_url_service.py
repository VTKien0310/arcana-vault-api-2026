from typing import Annotated
from fastapi import Depends
from storage3.exceptions import StorageApiError

from app.core import AppException
from app.database import DbSessionManagerDep
from app.features.item.data import FindOrCreateCollectionWriterDep
from app.features.authentication.entities import User
from app.ports import SupabasePortDep


class GenerateUploadUrlService:
    def __init__(
        self,
        spb_port: SupabasePortDep,
        db_session_manager: DbSessionManagerDep,
        find_or_create_collection_writer: FindOrCreateCollectionWriterDep,
    ):
        self.__spb_port = spb_port
        self.__db_session_manager = db_session_manager
        self.__find_or_create_collection_writer = find_or_create_collection_writer

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

        async with self.__db_session_manager.session() as db_session:
            await self.__find_or_create_collection_writer.handle(
                db_session, folder, user.id
            )

        return f"{user.id}/{folder}/{filename}"


GenerateUploadUrlServiceDep = Annotated[GenerateUploadUrlService, Depends()]
