from bson import ObjectId
from pydantic import BaseModel

from app.enum.customer_prio import CustomerPrio
from app.enum.prio import Prio


class Ticket(BaseModel):
    id: str = ""
    title: str
    service: str
    category: str
    keywords: list
    customerPriority: CustomerPrio
    affectedPerson: str
    description: str
    priority: Prio
    requestType: str
    attachmentNames: list[str] = []
