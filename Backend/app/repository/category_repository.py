from bson import ObjectId
from pymongo.collection import Collection
from pymongo.results import InsertOneResult, UpdateResult, DeleteResult

from app.repository.entity.category_entity import CategoryEntity
from app.util.logger import logger


class CategoryRepository:
    def __init__(self, collection: Collection):
        self.collection = collection

    def create_category(self, category: CategoryEntity | dict) -> InsertOneResult:
        logger.info("Creating category in the database...")
        return self.collection.insert_one(document=category)

    def read_categories(
        self, category_id: ObjectId = None
    ) -> list[CategoryEntity]:
        logger.info("Reading category/(ies) from the database...")
        return list(
            self.collection.find(filter={"_id": category_id} if category_id else None)
        )

    def delete_category(self, category_id: ObjectId) -> DeleteResult:
        logger.info(f"Deleting category {category_id} from the database...")
        return self.collection.delete_one(filter={"_id": category_id})
