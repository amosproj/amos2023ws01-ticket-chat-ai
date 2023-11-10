from bson import ObjectId
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.results import InsertOneResult, UpdateResult, DeleteResult

from app.configs.database_config import MONGODB_URL
from app.dto.ticket import Ticket


class TicketRepository:
    def __init__(self):
        client = MongoClient(MONGODB_URL)
        db = client.talktix
        self.collection: Collection = db.ticket

    def create_ticket(self, ticket: Ticket) -> InsertOneResult:
        return self.collection.insert_one(document=ticket.dict())

    def read_tickets(self, ticket_id: ObjectId = None) -> list[dict]:
        return list(self.collection.find(filter={"_id": ticket_id} if ticket_id else None))

    def update_ticket(self, ticket_id: ObjectId, ticket: Ticket) -> UpdateResult:
        return self.collection.replace_one(filter={"_id": ticket_id}, replacement=ticket.dict(), upsert=True)

    def delete_ticket(self, ticket_id: ObjectId) -> DeleteResult:
        return self.collection.delete_one(filter={"_id": ticket_id})
