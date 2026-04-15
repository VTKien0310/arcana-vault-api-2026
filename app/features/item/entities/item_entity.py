from datetime import datetime
from typing import Annotated, Any
from fastapi import Depends
from pydantic import BaseModel


class Item(BaseModel):
    # Expect the fields type-hinted as None to be None for directories. Yes, Supabase's directory has a None for id.
    id: str | None
    name: str
    created_at: datetime | None
    updated_at: datetime | None
    last_accessed_at: datetime | None
    size: int | None
    mime_type: str | None


class ItemRepository:
    @classmethod
    def item_from_spb_list(cls, item_dict: dict[str, Any]) -> Item:
        metadata = item_dict.get("metadata", {})
        return Item(
            id=item_dict["id"],
            name=item_dict["name"],
            created_at=datetime.fromisoformat(item_dict["created_at"])
            if item_dict["created_at"] is not None
            else None,
            updated_at=datetime.fromisoformat(item_dict["updated_at"])
            if item_dict["updated_at"] is not None
            else None,
            last_accessed_at=datetime.fromisoformat(item_dict["last_accessed_at"])
            if item_dict["last_accessed_at"] is not None
            else None,
            size=metadata.get("size") if metadata is not None else None,
            mime_type=metadata.get("mimetype") if metadata is not None else None,
        )

    @classmethod
    def items_from_spb_list(cls, items_dict: list[dict[str, Any]]) -> list[Item]:
        return [cls.item_from_spb_list(item) for item in items_dict]


ItemRepositoryDep = Annotated[ItemRepository, Depends()]
