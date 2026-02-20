from typing import Annotated
from fastapi import Depends
from app.features.authentication.entities import User
from app.http.request import SortCondition
from app.ports import SupabasePortDep


class ListItemInCollectionService:
    def __init__(self, spb_port: SupabasePortDep):
        self.__spb_port = spb_port

    def handle(
        self,
        user: User,
        collection: str = "",
        offset: int = 0,
        sort_condition: SortCondition = None,
        limit: int = 100,
    ):
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

        return self.__spb_port.storage_vault().list(
            path,
            {
                "limit": limit,
                "offset": offset,
                "sortBy": sort_by,
            },
        )


ListItemInCollectionServiceDep = Annotated[ListItemInCollectionService, Depends()]
