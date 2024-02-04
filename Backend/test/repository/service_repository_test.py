import unittest
from unittest.mock import MagicMock

from app.repository.entity.service_entity import ServiceEntity
from app.repository.service_repository import ServiceRepository
from bson import ObjectId
from pymongo.results import InsertOneResult, UpdateResult, DeleteResult


class ServiceRepositoryUnitTest(unittest.TestCase):
    def setUp(self):
        self.collection_mock = MagicMock()
        self.service_repository = ServiceRepository(collection=self.collection_mock)
        self.service_id = ObjectId("6554b34d82161e93bff08df3")
        self.service = ServiceEntity(
            _id=self.service_id,
            service_name="Atlassian",
            safe_keywords=["Jira", "Sourcetree", "Opsgenie", "Trello", "Confluence", "Bitbucket"],
            hint_keywords=["roadmaps", "marketplace"]
        )

    def test_create_service(self):
        result_exp = InsertOneResult(inserted_id=self.service_id, acknowledged=True)
        self.collection_mock.insert_one.return_value = result_exp
        result_act = self.service_repository.create_service(service=self.service)
        self.assertEqual(result_exp, result_act, "wrong result of create_service()")
        self.collection_mock.insert_one.assert_called_once_with(document=self.service)

    def test_read_one_service(self):
        result_exp = [self.service]
        self.collection_mock.find.return_value = result_exp
        result_act = self.service_repository.read_services(service_id=self.service_id)
        self.assertEqual(result_exp, result_act, "wrong result of read_services()")
        self.collection_mock.find.assert_called_once_with(
            filter={"_id": self.service_id}
        )

    def test_read_all_services(self):
        result_exp = [self.service, self.service]
        self.collection_mock.find.return_value = result_exp
        result_act = self.service_repository.read_services()
        self.assertEqual(result_exp, result_act, "wrong result of read_services()")
        self.collection_mock.find.assert_called_once_with(filter=None)

    def test_update_service(self):
        result_exp = UpdateResult(raw_result=self.service, acknowledged=True)
        self.collection_mock.replace_one.return_value = result_exp
        result_act = self.service_repository.update_service(
            service_id=self.service_id, service=self.service
        )
        self.assertEqual(result_exp, result_act, "wrong result of update_service()")
        self.collection_mock.replace_one.assert_called_once_with(
            filter={"_id": self.service_id}, replacement=self.service, upsert=True
        )

    def test_delete_service(self):
        result_exp = DeleteResult(raw_result=self.service, acknowledged=True)
        self.collection_mock.delete_one.return_value = result_exp
        result_act = self.service_repository.delete_service(service_id=self.service_id)
        self.assertEqual(result_exp, result_act, "wrong result of delete_service()")
        self.collection_mock.delete_one.assert_called_once_with(
            filter={"_id": self.service_id}
        )
