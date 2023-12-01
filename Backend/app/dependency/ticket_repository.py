from app.dependency.collection import get_ticket_collection
from fastapi import Depends
from pymongo.collection import Collection

from app.repository.ticket_repository import TicketRepository


def get_ticket_repository(
    collection: Collection = Depends(get_ticket_collection),
) -> TicketRepository:
    return TicketRepository(collection=collection)
