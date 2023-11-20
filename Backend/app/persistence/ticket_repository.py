from bson import ObjectId
from fastapi import Depends
from pymongo.collection import Collection
from pymongo.results import InsertOneResult, UpdateResult, DeleteResult

from app.config.collection_config import get_ticket_collection
from app.dto.ticket import Ticket


class TicketRepository:
    def __init__(self, collection: Collection = Depends(get_ticket_collection)):
        self.collection = collection

    def create_ticket(self, ticket: Ticket) -> InsertOneResult:
        return self.collection.insert_one(document=ticket.dict())

    def read_tickets(self, ticket_id: ObjectId = None) -> list[dict]:
        return list(
            self.collection.find(filter={"_id": ticket_id} if ticket_id else None)
        )

    def update_ticket(self, ticket_id: ObjectId, ticket: Ticket) -> UpdateResult:
        return self.collection.replace_one(
            filter={"_id": ticket_id}, replacement=ticket.dict(), upsert=True
        )

    def delete_ticket(self, ticket_id: ObjectId) -> DeleteResult:
        return self.collection.delete_one(filter={"_id": ticket_id})
