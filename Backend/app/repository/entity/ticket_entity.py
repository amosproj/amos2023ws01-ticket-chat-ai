from typing import TypedDict

from bson import ObjectId

from app.repository.entity.attachment_entity import AttachmentEntity
from app.enum.customer_prio import CustomerPrio
from app.enum.prio import Prio


class TicketEntity(TypedDict):
    _id: ObjectId
    title: str
    service: str
    category: str
    keywords: list
    customerPriority: CustomerPrio
    affectedPerson: str
    description: str
    priority: Prio
    attachments: list[AttachmentEntity]
    requestType: str
