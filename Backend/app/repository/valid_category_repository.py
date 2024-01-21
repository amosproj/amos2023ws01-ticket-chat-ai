from bson import ObjectId
from pymongo.collection import Collection
from pymongo.results import InsertOneResult, UpdateResult, DeleteResult

from app.repository.entity.valid_category_entity import ValidCategoryEntity
from app.util.logger import logger


class ValidCategoryRepository:
    def __init__(self, collection: Collection):
        self.collection = collection

    def create_category(self, category: ValidCategoryEntity | dict) -> InsertOneResult:
        logger.info("Creating valid category in the database...")
        return self.collection.insert_one(document=category)

    def read_categories(
        self, category_id: ObjectId = None
    ) -> list[ValidCategoryEntity]:
        logger.info("Reading valid category/(ies) from the database...")
        return list(
            self.collection.find(filter={"_id": category_id} if category_id else None)
        )

    def delete_category(self, category_id: ObjectId) -> DeleteResult:
        logger.info(f"Deleting valid category {category_id} from the database...")
        return self.collection.delete_one(filter={"_id": category_id})
