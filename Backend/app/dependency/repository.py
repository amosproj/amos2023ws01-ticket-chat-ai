from fastapi import Depends
from pymongo.collection import Collection

from app.dependency.collection import (
    get_ticket_collection,
    get_user_collection,
    get_service_collection,
    get_category_collection,
    get_valid_category_collection,
    get_location_collection,
)
from app.repository.ticket_repository import TicketRepository
from app.repository.user_repository import UserRepository
from app.repository.service_repository import ServiceRepository
from app.repository.location_repository import LocationRepository
from app.repository.category_repository import CategoryRepository
from app.repository.valid_category_repository import ValidCategoryRepository


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


def get_location_repository(
    collection: Collection = Depends(get_location_collection),
) -> LocationRepository:
    return LocationRepository(collection=collection)


def get_category_repository(
    collection: Collection = Depends(get_category_collection),
) -> CategoryRepository:
    return CategoryRepository(collection=collection)


def get_valid_category_repository(
    collection: Collection = Depends(get_valid_category_collection),
) -> ValidCategoryRepository:
    return ValidCategoryRepository(collection=collection)
