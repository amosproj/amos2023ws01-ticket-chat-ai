from bson import ObjectId
from pydantic import BaseModel

from app.enum.customer_prio import CustomerPrio
from app.enum.prio import Prio


class Ticket(BaseModel):
    id: str = ""
    title: str | None
    service: Location | ServiceEnum | None
    category: str | None
    keywords: list
    customerPriority: CustomerPrio | None
    affectedPerson: str
    description: str
    priority: Prio | None
    requestType: str | None
    attachmentNames: list[str] = []
