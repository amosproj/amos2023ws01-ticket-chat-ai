from pydantic import BaseModel

from app.dto.enum.prio import Prio


class Ticket(BaseModel):
    subject: str
    description: str
    impact: Prio
    priority: Prio
    request_type: str
