import base64

from bson import ObjectId
from fastapi import UploadFile

from app.dto.ticket import Ticket
from app.entity.attachment_entity import AttachmentEntity
from app.entity.ticket_entity import TicketEntity
from app.logger import logger
from app.persistence.ticket_repository import TicketRepository


class TicketDBService:
    def __init__(self, ticket_repository: TicketRepository):
        self.ticket_repository = ticket_repository

    def create_ticket(self, ticket_entity: TicketEntity):
        logger.info("Creating ticket...")
        return self.ticket_repository.create_ticket(ticket_entity)

    def update_ticket_attachments(self, ticket_id: str, files: list[UploadFile]) -> Ticket:
        logger.info("Updating ticket via adding attachments...")
        ticket_id = ObjectId(ticket_id)
        found_tickets = self.ticket_repository.read_tickets(ticket_id)
        if len(found_tickets) != 1:
            pass
        ticket_entity = found_tickets[0]
        attachment_entities = []
        for file in files:
            attachment_entity = AttachmentEntity(name=file.filename, type=file.content_type,
                                          data=base64.b64encode(file.file.read()))
            attachment_entities.append(attachment_entity)
        ticket_entity["attachments"] = attachment_entities
        update_result = self.ticket_repository.update_ticket(ticket_id, ticket_entity)
        if update_result.modified_count != 1:
            pass
        ticket = Ticket.parse_obj(ticket_entity)
        ticket.id = str(ticket_entity["_id"])
        for attachment_entity in ticket_entity["attachments"]:
            ticket.attachmentNames.append(attachment_entity["name"])
        return ticket
