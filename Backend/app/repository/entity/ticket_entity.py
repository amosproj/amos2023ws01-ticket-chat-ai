from typing import TypedDict

from bson import ObjectId

from app.repository.entity.attachment_entity import AttachmentEntity
from app.enum.customer_prio import CustomerPrio
from app.enum.prio import Prio
from app.enum.location import Location
from app.enum.service import ServiceEnum


class TicketEntity(TypedDict):
    _id: ObjectId
    title: str
    service: Location | ServiceEnum
    category: str
    keywords: list
    customerPriority: CustomerPrio
    affectedPerson: str
    description: str
    priority: Prio
    attachments: list[AttachmentEntity]
    requestType: str
