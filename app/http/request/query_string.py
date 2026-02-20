from typing import Annotated, TypedDict
from fastapi import Depends


class SortCondition(TypedDict):
    field: str
    desc: bool


class ListResourceParams(TypedDict):
    offset: int
    limit: int
    sort_conditions: list[SortCondition]


async def resolve_list_resource_params(
    offset: int = 0, limit: int = 100, sort: str = ""
) -> ListResourceParams:
    sort_conditions: list[SortCondition] = [
        {"field": s.lstrip("-"), "desc": s.startswith("-")}
        for s in sort.split(",")
        if s
    ]
    return {"offset": offset, "limit": limit, "sort_conditions": sort_conditions}


ListResourceParamsDep = Annotated[
    ListResourceParams, Depends(resolve_list_resource_params)
]
