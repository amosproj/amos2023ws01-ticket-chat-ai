from fastapi.testclient import TestClient
import json

from unittest.mock import MagicMock, patch

from bson import ObjectId
from pymongo.results import InsertOneResult
from app.dto.enum.customer_prio import CustomerPrio
from app.dto.enum.prio import Prio
from app.dto.ticket import Ticket
from app.persistence.ticket_db_service import TicketDBService

from app.main import app

client = TestClient(app)


@patch("app.api.v1.text_endpoint.TrainedT5Model")
@patch("app.api.v1.text_endpoint.TicketDBService")
def test_process_text(ticket_service_mock, trained_t5_model_mock):
    # Arrange
    # Define your test data with "text" as a string
    data = {"text": "Hello from the test!"}

    mock_return_value = Ticket(
        title="Test Ticket",
        location="Test the test ticket",
        category="",
        keywords=[],
        customerPriority=CustomerPrio.can_work,
        affectedPerson="",
        description="",
        priority=Prio.low,
    )

    trained_t5_model_mock.return_value.run_model.return_value = mock_return_value.dict()

    ticket_service_mock = MagicMock()
    ticket_id = ObjectId("6554b34d82161e93bff08df6")
    result_exp = InsertOneResult(inserted_id=ticket_id, acknowledged=True)
    ticket_service_mock.save_ticket.return_value = result_exp

    # Act
    response = client.post(
        "/api/v1/text",
        data=json.dumps(data),
        headers={"Content-Type": "application/json"},
    )

    # Assert
    assert response.status_code == 200
    assert response.json().get("data") == "Message was received and ticket created"


def test_process_text_empty_input():
    # Define your test data with an empty "text" field
    data = {"text": ""}

    # Send a POST request to the "/text" endpoint with the correct content type header
    response = client.post(
        "/api/v1/text",
        data=json.dumps(data),
        headers={"Content-Type": "application/json"},
    )

    # Check if the response status code is 400 (Bad Request)
    assert response.status_code == 400

    # Check if the response contains the expected error message
    assert response.json() == {"detail": "Text is required"}
