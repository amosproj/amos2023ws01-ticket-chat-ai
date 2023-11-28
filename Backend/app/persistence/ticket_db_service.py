from app.dto.ticket import Ticket
from app.persistence.ticket_repository import TicketRepository
from app.logger import logger


class TicketDBService:
    def __init__(self, ticket_repository: TicketRepository):
        self.ticket_repository = ticket_repository

    def save_ticket(self, ticket: dict):
        logger.info("Saving ticket to the database...")
        ticket = Ticket.parse_obj(ticket)
        return self.ticket_repository.create_ticket(ticket)
