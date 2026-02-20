from pydantic import BaseModel


class ItemRequest(BaseModel):
    item: str
    collection: str = ""
