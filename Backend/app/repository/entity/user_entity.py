from typing import TypedDict, Optional

from bson import ObjectId


class UserEntity(TypedDict):
    _id: ObjectId
    first_name: Optional[str]
    family_name: Optional[str]
    email_address: str
    location: str
    password: str
    ticket_ids: list
