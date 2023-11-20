from pydantic import BaseModel

from app.dto.enum.prio import Prio
from app.dto.enum.customer_prio import CustomerPrio


class Ticket(BaseModel):
    title: str
    location: str
    category: str
    keywords: list
    customerPriority: CustomerPrio
    affectedPerson: str
    description: str
    priority: Prio
