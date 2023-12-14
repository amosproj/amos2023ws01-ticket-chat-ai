from typing import TypedDict

from bson import ObjectId


class UserEntity(TypedDict):
    _id: ObjectId
    first_name: str
    family_name: str
    email_address: str
    location: str
    password: str
    ticket_ids: list
