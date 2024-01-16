import base64

from bson import ObjectId
from fastapi import UploadFile, HTTPException
from starlette import status

from app.api.dto.ticket import Ticket
from app.util.logger import logger
from app.repository.entity.attachment_entity import AttachmentEntity
from app.repository.entity.ticket_entity import TicketEntity
from app.repository.ticket_repository import TicketRepository


class TicketDBService:
    def __init__(self, ticket_repository: TicketRepository):
        self.ticket_repository = ticket_repository

    def create_ticket(self, ticket_entity: TicketEntity | dict) -> Ticket:
        logger.info("Creating ticket...")
        insert_one_result = self.ticket_repository.create_ticket(ticket_entity)
        if not insert_one_result.acknowledged:
            self._throw_internal_server_error("Ticket creation failed.")
        found_tickets = self.ticket_repository.read_tickets(
            insert_one_result.inserted_id
        )
        if len(found_tickets) != 1:
            self._throw_internal_server_error(
                f"Ticket with id {str(insert_one_result.inserted_id)} not found."
            )
        ticket_entity = found_tickets[0]
        return self._map_ticket(ticket_entity)

    def update_ticket_attributes(
        self, ticket_id: str, updated_ticket: TicketEntity | dict
    ) -> Ticket:
        logger.info("Updating ticket attributes...")
        ticket_id = ObjectId(ticket_id)
        found_tickets = self.ticket_repository.read_tickets(ticket_id)
        if len(found_tickets) != 1:
            self._throw_internal_server_error(
                f"Ticket with id {str(ticket_id)} not found."
            )
        ticket_entity = found_tickets[0]
        ticket_entity["title"] = updated_ticket.title
        ticket_entity["service"] = updated_ticket.service
        ticket_entity["category"] = updated_ticket.category
        ticket_entity["keywords"] = updated_ticket.keywords
        ticket_entity["customerPriority"] = updated_ticket.customerPriority
        ticket_entity["affectedPerson"] = updated_ticket.affectedPerson
        ticket_entity["description"] = updated_ticket.description
        ticket_entity["priority"] = updated_ticket.priority
        ticket_entity["requestType"] = updated_ticket.requestType

        update_result = self.ticket_repository.update_ticket(ticket_id, ticket_entity)
        if not update_result.acknowledged:
            self._throw_internal_server_error(
                f"Ticket with id {str(ticket_id)} not updated."
            )
        return self._map_ticket(ticket_entity)

    def update_ticket_attachments(
        self, ticket_id: str, files: list[UploadFile]
    ) -> Ticket:
        logger.info("Updating ticket via adding attachments...")
        ticket_id = ObjectId(ticket_id)
        found_tickets = self.ticket_repository.read_tickets(ticket_id)
        if len(found_tickets) != 1:
            self._throw_internal_server_error(
                f"Ticket with id {str(ticket_id)} not found."
            )
        ticket_entity = found_tickets[0]
        attachment_entities = []
        if ticket_entity["attachments"]:
            attachment_entities = ticket_entity["attachments"]
        for file in files:
            attachment_entity = AttachmentEntity(
                name=file.filename,
                type=file.content_type,
                data=base64.b64encode(file.file.read()),
            )
            attachment_entities.append(attachment_entity)
        ticket_entity["attachments"] = attachment_entities
        update_result = self.ticket_repository.update_ticket(ticket_id, ticket_entity)
        if not update_result.acknowledged:
            self._throw_internal_server_error(
                f"Ticket with id {str(ticket_id)} not updated."
            )
        return self._map_ticket(ticket_entity)

    @staticmethod
    def _map_ticket(ticket_entity: TicketEntity) -> Ticket:
        ticket = Ticket.parse_obj(ticket_entity)
        ticket.id = str(ticket_entity["_id"])
        if "attachments" not in ticket_entity.keys():
            ticket_entity["attachments"] = []
        for attachment_entity in ticket_entity["attachments"]:
            ticket.attachmentNames.append(attachment_entity["name"])
        return ticket

    @staticmethod
    def _throw_internal_server_error(message: str):
        logger.error(message)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=message,
        )
