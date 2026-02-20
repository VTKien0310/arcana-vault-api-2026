from typing import Annotated
from fastapi import Depends
from app.features.user.entities import User
from app.ports import SupabasePortDep


class ListItemInCollectionService:
    def __init__(self, spb_port: SupabasePortDep):
        self.__spb_port = spb_port

    def handle(self, user: User, collection: str, offset: int = 0, limit: int = 100):
        path = user.id

        if collection != "":
            path += f"/{collection}"

        return self.__spb_port.storage_vault().list(
            path,
            {
                "limit": limit,
                "offset": offset,
                "sortBy": {"column": "created_at", "order": "desc"},
            },
        )


ListItemInCollectionServiceDep = Annotated[ListItemInCollectionService, Depends()]
