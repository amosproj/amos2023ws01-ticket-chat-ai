from typing import TypedDict


class AttachmentEntity(TypedDict):
    name: str
    type: str
    data: bytes
