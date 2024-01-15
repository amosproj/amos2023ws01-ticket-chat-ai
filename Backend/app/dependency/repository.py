from fastapi import Depends
from pymongo.collection import Collection

from app.dependency.collection import get_ticket_collection, get_user_collection, get_service_collection
from app.repository.ticket_repository import TicketRepository
from app.repository.user_repository import UserRepository
from app.repository.service_repository import ServiceRepository


def get_ticket_repository(
        collection: Collection = Depends(get_ticket_collection),
) -> TicketRepository:
    return TicketRepository(collection=collection)


def get_user_repository(
        collection: Collection = Depends(get_user_collection),
) -> UserRepository:
    return UserRepository(collection=collection)


def get_service_repository(
        collection: Collection = Depends(get_service_collection),
) -> ServiceRepository:
    return ServiceRepository(collection=collection)
