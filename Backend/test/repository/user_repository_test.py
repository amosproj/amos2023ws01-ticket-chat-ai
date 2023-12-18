import configparser
import unittest
from unittest.mock import MagicMock
import pytest
from bson import ObjectId
from pymongo import MongoClient
from pymongo.results import InsertOneResult, UpdateResult, DeleteResult

from app.repository.entity.user_entity import UserEntity
from app.repository.user_repository import UserRepository
from app.util.database_routine import start_server, stop_server
from test.config.pytest import SKIP_TEST


class UserRepositoryUnitTest(unittest.TestCase):
    def setUp(self):
        self.collection_mock = MagicMock()
        self.user_repository = UserRepository(collection=self.collection_mock)
        self.user_id = ObjectId("5f50c31e8a88c832bc32f2f1")
        self.user = UserEntity(
            _id=self.user_id,
            first_name="First",
            family_name="Family",
            email_address="First.FirstEmail@gmail.com",
            location="Location",
            password="pass",
            ticket_ids=[],
        )

    def test_create_user(self):
        result_exp = InsertOneResult(inserted_id=self.user_id, acknowledged=True)
        self.collection_mock.insert_one.return_value = result_exp
        result_act = self.user_repository.create_user(user=self.user)
        self.assertEqual(result_exp, result_act, "wrong result of create_user()")
        self.collection_mock.insert_one.assert_called_once_with(document=self.user)

    def test_read_users(self):
        user_list_exp = [self.user]
        self.collection_mock.find.return_value = user_list_exp
        result_act = self.user_repository.read_users(user_id=self.user_id)
        self.assertEqual(user_list_exp, result_act, "wrong result of read_users()")
        self.collection_mock.find.assert_called_once_with(filter={"_id": self.user_id})

    def test_update_user(self):
        result_exp = UpdateResult(raw_result={"nModified": 1}, acknowledged=True)
        self.collection_mock.replace_one.return_value = result_exp
        result_act = self.user_repository.update_user(
            user_id=self.user_id, user=self.user
        )
        self.assertEqual(result_exp, result_act, "wrong result of update_user()")
        self.collection_mock.replace_one.assert_called_once_with(
            filter={"_id": self.user_id}, replacement=self.user, upsert=True
        )

    def test_delete_user(self):
        result_exp = DeleteResult(raw_result={"n": 1}, acknowledged=True)
        self.collection_mock.delete_one.return_value = result_exp
        result_act = self.user_repository.delete_user(user_id=self.user_id)
        self.assertEqual(result_exp, result_act, "wrong result of delete_user()")
        self.collection_mock.delete_one.assert_called_once_with(
            filter={"_id": self.user_id}
        )

    def test_read_users_by_email(self):
        email = "test@example.com"
        user_list_exp = [self.user]
        self.collection_mock.find.return_value = user_list_exp
        result_act = self.user_repository.read_users_by_email(email)
        self.assertEqual(user_list_exp, result_act, "wrong result of read_users_by_email()")
        self.collection_mock.find.assert_called_once_with({"email_address": email})



@pytest.mark.skipif(condition=SKIP_TEST, reason="Database is missing")
class UserRepositoryIntegrationTest(unittest.TestCase):
    def setUp(self):
        config = configparser.ConfigParser()
        config.read("config.ini")
        mongodb_url = config["DEFAULT"]["MONGODB_URL"]
        client = MongoClient(mongodb_url)
        db = client.talktix
        collection = db.user
        self.user_repository = UserRepository(collection)
        self.user = {
            "id": "",
            "first_name": "First",
            "family_name": "Family",
            "email_address": "First.FirstEmail@gmail.com",
            "location": "Location",
            "password": "pass",
            "ticket_ids": [],
        }

    def test_crud(self):
        # Start db server
        system_status = start_server()
        assert system_status == 0

        # Create user
        user_id = self.user_repository.create_user(user=self.user).inserted_id
        assert user_id is not None

        # Read created user
        users = self.user_repository.read_users(user_id=user_id)
        assert len(users) == 1 and users[0]["_id"] == user_id

        # Update user
        updated_user = self.user.copy()
        updated_user["some_field"] = "new_value"
        update_result = self.user_repository.update_user(
            user_id=user_id, user=updated_user
        )
        assert update_result.modified_count == 1

        # Read updated user
        users = self.user_repository.read_users(user_id=user_id)
        assert len(users) == 1 and users[0]["some_field"] == "new_value"

        # Delete user
        delete_result = self.user_repository.delete_user(user_id=user_id)
        assert delete_result.deleted_count == 1

        # Stop db server
        system_status = stop_server()
        assert system_status == 0
