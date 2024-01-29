from fastapi.params import Depends

from app.dependency.repository import get_ticket_repository, get_user_repository
from app.repository.ticket_repository import TicketRepository
from app.repository.user_repository import UserRepository
from app.service.ticket_db_service import TicketDBService
from app.service.user_db_service import UserDBService


def get_ticket_db_service(
    ticket_repository: TicketRepository = Depends(get_ticket_repository),
):
    return TicketDBService(ticket_repository=ticket_repository)


def get_user_db_service(
    user_repository: UserRepository = Depends(get_user_repository),
):
    return UserDBService(user_repository=user_repository)
