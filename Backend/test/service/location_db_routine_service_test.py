from unittest import TestCase
from unittest.mock import MagicMock

from app.service.location_db_routine_service import LocationDBRoutineService


class LocationDBRoutineServiceUnitTest(TestCase):
    def setUp(self):
        self.location_repository_mock = MagicMock()
        self.location_db_service = LocationDBRoutineService(location_repository=self.location_repository_mock)

    def test_start_routine(self):
        # Act
        self.location_db_service.start_routine()
        # Assert
        self.assertEqual(5, len(self.location_repository_mock.create_location.mock_calls), "not all defaults saved")
