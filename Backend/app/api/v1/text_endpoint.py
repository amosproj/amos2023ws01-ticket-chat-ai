import json

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends

from app.dependency.ticket_db_service import get_ticket_db_service
from app.dependency.trained_t5_model import get_trained_t5_model
from app.dto.text_input import TextInput
from app.dto.text_response import TextResponse
from app.model.t5.use_trained_t5_model import TrainedT5Model
from app.persistence.ticket_db_service import TicketDBService

router = APIRouter()


@router.post("/text")
async def process_text(text_input: TextInput, trained_t5_model: TrainedT5Model = Depends(get_trained_t5_model),
                       ticket_db_service: TicketDBService = Depends(get_ticket_db_service)):
    """
    Receive Text from the Frontend

    Args:
    - text_input (TextInput): A Pydantic model defining the expected input format containing the 'text' field.

    Returns:
    - TextResponse: A response containing the received text and a status code.

    Raises:
    - HTTPException: If 'text' field is empty, returns a 400 Bad Request with an error message.
    """
    # Check if the 'text' field is empty
    if not text_input.text:
        raise HTTPException(status_code=400, detail="Text is required")

    # Run the model to process the input text
    received_dict = trained_t5_model.run_model(text_input.text)

    # Save the ticket to the database using the TicketDBService
    created_ticket = ticket_db_service.save_ticket(received_dict)

    if created_ticket:
        response_data = "Message was received and ticket created"
        status_code = 200
    else:
        response_data = "Ticket creation failed"
        status_code = 500

    return TextResponse(
        data=response_data, text=json.dumps(received_dict), code=status_code
    )
