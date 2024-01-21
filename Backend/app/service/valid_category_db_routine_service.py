import json
import os

from app.repository.valid_category_repository import ValidCategoryRepository
from app.util.logger import logger


class ValidCategoryDBRoutineService:
    def __init__(
        self,
        valid_category_repository: ValidCategoryRepository,
    ):
        self.valid_category_repository = valid_category_repository

    def start_routine(self):
        len_valid_categories = len(self.valid_category_repository.read_categories())

        if len_valid_categories < 312:
            logger.info("Start valid category db routine")

            default_categories = os.path.join(
                os.path.dirname(__file__),
                "..",
                "repository",
                "resources",
                "default_categories.json",
            )
            default_services = os.path.join(
                os.path.dirname(__file__),
                "..",
                "repository",
                "resources",
                "default_services.json",
            )
            with open(default_categories) as categories_file:
                categories = json.load(categories_file)
                with open(default_services) as services_file:
                    services = json.load(services_file)
                    for category in categories:
                        for service in services:
                            for service_keyword in service["safe_keywords"]:
                                valid_category = service_keyword + "->" + category["name"]
                                valid_category_dict = {
                                    "name": valid_category
                                }
                                self.valid_category_repository.create_category(valid_category_dict)

            logger.info("Valid categories added")
