from typing import TypedDict

from bson import ObjectId


class LocationEntity(TypedDict):
    _id: ObjectId
    name: str
