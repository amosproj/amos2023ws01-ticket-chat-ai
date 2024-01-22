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
        len_categories = len(self.category_repository.read_categories())

        if len_categories < 312:
            logger.info("Start category db routine")

            default_departments = os.path.join(
                os.path.dirname(__file__),
                "..",
                "repository",
                "resources",
                "default_departments.json",
            )
            default_services = os.path.join(
                os.path.dirname(__file__),
                "..",
                "repository",
                "resources",
                "default_services.json",
            )
            with open(default_departments) as departments_file:
                departments = json.load(departments_file)
                with open(default_services) as services_file:
                    services = json.load(services_file)
                    for department in departments:
                        for service in services:
                            for service_keyword in service["safe_keywords"]:
                                category = (
                                    service_keyword + "->" + department["name"]
                                )
                                category_dict = {"name": category}
                                self.category_repository.create_category(
                                    category_dict
                                )

            logger.info("Categories added")
