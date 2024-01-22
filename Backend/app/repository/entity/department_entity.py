from typing import TypedDict

from bson import ObjectId


class DepartmentEntity(TypedDict):
    _id: ObjectId
    name: str
