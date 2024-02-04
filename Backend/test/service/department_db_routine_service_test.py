from unittest import TestCase
from unittest.mock import MagicMock

from app.service.department_db_routine_service import DepartmentDBRoutineService


class DepartmentDBRoutineServiceUnitTest(TestCase):
    def setUp(self):
        self.department_repository_mock = MagicMock()
        self.department_db_service = DepartmentDBRoutineService(department_repository=self.department_repository_mock)

    def test_start_routine(self):
        # Act
        self.department_db_service.start_routine()
        # Assert
        self.assertEqual(6, len(self.department_repository_mock.create_department.mock_calls), "not all defaults saved")
