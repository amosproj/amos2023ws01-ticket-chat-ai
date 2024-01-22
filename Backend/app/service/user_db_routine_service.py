import json
import os

from app.repository.user_repository import UserRepository
from app.util.logger import logger


class UserDBRoutineService:
    def __init__(
        self,
        user_repository: UserRepository,
    ):
        self.user_repository = user_repository

    def start_routine(self):
        if len(self.user_repository.read_users()) < 10:
            logger.info("Start user db routine")

            default_users = os.path.join(
                os.path.dirname(__file__),
                "..",
                "repository",
                "resources",
                "default_users.json",
            )
            with open(default_users) as users_file:
                users = json.load(users_file)
                for user in users:
                    self.user_repository.create_user(user)

            logger.info("Default users added")
