import json
import unittest
from unittest.mock import MagicMock

from bson import ObjectId
from fastapi.testclient import TestClient
from pymongo.results import InsertOneResult

from app.api.v1.ticket_api import process_text
from app.dependency.collection import get_ticket_collection
from app.enum.customer_prio import CustomerPrio
from app.enum.prio import Prio
from app.api.dto.text_input import TextInput
from app.repository.entity.ticket_entity import TicketEntity
from app.main import app


class TextEndpointUnitTest(unittest.TestCase):
    def setUp(self):
        self.ticket_db_service_mock = MagicMock()
        self.trained_t5_model_mock = MagicMock()

    async def test_process_text(self):
        # Arrange
        # Define your test data with "text" as a string
        text_input = TextInput(text="Hello from the test!")

        ticket = TicketEntity(
            _id=ObjectId(),
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

        ticket_id = ObjectId("6554b34d82161e93bff08df6")
        result_exp = InsertOneResult(inserted_id=ticket_id, acknowledged=True)

        # Define mock behavior
        self.trained_t5_model_mock.return_value.run_model.return_value = ticket.dict()
        self.ticket_db_service_mock.save_ticket.return_value = result_exp

        # Act
        response = await process_text(
            text_input=text_input,
            ticket_db_service=self.ticket_db_service_mock,
            trained_t5_model=self.trained_t5_model_mock,
        )

        # Assert
        # Mocks
        self.trained_t5_model_mock.return_value.run_model.assert_called_once_with(
            text_input.text
        )
        self.ticket_db_service_mock.save_ticket.assert_called_once_with(ticket.dict())
        # Response
        assert response.code == 200
        assert response.data == "Message was received and ticket created"


class TextEndpointIntegrationTest(unittest.TestCase):
    def override_get_ticket_collection(self):
        return self.collection_mock

    def setUp(self):
        self.client = TestClient(app)
        self.collection_mock = MagicMock()
        app.dependency_overrides = {
            get_ticket_collection: self.override_get_ticket_collection
        }

    def test_process_text(self):
        # Arrange
        # Define your test data with "text" as a string
        data = {"text": "Hello from the test!"}

        ticket_id = ObjectId("6554b34d82161e93bff08df6")
        result_exp = InsertOneResult(inserted_id=ticket_id, acknowledged=True)

        ticket_exp = TicketEntity(
            _id=ticket_id,
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

        # Define mock behavior
        self.collection_mock.insert_one.return_value = result_exp
        self.collection_mock.find.return_value = [ticket_exp]

        # Act
        response = self.client.post(
            "/api/v1/ticket/text",
            data=json.dumps(data),
            headers={"Content-Type": "application/json"},
        )

        # Assert
        # Mocks
        self.collection_mock.insert_one.assert_called_once()
        self.collection_mock.find.assert_called_once_with(filter={"_id": ticket_id})
        # Response
        assert response.status_code == 201
        assert response.json().get("id") == str(ticket_id)

    def test_process_text_empty_input(self):
        # Define your test data with an empty "text" field
        data = {"text": ""}

        # Send a POST request to the "/text" endpoint with the correct content type header
        response = self.client.post(
            "/api/v1/ticket/text",
            data=json.dumps(data),
            headers={"Content-Type": "application/json"},
        )

        # Check if the response status code is 400 (Bad Request)
        assert response.status_code == 400

        # Check if the response contains the expected error message
        assert response.json() == {"detail": "Text is required"}
