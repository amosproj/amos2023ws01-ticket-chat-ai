from app.repository.entity.department_entity import DepartmentEntity
from app.util.logger import logger
from bson import ObjectId
from pymongo.collection import Collection
from pymongo.results import InsertOneResult


class DepartmentRepository:
    def __init__(self, collection: Collection):
        self.collection = collection

    def create_department(self, department: DepartmentEntity | dict) -> InsertOneResult:
        logger.info("Creating department in the database...")
        return self.collection.insert_one(document=department)

    def read_departments(
        self, department_id: ObjectId = None
    ) -> list[DepartmentEntity]:
        logger.info("Reading department/s from the database...")
        return list(
            self.collection.find(
                filter={"_id": department_id} if department_id else None
            )
        )
