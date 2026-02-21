from typing import Annotated

from fastapi import Depends

from app.features.authentication.entities import User
from app.ports import SupabasePortDep


class GenerateViewUrlService:
    def __init__(self, spb_port: SupabasePortDep):
        self.__spb_port = spb_port

    def handle(self, user: User, filename: str, folder: str) -> str:
        path = (
            f"{user.id}/{filename}"
            if folder is ""
            else f"{user.id}/{folder}/{filename}"
        )

        return self.__spb_port.storage_vault().create_signed_url(path)["signedUrl"]


GenerateViewUrlServiceDep = Annotated[GenerateViewUrlService, Depends()]
