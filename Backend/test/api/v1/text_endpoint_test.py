import json

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_process_text():
    # Define your test data with "text" as a string
    data = {"text": "Hello from the test!"}

    # Send a POST request to the "/text" endpoint with the correct content type header
    response = client.post(
        "/api/v1/text",
        data=json.dumps(data),
        headers={"Content-Type": "application/json"},
    )

    # Check if the response status code is 200
    assert response.status_code == 200

    # Check if the response contains the expected data
    assert response.json().get("data") == "Message was received"

    # Check if the response was generated by the model
    assert "Generated response:" in response.json().get("text")


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
