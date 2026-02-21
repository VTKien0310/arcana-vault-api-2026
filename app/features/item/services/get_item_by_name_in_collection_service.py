from typing import Annotated
from fastapi import Depends
from app.features.item.entities import ItemRepositoryDep, Item
from app.ports import SupabasePortDep


class GetItemByNameInCollectionService:
    def __init__(self, spb_port: SupabasePortDep, item_repository: ItemRepositoryDep):
        self.__spb_port = spb_port
        self.__item_repository = item_repository

    def handle(self, user_id: str, item_name: str, collection: str = "") -> Item | None:
        path = user_id
        if collection != "":
            path += f"/{collection}"
        path += f"/{item_name}"

        list_result = self.__spb_port.storage_vault().list(
            path,
            {
                "limit": 1,
                "offset": 0,
            },
        )

        if len(list_result) == 0:
            return None

        return self.__item_repository.item_from_spb_list(list_result[0])


GetItemByNameInCollectionServiceDep = Annotated[
    GetItemByNameInCollectionService, Depends()
]
