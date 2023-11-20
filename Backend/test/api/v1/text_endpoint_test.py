import json
import unittest
from unittest.mock import patch

from bson import ObjectId
from fastapi.testclient import TestClient
from pymongo.results import InsertOneResult

from app.config.ticket_repository_config import get_ticket_repository
from app.main import app


class TextEndpointUnitTest(unittest.TestCase):
    def override_get_ticket_repository(self):
        return self.ticket_repository_mock

    @patch("app.persistence.ticket_repository.TicketRepository")
    def setUp(self, ticket_repository_mock):
        self.ticket_repository_mock = ticket_repository_mock
        self.client = TestClient(app)
        app.dependency_overrides = {get_ticket_repository: self.override_get_ticket_repository}

    def test_process_text(self):
        # Define mock behavior
        self.ticket_repository_mock.create_ticket.return_value = InsertOneResult(
            inserted_id=ObjectId("6554b34d82161e93bff08df3"),
            acknowledged=True
        )

        # Define your test data with "text" as a string
        data = {"text": "Hello from the test!"}

        # Send a POST request to the "/text" endpoint with the correct content type header
        response = self.client.post(
            "/api/v1/text",
            data=json.dumps(data),
            headers={"Content-Type": "application/json"},
        )

        # Check if the response status code is 200
        assert response.status_code == 200

        # Check if the response contains the expected data
        assert response.json().get("data") == "Message was received and ticket created"

        # Check if the ticket information is included in the response
        assert "title" in response.json().get("text")

    def test_process_text_empty_input(self):
        # Define your test data with an empty "text" field
        data = {"text": ""}

        # Send a POST request to the "/text" endpoint with the correct content type header
        response = self.client.post(
            "/api/v1/text",
            data=json.dumps(data),
            headers={"Content-Type": "application/json"},
        )

        # Check if the response status code is 400 (Bad Request)
        assert response.status_code == 400

        # Check if the response contains the expected error message
        assert response.json() == {"detail": "Text is required"}
