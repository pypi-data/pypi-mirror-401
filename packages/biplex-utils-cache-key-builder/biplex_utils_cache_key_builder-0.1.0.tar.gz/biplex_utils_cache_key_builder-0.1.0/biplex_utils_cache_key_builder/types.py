from typing import TypedDict, Optional


class Cursor(TypedDict, total=False):
    id: str
    created_at: str


class SortItem(TypedDict):
    field: str
    direction: str
