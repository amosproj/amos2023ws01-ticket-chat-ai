from pydantic import BaseModel

from app.dto.prio_enum import PrioEnum


class Ticket(BaseModel):
    subject: str
    description: str
    impact: PrioEnum
    priority: PrioEnum
    request_type: str
