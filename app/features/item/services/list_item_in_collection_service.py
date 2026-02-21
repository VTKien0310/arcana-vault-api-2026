from typing import Annotated
from fastapi import Depends
from app.features.authentication.entities import User
from app.features.item.entities import ItemRepositoryDep, Item
from app.http.request import SortCondition
from app.ports import SupabasePortDep


class ListItemInCollectionService:
    def __init__(self, spb_port: SupabasePortDep, item_repository: ItemRepositoryDep):
        self.__spb_port = spb_port
        self.__item_repository = item_repository

    def handle(
        self,
        user: User,
        collection: str = "",
        offset: int = 0,
        sort_condition: SortCondition = None,
        limit: int = 100,
    ) -> list[Item]:
        path = user.id

        if collection != "":
            path += f"/{collection}"

        sort_by = (
            {"column": "created_at", "order": "desc"}
            if sort_condition is None
            else {
                "column": sort_condition["field"],
                "order": "desc" if sort_condition["desc"] else "asc",
            }
        )

        list_results = self.__spb_port.storage_vault().list(
            path,
            {
                "limit": limit,
                "offset": offset,
                "sortBy": sort_by,
            },
        )

        return self.__item_repository.items_from_spb_list(list_results)


ListItemInCollectionServiceDep = Annotated[ListItemInCollectionService, Depends()]
