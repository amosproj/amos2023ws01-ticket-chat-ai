from typing import TypedDict

from bson import ObjectId


class CategoryEntity(TypedDict):
    _id: ObjectId
    name: str
