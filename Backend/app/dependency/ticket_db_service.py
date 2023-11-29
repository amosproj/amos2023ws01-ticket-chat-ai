from fastapi.params import Depends

from app.dependency.ticket_repository import get_ticket_repository
from app.service.ticket_db_service import TicketDBService
from app.repository.ticket_repository import TicketRepository


def get_ticket_db_service(
    ticket_repository: TicketRepository = Depends(get_ticket_repository),
):
    return TicketDBService(ticket_repository=ticket_repository)
