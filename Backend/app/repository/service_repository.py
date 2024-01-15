from bson import ObjectId
from pymongo.collection import Collection
from pymongo.results import InsertOneResult, UpdateResult, DeleteResult

from app.repository.entity.service_entity import ServiceEntity
from app.util.logger import logger


class ServiceRepository:
    def __init__(self, collection: Collection):
        self.collection = collection

    def create_service(self, service: ServiceEntity | dict) -> InsertOneResult:
        logger.info("Creating service in the database...")
        return self.collection.insert_one(document=service)

    def read_services(self, service_id: ObjectId = None) -> list[ServiceEntity]:
        logger.info("Reading service(s) from the database...")
        return list(
            self.collection.find(filter={"_id": service_id} if service_id else None)
        )

    def update_service(
        self, service_id: ObjectId, service: ServiceEntity | dict
    ) -> UpdateResult:
        logger.info(f"Updating service {service_id} in the database...")
        return self.collection.replace_one(
            filter={"_id": service_id}, replacement=service, upsert=True
        )

    def delete_service(self, service_id: ObjectId) -> DeleteResult:
        logger.info(f"Deleting service {service_id} from the database...")
        return self.collection.delete_one(filter={"_id": service_id})
