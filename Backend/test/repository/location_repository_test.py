import unittest
from unittest.mock import MagicMock

from app.repository.entity.location_entity import LocationEntity
from app.repository.location_repository import LocationRepository
from bson import ObjectId
from pymongo.results import InsertOneResult


class LocationRepositoryUnitTest(unittest.TestCase):
    def setUp(self):
        self.collection_mock = MagicMock()
        self.location_repository = LocationRepository(collection=self.collection_mock)
        self.location_id = ObjectId("6554b34d82161e93bff08df3")
        self.location = LocationEntity(_id=self.location_id, name="Frankfurt")

    def test_create_location(self):
        result_exp = InsertOneResult(inserted_id=self.location_id, acknowledged=True)
        self.collection_mock.insert_one.return_value = result_exp
        result_act = self.location_repository.create_location(location=self.location)
        self.assertEqual(result_exp, result_act, "wrong result of create_location()")
        self.collection_mock.insert_one.assert_called_once_with(document=self.location)

    def test_read_one_location(self):
        result_exp = [self.location]
        self.collection_mock.find.return_value = result_exp
        result_act = self.location_repository.read_locations(
            location_id=self.location_id
        )
        self.assertEqual(result_exp, result_act, "wrong result of read_locations()")
        self.collection_mock.find.assert_called_once_with(
            filter={"_id": self.location_id}
        )

    def test_read_all_locations(self):
        result_exp = [self.location, self.location]
        self.collection_mock.find.return_value = result_exp
        result_act = self.location_repository.read_locations()
        self.assertEqual(result_exp, result_act, "wrong result of read_locations()")
        self.collection_mock.find.assert_called_once_with(filter=None)
