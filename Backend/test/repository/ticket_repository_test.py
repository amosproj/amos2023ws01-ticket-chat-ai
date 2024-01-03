import configparser
import unittest
from unittest.mock import MagicMock

import pytest
from bson import ObjectId
from pymongo import MongoClient
from pymongo.results import InsertOneResult, UpdateResult, DeleteResult

from app.enum.customer_prio import CustomerPrio
from app.enum.prio import Prio
from app.repository.entity.ticket_entity import TicketEntity
from app.repository.ticket_repository import TicketRepository
from app.util.database_routine import start_server, stop_server
from test.config.pytest import SKIP_TEST


class TicketRepositoryUnitTest(unittest.TestCase):
    def setUp(self):
        self.collection_mock = MagicMock()
        self.ticket_repository = TicketRepository(collection=self.collection_mock)
        self.ticket_id = ObjectId("6554b34d82161e93bff08df3")
        self.ticket = TicketEntity(
            _id=self.ticket_id,
            title="Test Ticket",
            service="Test the test ticket",
            category="",
            keywords=[],
            customerPriority=CustomerPrio.can_work,
            affectedPerson="",
            description="",
            priority=Prio.low,
            attachments=[],
        )

    def test_create_ticket(self):
        result_exp = InsertOneResult(inserted_id=self.ticket_id, acknowledged=True)
        self.collection_mock.insert_one.return_value = result_exp
        result_act = self.ticket_repository.create_ticket(ticket=self.ticket)
        self.assertEqual(result_exp, result_act, "wrong result of create_ticket()")
        self.collection_mock.insert_one.assert_called_once_with(document=self.ticket)

    def test_read_one_ticket(self):
        result_exp = [self.ticket]
        self.collection_mock.find.return_value = result_exp
        result_act = self.ticket_repository.read_tickets(ticket_id=self.ticket_id)
        self.assertEqual(result_exp, result_act, "wrong result of read_tickets()")
        self.collection_mock.find.assert_called_once_with(
            filter={"_id": self.ticket_id}
        )

    def test_read_all_tickets(self):
        result_exp = [self.ticket, self.ticket]
        self.collection_mock.find.return_value = result_exp
        result_act = self.ticket_repository.read_tickets()
        self.assertEqual(result_exp, result_act, "wrong result of read_tickets()")
        self.collection_mock.find.assert_called_once_with(filter=None)

    def test_update_ticket(self):
        result_exp = UpdateResult(raw_result=self.ticket, acknowledged=True)
        self.collection_mock.replace_one.return_value = result_exp
        result_act = self.ticket_repository.update_ticket(
            ticket_id=self.ticket_id, ticket=self.ticket
        )
        self.assertEqual(result_exp, result_act, "wrong result of update_ticket()")
        self.collection_mock.replace_one.assert_called_once_with(
            filter={"_id": self.ticket_id}, replacement=self.ticket, upsert=True
        )

    def test_delete_ticket(self):
        result_exp = DeleteResult(raw_result=self.ticket, acknowledged=True)
        self.collection_mock.delete_one.return_value = result_exp
        result_act = self.ticket_repository.delete_ticket(ticket_id=self.ticket_id)
        self.assertEqual(result_exp, result_act, "wrong result of delete_ticket()")
        self.collection_mock.delete_one.assert_called_once_with(
            filter={"_id": self.ticket_id}
        )


@pytest.mark.skipif(condition=SKIP_TEST, reason="Database is missing")
class TicketRepositoryIntegrationTest(unittest.TestCase):
    def setUp(self):
        config = configparser.ConfigParser()
        config.read("config.ini")
        mongodb_url = config["DEFAULT"]["MONGODB_URL"]
        client = MongoClient(mongodb_url)
        db = client.talktix
        collection = db.ticket
        self.ticket_repository = TicketRepository(collection)
        self.ticket = {
            "title": "Test Ticket",
            "service": "Test the test ticket",
            "category": "",
            "keywords": [],
            "customerPriority": CustomerPrio.can_work,
            "affectedPerson": "",
            "description": "",
            "priority": Prio.low,
            "attachments": [],
        }

    def test_crud(self):
        # start db server
        system_status = start_server()
        assert system_status == 0

        # determine number of tickets in collection
        num_tickets = len(self.ticket_repository.read_tickets())
        assert num_tickets is not None

        # create ticket
        ticket_id = self.ticket_repository.create_ticket(ticket=self.ticket).inserted_id
        assert ticket_id is not None

        # read created ticket
        tickets = self.ticket_repository.read_tickets(ticket_id=ticket_id)
        assert len(tickets) == 1 and tickets[0]["_id"] == ticket_id

        # update ticket
        updated_ticket: TicketEntity = self.ticket.copy()
        updated_ticket["priority"] = Prio.medium
        update_result = self.ticket_repository.update_ticket(
            ticket_id=ticket_id, ticket=updated_ticket
        )
        assert update_result.modified_count == 1

        # read updated ticket
        tickets = self.ticket_repository.read_tickets(ticket_id=ticket_id)
        assert len(tickets) == 1 and tickets[0]["priority"] == Prio.medium

        # delete ticket
        delete_result = self.ticket_repository.delete_ticket(ticket_id=ticket_id)
        assert delete_result.deleted_count == 1

        # determine number of tickets in collection again
        new_num_tickets = len(self.ticket_repository.read_tickets())
        assert new_num_tickets == num_tickets

        # stop db server
        system_status = stop_server()
        assert system_status == 0
