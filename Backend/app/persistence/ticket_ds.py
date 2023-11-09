from bson import ObjectId
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.results import InsertOneResult, UpdateResult, DeleteResult

from app.dto.ticket import Ticket


class TicketDS:
    def __init__(self):
        client = MongoClient("mongodb://localhost:27017/")
        db = client.talktix
        self.collection: Collection = db.ticket

    def create_ticket(self, ticket: Ticket) -> InsertOneResult:
        return self.collection.insert_one(document=ticket.dict())

    def read_all_tickets(self) -> list[dict]:
        return list(self.collection.find())

    def update_ticket(self, ticket_id: ObjectId, ticket: Ticket) -> UpdateResult:
        return self.collection.replace_one(filter={"_id": ticket_id}, replacement=ticket.dict(), upsert=True)

    def delete_ticket(self, ticket_id: ObjectId) -> DeleteResult:
        return self.collection.delete_one(filter={"_id": ticket_id})
