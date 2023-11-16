from fastapi import APIRouter, HTTPException

from app.dto.text_input import TextInput
from app.dto.text_response import TextResponse
from app.model.t5.use_trained_t5_model import TrainedT5Model
from app.persistence.ticket_repository import TicketRepository
from app.dto.ticket import Ticket

router = APIRouter()
ticket_ds = TicketRepository()

@router.post("/text")
async def process_text(text_input: TextInput):
    """
    Receive Text from the Frontend

    Args:
    - text_input (TextInput): A Pydantic model defining the expected input format containing the 'text' field.

    Returns:
    - TextResponse: A response containing the received text, a status code, and the ticket ID.

    Raises:
    - HTTPException: If 'text' field is empty, returns a 400 Bad Request with an error message.
    """
    if not text_input.text:
        raise HTTPException(status_code=400, detail="Text is required")

    # run model
    trained_t5_model = TrainedT5Model()
    received_text = trained_t5_model.run_model(text_input.text)

    # save the ticket to the database
    created_ticket_id = 1 # ticket_ds.create_ticket(ticket=Ticket(**text_input.dict())).inserted_id

    # print the received text for debugging or logging purposes
    print(f"Received Text: {received_text}")

    # respond with a simple message, a status code, and the ticket ID
    response_data = "Message was received"
    status_code = 200

    return TextResponse(data=response_data, text=received_text, code=status_code, ticket_id=str(created_ticket_id))
