from unittest import TestCase
from unittest.mock import MagicMock

from bson import ObjectId
from fastapi import HTTPException
from pymongo.results import InsertOneResult
from starlette import status

from app.api.dto.ticket import Ticket
from app.enum.customer_prio import CustomerPrio
from app.enum.prio import Prio
from app.repository.entity.ticket_entity import TicketEntity
from app.service.ticket_db_service import TicketDBService


class TicketDBServiceUnitTest(TestCase):
    def setUp(self):
        self.ticket_repository_mock = MagicMock()
        self.ticket_db_service = TicketDBService(
            ticket_repository=self.ticket_repository_mock
        )
        self.ticket_dict = {
            "title": "Test Ticket",
            "location": "Test the test ticket",
            "category": "",
            "keywords": [],
            "customerPriority": CustomerPrio.can_work,
            "affectedPerson": "",
            "description": "",
            "priority": Prio.low,
        }
        self.ticket_id = ObjectId("6554b34d82161e93bff08df3")
        self.ticket_entity = TicketEntity(
            _id=self.ticket_id,
            title="Test Ticket",
            location="Test the test ticket",
            category="",
            keywords=[],
            customerPriority=CustomerPrio.can_work,
            affectedPerson="",
            description="",
            priority=Prio.low,
            attachments=[],
        )

    def test_create_ticket_success(self):
        # Define
        insert_one_result = InsertOneResult(
            inserted_id=self.ticket_id, acknowledged=True
        )
        exp_ticket = Ticket(
            id=str(self.ticket_id),
            title="Test Ticket",
            location="Test the test ticket",
            category="",
            keywords=[],
            customerPriority=CustomerPrio.can_work,
            affectedPerson="",
            description="",
            priority=Prio.low,
            attachmentNames=[],
        )

        # Mock
        self.ticket_repository_mock.create_ticket.return_value = insert_one_result
        self.ticket_repository_mock.read_tickets.return_value = [self.ticket_entity]

        # Act
        act_ticket = self.ticket_db_service.create_ticket(
            ticket_entity=self.ticket_dict
        )

        # Expect
        self.ticket_repository_mock.create_ticket.assert_called_once()
        self.ticket_repository_mock.read_tickets.assert_called_once()
        self.assertEqual(act_ticket, exp_ticket, "Tickets are not equal.")

    def test_create_ticket_creation_failed(self):
        # Define
        insert_one_result = InsertOneResult(
            inserted_id=self.ticket_id, acknowledged=False
        )
        exp_status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        exp_detail = "Ticket creation failed."

        # Mock
        self.ticket_repository_mock.create_ticket.return_value = insert_one_result

        # Act
        with self.assertRaises(HTTPException) as cm:
            self.ticket_db_service.create_ticket(ticket_entity=self.ticket_dict)
        act_exception = cm.exception

        # Expect
        self.assertEqual(act_exception.status_code, exp_status_code)
        self.assertEqual(act_exception.detail, exp_detail)
        self.ticket_repository_mock.create_ticket.assert_called_once()

    def test_create_ticket_not_found(self):
        # Define
        insert_one_result = InsertOneResult(
            inserted_id=self.ticket_id, acknowledged=True
        )
        exp_status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        exp_detail = f"Ticket with id {str(self.ticket_id)} not found."

        # Mock
        self.ticket_repository_mock.create_ticket.return_value = insert_one_result
        self.ticket_repository_mock.read_tickets.return_value = []

        # Act
        with self.assertRaises(HTTPException) as cm:
            self.ticket_db_service.create_ticket(ticket_entity=self.ticket_dict)
        act_exception = cm.exception

        # Expect
        self.assertEqual(act_exception.status_code, exp_status_code)
        self.assertEqual(act_exception.detail, exp_detail)
        self.ticket_repository_mock.create_ticket.assert_called_once()
        self.ticket_repository_mock.read_tickets.assert_called_once()
