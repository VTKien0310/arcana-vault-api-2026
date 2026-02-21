from typing import Annotated, TypedDict
from fastapi import Depends, Request


class SortCondition(TypedDict):
    field: str
    desc: bool


class FilterCondition(TypedDict):
    field: str
    value: str


class ListResourceParams(TypedDict):
    offset: int
    limit: int
    sort_conditions: list[SortCondition]
    filter_conditions: list[FilterCondition]


async def resolve_list_resource_params(
    request: Request,
    offset: int = 0,
    limit: int = 100,
    sort: str = "",
) -> ListResourceParams:
    sort_conditions: list[SortCondition] = [
        {"field": s.lstrip("-"), "desc": s.startswith("-")}
        for s in sort.split(",")
        if s
    ]

    raw_filters = {
        key[len("filter[") : -1]: value
        for key, value in request.query_params.multi_items()
        if key.startswith("filter[") and key.endswith("]")
    }
    filter_conditions: list[FilterCondition] = [
        {"field": field, "value": value} for field, value in raw_filters.items()
    ]

    return {
        "offset": offset,
        "limit": limit,
        "sort_conditions": sort_conditions,
        "filter_conditions": filter_conditions,
    }


ListResourceParamsDep = Annotated[
    ListResourceParams, Depends(resolve_list_resource_params)
]
