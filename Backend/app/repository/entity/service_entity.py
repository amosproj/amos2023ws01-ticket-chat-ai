from typing import TypedDict

from bson import ObjectId


class ServiceEntity(TypedDict):
    _id: ObjectId
    service_name: str
    safe_keywords: list[str]
    hint_keywords: list[str]
