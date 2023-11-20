from pymongo.collection import Collection
from pymongo import MongoClient
import configparser
from app.persistence.ticket_repository import TicketRepository
from app.dto.ticket import Ticket


class TicketDBService:
    def save_ticket(self, ticket: dict):
        db_collection = self.get_or_create_collection()
        ticket_ds = TicketRepository(db_collection)
        ticket = Ticket.parse_obj(ticket)

        return ticket_ds.create_ticket(ticket)

    def get_or_create_collection(self) -> Collection:
        config = configparser.ConfigParser()
        config.read("config.ini")
        mongodb_url = config["DEFAULT"]["MONGODB_URL"]
        client = MongoClient(mongodb_url)
        db = client.talktix
        collection = db.ticket
        return collection