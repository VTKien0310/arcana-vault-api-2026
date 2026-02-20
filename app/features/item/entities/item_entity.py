from datetime import datetime
from typing import Annotated, Any
from fastapi import Depends
from pydantic import BaseModel


class Item(BaseModel):
    id: str
    name: str
    description: str
    created_at: datetime
    updated_at: datetime
    last_accessed_at: datetime


class ItemRepository:
    @classmethod
    def item_from_spb_list(cls, item_dict: dict[str, Any]) -> Item:
        return Item(
            id=item_dict["id"],
            name=item_dict["name"],
            description=item_dict["description"],
            created_at=datetime.fromisoformat(item_dict["created_at"]),
            updated_at=datetime.fromisoformat(item_dict["updated_at"]),
            last_accessed_at=datetime.fromisoformat(item_dict["last_accessed_at"]),
        )

    @classmethod
    def items_from_spb_list(cls, items_dict: list[dict[str, Any]]) -> list[Item]:
        return [cls.item_from_spb_list(item) for item in items_dict]


ItemRepositoryDep = Annotated[ItemRepository, Depends()]
