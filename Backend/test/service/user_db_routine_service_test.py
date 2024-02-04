from unittest import TestCase
from unittest.mock import MagicMock

from app.service.user_db_routine_service import UserDBRoutineService


class UserDBRoutineServiceUnitTest(TestCase):
    def setUp(self):
        self.user_repository_mock = MagicMock()
        self.user_db_service = UserDBRoutineService(
            user_repository=self.user_repository_mock
        )

    def test_start_routine(self):
        # Act
        self.user_db_service.start_routine()
        # Assert
        self.assertEqual(
            10,
            len(self.user_repository_mock.create_user.mock_calls),
            "not all defaults saved",
        )
