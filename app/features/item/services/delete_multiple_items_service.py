from typing import Annotated
from fastapi import Depends

from app.ports import SupabasePortDep


class DeleteMultipleItemsService:
    def __init__(self, spb_port: SupabasePortDep):
        self.__spb_port = spb_port

    def handle(self, items: list[str]):
        self.__spb_port.storage_vault().remove(items)


DeleteMultipleItemsServiceDep = Annotated[DeleteMultipleItemsService, Depends()]
