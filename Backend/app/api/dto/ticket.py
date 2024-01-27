from bson import ObjectId
from pydantic import BaseModel

from app.enum.customer_prio import CustomerPrio
from app.enum.prio import Prio

from app.enum.state import State


class Ticket(BaseModel):
    id: str = ""
    title: str | None
    service: str | None
    category: str | None
    keywords: list
    customerPriority: CustomerPrio | None
    affectedPerson: str
    description: str
    priority: Prio | None
    attachmentNames: list[str] = []
    requestType: str | None
    state = State.draft
