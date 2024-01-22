from bson import ObjectId
from pydantic import BaseModel

from app.enum.customer_prio import CustomerPrio
from app.enum.prio import Prio
from app.enum.location import Location
from app.enum.service import ServiceEnum


class Ticket(BaseModel):
    id: str = ""
    title: str
    service: Location | ServiceEnum
    category: str
    keywords: list
    customerPriority: CustomerPrio
    affectedPerson: str
    description: str
    priority: Prio
    requestType: str
    attachmentNames: list[str] = []
