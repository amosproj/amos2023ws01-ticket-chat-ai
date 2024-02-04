import json
import os
from unittest import TestCase
from unittest.mock import MagicMock

from app.api.dto.ticket import Ticket
from app.dependency.collection import get_ticket_collection, get_user_collection
from app.dependency.email_service import get_email_service
from app.enum.customer_prio import CustomerPrio
from app.enum.prio import Prio
from app.enum.state import State
from app.main import app
from app.repository.entity.ticket_entity import TicketEntity
from bson import ObjectId
from fastapi.testclient import TestClient
from pymongo.results import InsertOneResult, UpdateResult
from starlette import status


class TicketAPIIntegrationTest(TestCase):
    def override_get_ticket_collection(self):
        return self.ticket_collection_mock

    def override_get_user_collection(self):
        return self.user_collection_mock

    def override_get_email_service(self):
        return self.email_service_mock

    def setUp(self):
        self.client = TestClient(app)
        self.ticket_collection_mock = MagicMock()
        self.user_collection_mock = MagicMock()
        self.email_service_mock = MagicMock()
        app.dependency_overrides = {
            get_ticket_collection: self.override_get_ticket_collection,
            get_user_collection: self.override_get_user_collection,
            get_email_service: self.override_get_email_service,
        }
        self.ticket_id = ObjectId("6554b34d82161e93bff08df6")
        self.file_name = "__init__.py"
        self.file_path = os.path.join(os.path.dirname(__file__), self.file_name)

    def test_process_text_without_email_success(self):
        # Define
        ticket_entity = TicketEntity(
            _id=self.ticket_id,
            title="Test Ticket",
            service="Fürth",
            category="",
            keywords=[],
            customerPriority=CustomerPrio.can_work,
            affectedPerson="",
            description="",
            priority=Prio.low,
            attachments=[],
            requestType="",
            state=State.draft,
        )
        insert_one_result = InsertOneResult(
            inserted_id=self.ticket_id, acknowledged=True
        )
        text_input = {"text": "Hello from the test!"}
        exp_ticket = Ticket(
            id=str(self.ticket_id),
            title="Test Ticket",
            service="Fürth",
            category="",
            keywords=[],
            customerPriority=CustomerPrio.can_work,
            affectedPerson="",
            description="",
            priority=Prio.low,
            attachmentNames=[],
            requestType="",
            state=State.draft,
        )

        # Define mock behavior
        self.ticket_collection_mock.insert_one.return_value = insert_one_result
        self.ticket_collection_mock.find.return_value = [ticket_entity]

        # Act
        response = self._run_process_text_endpoint(text_input)

        # Assert
        # Mocks
        self.ticket_collection_mock.insert_one.assert_called_once()
        self.ticket_collection_mock.find.assert_called_once()
        # Response
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(exp_ticket, Ticket.parse_obj(response.json()))

    def test_process_text_empty_input(self):
        # Define your test data with an empty "text" field
        text_input = {"text": ""}
        exp_json = {"detail": "Text is required"}

        # Send a POST request to the "/text" endpoint with the correct content type header
        response = self._run_process_text_endpoint(text_input)

        # Check if the response status code is 400 (Bad Request)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

        # Check if the response contains the expected error message
        self.assertEqual(exp_json, response.json())

    def test_update_ticket_attachments_success(self):
        # Define
        ticket_entity = TicketEntity(
            _id=self.ticket_id,
            title="Test Ticket",
            service="Fürth",
            category="",
            keywords=[],
            customerPriority=CustomerPrio.can_work,
            affectedPerson="",
            description="",
            priority=Prio.low,
            attachments=[],
            requestType="",
        )
        update_result = UpdateResult(raw_result=ticket_entity, acknowledged=True)
        exp_ticket = Ticket(
            id=str(self.ticket_id),
            title="Test Ticket",
            service="Fürth",
            category="",
            keywords=[],
            customerPriority=CustomerPrio.can_work,
            affectedPerson="",
            description="",
            priority=Prio.low,
            attachmentNames=[self.file_name],
            requestType="",
        )

        # Define mock behavior
        self.ticket_collection_mock.find.return_value = [ticket_entity]
        self.ticket_collection_mock.replace_one.return_value = update_result

        # Act
        response = self._run_update_ticket_attachments(ticket_id=str(self.ticket_id))

        # Assert
        # Mocks
        self.ticket_collection_mock.find.assert_called_once()
        self.ticket_collection_mock.replace_one.assert_called_once()
        # Response
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(exp_ticket, Ticket.parse_obj(response.json()))

    def test_update_ticket_attachments_invalid_ticket_id(self):
        exp_json = {"detail": "Received empty or invalid ticket id of type ObjectId!"}

        response = self._run_update_ticket_attachments(ticket_id="-")

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual(exp_json, response.json())

    def test_update_ticket_attributes_state_draft_success(self):
        # Define
        ticket_entity = TicketEntity(
            _id=self.ticket_id,
            title="Test Ticket",
            service="",
            category="",
            keywords=[],
            customerPriority=CustomerPrio.can_work,
            affectedPerson="",
            description="",
            priority=Prio.low,
            attachments=[],
            requestType="",
            state=State.draft,
        )
        update_result = UpdateResult(raw_result=ticket_entity, acknowledged=True)

        wrapped_ticket_json = {
            "email": "testEmail@talxTix.com",
            "ticket": {
                "id": "6554b34d82161e93bff08df6",
                "title": "Test Ticket",
                "service": "",
                "category": "",
                "keywords": [],
                "customerPriority": CustomerPrio.can_work,
                "affectedPerson": "",
                "description": "",
                "priority": Prio.low,
                "attachments": [],
                "requestType": "Incident",
                "state": State.draft,
            },
        }

        exp_ticket = Ticket(
            id=str(self.ticket_id),
            title="Test Ticket",
            service="",
            category="",
            keywords=[],
            customerPriority=CustomerPrio.can_work,
            affectedPerson="",
            description="",
            priority=Prio.low,
            attachmentNames=[],
            requestType="Incident",
            state=State.draft,
        )

        # Define mock behavior
        self.ticket_collection_mock.find.return_value = [ticket_entity]
        self.ticket_collection_mock.replace_one.return_value = update_result

        # Act
        response = self._run_update_ticket_attributes(
            ticket_id=str(self.ticket_id), wrapped_ticket=wrapped_ticket_json
        )

        # Assert
        # Mocks
        self.ticket_collection_mock.find.assert_called_once()
        self.ticket_collection_mock.replace_one.assert_called_once()
        # Response
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertDictEqual(exp_ticket.dict(), response.json())

    def test_update_ticket_attributes_state_accepted_success(self):
        # Define
        ticket_entity = TicketEntity(
            _id=self.ticket_id,
            title="Test Ticket",
            service="",
            category="",
            keywords=[],
            customerPriority=CustomerPrio.can_work,
            affectedPerson="",
            description="",
            priority=Prio.low,
            attachments=[],
            requestType="",
            state=State.accepted,
        )
        update_result = UpdateResult(raw_result=ticket_entity, acknowledged=True)

        wrapped_ticket_json = {
            "email": "testEmail@talxTix.com",
            "ticket": {
                "id": "6554b34d82161e93bff08df6",
                "title": "Test Ticket",
                "service": "",
                "category": "",
                "keywords": [],
                "customerPriority": CustomerPrio.can_work,
                "affectedPerson": "",
                "description": "",
                "priority": Prio.low,
                "attachments": [],
                "requestType": "Incident",
                "state": State.accepted,
            },
        }

        exp_ticket = Ticket(
            id=str(self.ticket_id),
            title="Test Ticket",
            service="",
            category="",
            keywords=[],
            customerPriority=CustomerPrio.can_work,
            affectedPerson="",
            description="",
            priority=Prio.low,
            attachmentNames=[],
            requestType="Incident",
            state=State.accepted,
        )

        # Define mock behavior
        self.ticket_collection_mock.find.return_value = [ticket_entity]
        self.ticket_collection_mock.replace_one.return_value = update_result

        # Act
        response = self._run_update_ticket_attributes(
            ticket_id=str(self.ticket_id), wrapped_ticket=wrapped_ticket_json
        )

        # Assert
        # Mocks
        self.ticket_collection_mock.find.assert_called_once()
        self.ticket_collection_mock.replace_one.assert_called_once()
        self.email_service_mock.send_email.assert_called_once()
        # Response
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertDictEqual(exp_ticket.dict(), response.json())

    def test_update_ticket_attributes_invalid_ticket_id(self):
        exp_json = {"detail": "Received empty or invalid ticket id of type ObjectId!"}

        response = self._run_update_ticket_attributes(
            ticket_id="-", wrapped_ticket=None
        )

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual(exp_json, response.json())

    def _run_process_text_endpoint(self, text_input: dict):
        return self.client.post(
            "/api/v1/ticket/text",
            data=json.dumps(text_input),
            headers={"Content-Type": "application/json"},
        )

    def _run_update_ticket_attachments(self, ticket_id: str):
        return self.client.put(
            f"/api/v1/ticket/{ticket_id}/attachments",
            files=[
                ("files", open(self.file_path, "rb")),
            ],
        )

    def _run_update_ticket_attributes(
        self, ticket_id: str, wrapped_ticket: dict | None
    ):
        return self.client.put(
            f"/api/v1/ticket/{ticket_id}/update",
            json=wrapped_ticket,
            headers={"Content-Type": "application/json"},
        )
