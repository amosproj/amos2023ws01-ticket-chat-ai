from typing import TypedDict

from bson import ObjectId


class ValidCategoryEntity(TypedDict):
    _id: ObjectId
    name: str
