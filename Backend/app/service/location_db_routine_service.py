import json
import os

from app.repository.location_repository import LocationRepository
from app.util.logger import logger


class LocationDBRoutineService:
    def __init__(
        self,
        location_repository: LocationRepository,
    ):
        self.location_repository = location_repository

    def start_routine(self):
        if len(self.location_repository.read_locations()) < 5:
            logger.info("Start location db routine")

            default_locations = os.path.join(
                os.path.dirname(__file__),
                "..",
                "repository",
                "resources",
                "default_locations.json",
            )
            with open(default_locations) as locations_file:
                locations = json.load(locations_file)
                for location in locations:
                    self.location_repository.create_location(location)

            logger.info("Default locations added")
