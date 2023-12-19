from bson import ObjectId
from fastapi import HTTPException
from starlette import status

from app.api.dto.user import User
from app.repository.entity.user_entity import UserEntity
from app.repository.user_repository import UserRepository
from app.util.logger import logger


class UserDBService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def create_user(self, user_entity: UserEntity | dict) -> User:
        logger.info("Creating user...")
        insert_one_result = self.user_repository.create_user(user_entity)
        if not insert_one_result.acknowledged:
            self._throw_internal_server_error("user creation failed.")
        found_users = self.user_repository.read_users(insert_one_result.inserted_id)
        if len(found_users) != 1:
            self._throw_internal_server_error(
                f"user with id {str(insert_one_result.inserted_id)} not found."
            )
        user_entity = found_users[0]
        return self._map_user(user_entity)

    def update_user_ticket(self, user_id: str, new_ticket_id: str) -> User:
        logger.info("Updating user via adding tickets...")
        user_id = ObjectId(user_id)
        found_users = self.user_repository.read_users(user_id)
        if len(found_users) != 1:
            self._throw_internal_server_error(f"user with id {str(user_id)} not found.")
        user_entity = found_users[0]
        ticket_ids = []
        if user_entity["ticket_ids"]:
            ticket_ids = user_entity["ticket_ids"]
        ticket_ids.append(new_ticket_id)

        user_entity["ticket_ids"] = ticket_ids
        update_result = self.user_repository.update_user(user_id, user_entity)
        if not update_result.acknowledged:
            self._throw_internal_server_error(
                f"user with id {str(user_id)} not updated."
            )
        return self._map_user(user_entity)

    def get_user_by_email(self, email: str) -> User:
        logger.info("Retrieving user by email...")
        user_entities = self.user_repository.read_users_by_email(email)
        if not user_entities:
            self._throw_internal_server_error(f"user with email {email} not found.")

        user_entity = user_entities[0]
        return self._map_user(user_entity)

    @staticmethod
    def _map_user(user_entity: UserEntity) -> User:
        user = User.parse_obj(user_entity)
        user.id = str(user_entity["_id"])
        return user

    @staticmethod
    def _throw_internal_server_error(message: str):
        logger.error(message)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=message,
        )
