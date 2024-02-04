import unittest
from unittest.mock import MagicMock

from app.repository.department_repository import DepartmentRepository
from app.repository.entity.department_entity import DepartmentEntity
from bson import ObjectId
from pymongo.results import InsertOneResult


class DepartmentRepositoryUnitTest(unittest.TestCase):
    def setUp(self):
        self.collection_mock = MagicMock()
        self.department_repository = DepartmentRepository(collection=self.collection_mock)
        self.department_id = ObjectId("6554b34d82161e93bff08df3")
        self.department = DepartmentEntity(
            _id=self.department_id,
            name="Technical Issues"
        )

    def test_create_department(self):
        result_exp = InsertOneResult(inserted_id=self.department_id, acknowledged=True)
        self.collection_mock.insert_one.return_value = result_exp
        result_act = self.department_repository.create_department(department=self.department)
        self.assertEqual(result_exp, result_act, "wrong result of create_department()")
        self.collection_mock.insert_one.assert_called_once_with(document=self.department)

    def test_read_one_department(self):
        result_exp = [self.department]
        self.collection_mock.find.return_value = result_exp
        result_act = self.department_repository.read_departments(department_id=self.department_id)
        self.assertEqual(result_exp, result_act, "wrong result of read_departments()")
        self.collection_mock.find.assert_called_once_with(
            filter={"_id": self.department_id}
        )

    def test_read_all_departments(self):
        result_exp = [self.department, self.department]
        self.collection_mock.find.return_value = result_exp
        result_act = self.department_repository.read_departments()
        self.assertEqual(result_exp, result_act, "wrong result of read_departments()")
        self.collection_mock.find.assert_called_once_with(filter=None)
