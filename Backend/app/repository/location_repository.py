from app.repository.entity.location_entity import LocationEntity
from app.util.logger import logger
from bson import ObjectId
from pymongo.collection import Collection
from pymongo.results import InsertOneResult


class LocationRepository:
    def __init__(self, collection: Collection):
        self.collection = collection

    def create_location(self, location: LocationEntity | dict) -> InsertOneResult:
        logger.info("Creating location in the database...")
        return self.collection.insert_one(document=location)

    def read_locations(self, location_id: ObjectId = None) -> list[LocationEntity]:
        logger.info("Reading location(s) from the database...")
        return list(
            self.collection.find(filter={"_id": location_id} if location_id else None)
        )
