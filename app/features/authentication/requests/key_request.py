from pydantic import BaseModel


class KeyValueRequest(BaseModel):
    value: str
