from bson import ObjectId
from pymongo.collection import Collection
from pymongo.results import InsertOneResult, UpdateResult, DeleteResult

from app.repository.entity.user_entity import UserEntity
from app.util.logger import logger


class UserRepository:
    def __init__(self, collection: Collection):
        self.collection = collection

    def create_user(self, user: UserEntity | dict) -> InsertOneResult:
        logger.info("Creating user in the database...")
        return self.collection.insert_one(document=user)

    def read_users(self, user_id: ObjectId = None) -> list[UserEntity]:
        logger.info("Reading user(s) from the database...")
        return list(self.collection.find(filter={"_id": user_id} if user_id else None))

    def update_user(self, user_id: ObjectId, user: UserEntity | dict) -> UpdateResult:
        logger.info(f"Updating user {user_id} in the database...")
        return self.collection.replace_one(
            filter={"_id": user_id}, replacement=user, upsert=True
        )

    def delete_user(self, user_id: ObjectId) -> DeleteResult:
        logger.info(f"Deleting user {user_id} from the database...")
        return self.collection.delete_one(filter={"_id": user_id})

    def read_users_by_email(self, email: str) -> list[UserEntity]:
        logger.info(f"Reading user(s) with email {email} from the database...")
        users = list(self.collection.find({"email_address": email}))
        return users if users else []

    def authenticate_user(self, email: str, password: str) -> bool:
        logger.info(f"Authenticating user with email {email}...")
        user = self.collection.find_one({"email_address": email, "password": password})
        return user is not None
