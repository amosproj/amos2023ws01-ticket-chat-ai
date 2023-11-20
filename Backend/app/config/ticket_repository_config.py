from typing import Annotated, Any

from fastapi import Depends
from pymongo.collection import Collection

from app.config.collection_config import get_ticket_collection
from app.persistence.ticket_repository import TicketRepository


def get_ticket_repository(collection: Collection = Depends(get_ticket_collection)) -> TicketRepository:
    return TicketRepository(collection=collection)
