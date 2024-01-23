import json
import os

from app.repository.department_repository import DepartmentRepository
from app.util.logger import logger


class DepartmentDBRoutineService:
    def __init__(
        self,
        department_repository: DepartmentRepository,
    ):
        self.department_repository = department_repository

    def start_routine(self):
        if len(self.department_repository.read_departments()) < 6:
            logger.info("Start department db routine")

            default_departments = os.path.join(
                os.path.dirname(__file__),
                "..",
                "repository",
                "resources",
                "default_departments.json",
            )
            with open(default_departments) as departments_file:
                departments = json.load(departments_file)
                for department in departments:
                    self.department_repository.create_department(department)

            logger.info("Default departments added")
