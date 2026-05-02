from pydantic import BaseModel, Field


class ItemRequest(BaseModel):
    item: str = Field(pattern=r"^[^/\\]*$")
    collection: str = Field(default="", pattern=r"^[^/\\]*$")


class ItemDeleteMultipleRequest(BaseModel):
    items: list[str] = Field(min_length=1)
    collection: str = Field(default="", pattern=r"^[^/\\]*$")
