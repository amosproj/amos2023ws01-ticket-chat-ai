from pydantic import BaseModel

from Backend.app.api.dto.ticket import Ticket


class WrappedTicket(BaseModel):
    email: str
    ticket: Ticket
