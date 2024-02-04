from unittest import TestCase
from unittest.mock import MagicMock

from app.service.category_db_routine_service import CategoryDBRoutineService


class CategoryDBRoutineServiceUnitTest(TestCase):
    def setUp(self):
        self.category_repository_mock = MagicMock()
        self.category_db_service = CategoryDBRoutineService(category_repository=self.category_repository_mock)

    def test_start_routine(self):
        # Act
        self.category_db_service.start_routine()
        # Assert
        self.assertEqual(6, len(self.category_repository_mock.create_category.mock_calls), "not all defaults saved")
