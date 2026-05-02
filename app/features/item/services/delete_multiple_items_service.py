from typing import Annotated
from fastapi import Depends

from app.features.authentication.entities import User
from app.ports import SupabasePortDep


class DeleteMultipleItemsService:
    def __init__(self, spb_port: SupabasePortDep):
        self.__spb_port = spb_port

    def handle(self, user: User, items: list[str], collection: str = "") -> int:
        processed_items = [
            f"{user.id}/{collection}/{item}" for item in items
        ] if collection != "" else [
            f"{user.id}/{item}" for item in items
        ]

        return len(self.__spb_port.storage_vault().remove(processed_items))


DeleteMultipleItemsServiceDep = Annotated[DeleteMultipleItemsService, Depends()]
