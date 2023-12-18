from unittest import TestCase
from unittest.mock import MagicMock
from bson import ObjectId
from fastapi import HTTPException
from starlette import status
from pymongo.results import InsertOneResult, UpdateResult

from app.api.dto.user import User
from app.repository.entity.user_entity import UserEntity
from app.service.user_db_service import UserDBService


class UserDBServiceUnitTest(TestCase):
    def setUp(self):
        self.user_repository_mock = MagicMock()
        self.user_db_service = UserDBService(user_repository=self.user_repository_mock)
        self.user_id = ObjectId("5f50c31e8a88c832bc32f2f1")
        self.user_entity = UserEntity(
            _id=self.user_id,
            first_name="First",
            family_name="Family",
            email_address="First.FirstEmail@gmail.com",
            location="Location",
            password="pass",
            ticket_ids=[],
        )

    def test_create_user_success(self):
        # Define
        insert_one_result = InsertOneResult(inserted_id=self.user_id, acknowledged=True)
        exp_user = User(
            id=str(self.user_id),
            first_name="First",
            family_name="Family",
            email_address="First.FirstEmail@gmail.com",
            location="Location",
            password="pass",
            ticket_ids=[],
        )

        # Mock
        self.user_repository_mock.create_user.return_value = insert_one_result
        self.user_repository_mock.read_users.return_value = [self.user_entity]

        # Act
        act_user = self.user_db_service.create_user(user_entity=self.user_entity)

        # Expect
        self.assertEqual(exp_user.dict(), act_user.dict())
        self.user_repository_mock.create_user.assert_called_once()
        self.user_repository_mock.read_users.assert_called_once()

    def test_create_user_creation_failed(self):
        # Define
        insert_one_result = InsertOneResult(
            inserted_id=self.user_id, acknowledged=False
        )
        exp_status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        exp_detail = "User creation failed."

        # Mock
        self.user_repository_mock.create_user.return_value = insert_one_result

        # Act & Expect
        with self.assertRaises(HTTPException) as cm:
            self.user_db_service.create_user(user_entity=self.user_entity)
        act_exception = cm.exception

        self.assertEqual(exp_status_code, act_exception.status_code)
        self.assertEqual(exp_detail.lower(), act_exception.detail.lower())

    def test_update_user_ticket_success(self):
        # Define
        update_result = UpdateResult(raw_result={"nModified": 1}, acknowledged=True)
        exp_user = User(
            id=str(self.user_id),
            first_name="First",
            family_name="Family",
            email_address="First.FirstEmail@gmail.com",
            location="Location",
            password="pass",
            ticket_ids=["new_ticket_id"],
        )

        # Mock
        self.user_repository_mock.read_users.return_value = [self.user_entity]
        self.user_repository_mock.update_user.return_value = update_result

        # Act
        act_user = self.user_db_service.update_user_ticket(
            str(self.user_id), "new_ticket_id"
        )

        # Expect
        self.assertEqual(exp_user.dict(), act_user.dict())  # Compare as dictionaries
        self.user_repository_mock.read_users.assert_called_once()
        self.user_repository_mock.update_user.assert_called_once()

    def test_get_user_by_email_success(self):
        # Define
        mocked_user = {
            "_id": ObjectId("5f50c31e8a88c832bc32f2f1"),
            "first_name": "Mocked",
            "family_name": "User",
            "email_address": "mocked.user@example.com",
            "location": "Mockville",
            "password": "mocked_password",
            "ticket_ids": [],
        }
        user_entity = UserEntity(**mocked_user)

        # Mock
        self.user_repository_mock.read_users_by_email.return_value = [user_entity]

        # Act
        retrieved_user = self.user_db_service.get_user_by_email(
            "mocked.user@example.com"
        )

        # Assert
        self.assertEqual(retrieved_user.first_name, "Mocked")
        self.assertEqual(retrieved_user.email_address, "mocked.user@example.com")
        # Add other assertions for remaining attributes as needed

        self.user_repository_mock.read_users_by_email.assert_called_once_with(
            "mocked.user@example.com"
        )
