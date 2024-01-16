import json
import os

from app.repository.service_repository import ServiceRepository
from app.util.logger import logger


class ServiceDBRoutineService:
    def __init__(
        self,
        service_repository: ServiceRepository,
    ):
        self.service_repository = service_repository

    def start_routine(self):
        if len(self.service_repository.read_services()) < 9:
            logger.info("Start service db routine")

            default_services = os.path.join(
                os.path.dirname(__file__),
                "..",
                "repository",
                "resources",
                "default_services.json",
            )
            with open(default_services) as services_file:
                services = json.load(services_file)
                for service in services:
                    self.service_repository.create_service(service)

            logger.info("Default services added")
