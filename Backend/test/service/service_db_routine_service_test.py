from unittest import TestCase
from unittest.mock import MagicMock

from app.service.service_db_routine_service import ServiceDBRoutineService


class ServiceDBRoutineServiceUnitTest(TestCase):
    def setUp(self):
        self.service_repository_mock = MagicMock()
        self.service_db_service = ServiceDBRoutineService(service_repository=self.service_repository_mock)

    def test_start_routine(self):
        # Act
        self.service_db_service.start_routine()
        # Assert
        self.assertEqual(9, len(self.service_repository_mock.create_service.mock_calls), "not all defaults saved")
