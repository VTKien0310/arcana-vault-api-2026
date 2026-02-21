from pydantic import BaseModel, Field


class ItemRequest(BaseModel):
    item: str = Field(pattern=r"^[^/\\]*$")
    collection: str = Field(default="", pattern=r"^[^/\\]*$")
