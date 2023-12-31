from bson import ObjectId
from pymongo.collection import Collection
from pymongo.results import InsertOneResult, UpdateResult, DeleteResult
from app.repository.entity.ticket_entity import TicketEntity
from app.util.logger import logger


class TicketRepository:
    def __init__(self, collection: Collection):
        self.collection = collection

    def create_ticket(self, ticket: TicketEntity | dict) -> InsertOneResult:
        logger.info("Creating ticket in the database...")
        return self.collection.insert_one(document=ticket)

    def read_tickets(self, ticket_id: ObjectId = None) -> list[TicketEntity]:
        logger.info("Reading ticket(s) from the database...")
        return list(
            self.collection.find(filter={"_id": ticket_id} if ticket_id else None)
        )

    def update_ticket(
        self, ticket_id: ObjectId, ticket: TicketEntity | dict
    ) -> UpdateResult:
        logger.info(f"Updating ticket {ticket_id} in the database...")
        return self.collection.replace_one(
            filter={"_id": ticket_id}, replacement=ticket, upsert=True
        )

    def delete_ticket(self, ticket_id: ObjectId) -> DeleteResult:
        logger.info(f"Deleting ticket {ticket_id} from the database...")
        return self.collection.delete_one(filter={"_id": ticket_id})
