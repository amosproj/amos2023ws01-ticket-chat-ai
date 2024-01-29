import json
import os

from app.repository.category_repository import CategoryRepository
from app.util.logger import logger


class CategoryDBRoutineService:
    def __init__(
        self,
        category_repository: CategoryRepository,
    ):
        self.category_repository = category_repository

    def start_routine(self):
        if len(self.category_repository.read_categories()) < 6:
            logger.info("Start Category db routine")

            default_departments = os.path.join(
                os.path.dirname(__file__),
                "..",
                "repository",
                "resources",
                "default_categories.json",
            )
            with open(default_departments) as departments_file:
                categories = json.load(departments_file)
                for category in categories:
                    self.category_repository.create_category(category)

            logger.info("Default categories added")

