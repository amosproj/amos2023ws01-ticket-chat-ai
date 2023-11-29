import base64

from bson import ObjectId
from fastapi import UploadFile

from app.api.dto.ticket import Ticket
from app.util.logger import logger
from app.repository.entity.attachment_entity import AttachmentEntity
from app.repository.entity.ticket_entity import TicketEntity
from app.repository.ticket_repository import TicketRepository


class TicketDBService:
    def __init__(self, ticket_repository: TicketRepository):
        self.ticket_repository = ticket_repository

    def create_ticket(self, ticket_entity: TicketEntity) -> Ticket:
        logger.info("Creating ticket...")
        insert_result = self.ticket_repository.create_ticket(ticket_entity)
        if not insert_result.acknowledged:
            pass
        found_tickets = self.ticket_repository.read_tickets(insert_result.inserted_id)
        if len(found_tickets) != 1:
            pass
        ticket_entity = found_tickets[0]
        return self._map_ticket(ticket_entity)

    def update_ticket_attachments(
        self, ticket_id: str, files: list[UploadFile]
    ) -> Ticket:
        logger.info("Updating ticket via adding attachments...")
        ticket_id = ObjectId(ticket_id)
        found_tickets = self.ticket_repository.read_tickets(ticket_id)
        if len(found_tickets) != 1:
            pass
        ticket_entity = found_tickets[0]
        attachment_entities = []
        for file in files:
            attachment_entity = AttachmentEntity(
                name=file.filename,
                type=file.content_type,
                data=base64.b64encode(file.file.read()),
            )
            attachment_entities.append(attachment_entity)
        ticket_entity["attachments"] = attachment_entities
        update_result = self.ticket_repository.update_ticket(ticket_id, ticket_entity)
        if update_result.modified_count != 1:
            pass
        return self._map_ticket(ticket_entity)

    def _map_ticket(self, ticket_entity: TicketEntity) -> Ticket:
        ticket = Ticket.parse_obj(ticket_entity)
        ticket.id = str(ticket_entity["_id"])
        if "attachments" not in ticket_entity.keys():
            ticket_entity["attachments"] = []
        for attachment_entity in ticket_entity["attachments"]:
            ticket.attachmentNames.append(attachment_entity["name"])
        return ticket
