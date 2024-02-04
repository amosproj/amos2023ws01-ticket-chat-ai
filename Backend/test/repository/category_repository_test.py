import unittest
from unittest.mock import MagicMock

from app.repository.category_repository import CategoryRepository
from app.repository.entity.category_entity import CategoryEntity
from bson import ObjectId
from pymongo.results import InsertOneResult, DeleteResult


class CategoryRepositoryUnitTest(unittest.TestCase):
    def setUp(self):
        self.collection_mock = MagicMock()
        self.category_repository = CategoryRepository(collection=self.collection_mock)
        self.category_id = ObjectId("6554b34d82161e93bff08df3")
        self.category = CategoryEntity(
            _id=self.category_id,
            name="Technical Issues"
        )

    def test_create_category(self):
        result_exp = InsertOneResult(inserted_id=self.category_id, acknowledged=True)
        self.collection_mock.insert_one.return_value = result_exp
        result_act = self.category_repository.create_category(category=self.category)
        self.assertEqual(result_exp, result_act, "wrong result of create_category()")
        self.collection_mock.insert_one.assert_called_once_with(document=self.category)

    def test_read_one_category(self):
        result_exp = [self.category]
        self.collection_mock.find.return_value = result_exp
        result_act = self.category_repository.read_categories(category_id=self.category_id)
        self.assertEqual(result_exp, result_act, "wrong result of read_categories()")
        self.collection_mock.find.assert_called_once_with(
            filter={"_id": self.category_id}
        )

    def test_read_all_categories(self):
        result_exp = [self.category, self.category]
        self.collection_mock.find.return_value = result_exp
        result_act = self.category_repository.read_categories()
        self.assertEqual(result_exp, result_act, "wrong result of read_categories()")
        self.collection_mock.find.assert_called_once_with(filter=None)

    def test_delete_category(self):
        result_exp = DeleteResult(raw_result=self.category, acknowledged=True)
        self.collection_mock.delete_one.return_value = result_exp
        result_act = self.category_repository.delete_category(category_id=self.category_id)
        self.assertEqual(result_exp, result_act, "wrong result of delete_category()")
        self.collection_mock.delete_one.assert_called_once_with(
            filter={"_id": self.category_id}
        )
