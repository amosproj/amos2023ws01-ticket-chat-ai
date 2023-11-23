from fastapi import APIRouter, HTTPException
from app.dto.text_input import TextInput
from app.dto.text_response import TextResponse
from app.model.t5.use_trained_t5_model import TrainedT5Model
from app.dto.ticket import Ticket
from app.persistence.ticket_db_service import TicketDBService
import json
from app.logger import logger

router = APIRouter()


@router.post("/text")
async def process_text(text_input: TextInput):
    """
    Receive Text from the Frontend

    Args:
    - text_input (TextInput): A Pydantic model defining the expected input format containing the 'text' field.

    Returns:
    - TextResponse: A response containing the received text and a status code.

    Raises:
    - HTTPException: If 'text' field is empty, returns a 400 Bad Request with an error message.
    """
    logger.info("Processing text...")

    # Check if the 'text' field is empty
    if not text_input.text:
        logger.error("Received empty text!")
        raise HTTPException(status_code=400, detail="Text is required")

    logger.info(f"Received text: {text_input.text}")

    logger.info("Running the model...")
    # Run the model to process the input text
    trained_t5_model = TrainedT5Model()
    received_dict = trained_t5_model.run_model(text_input.text)
    logger.info("Model execution complete. Result: %s", received_dict)

    logger.info("Saving ticket to the database...")
    # Save the ticket to the database using the TicketDBService
    ticket_db_service = TicketDBService()
    created_ticket = ticket_db_service.save_ticket(received_dict)

    if created_ticket:
        ticket_id = created_ticket.inserted_id
        logger.info(f"Ticket created and saved successfully. Ticket ID: {ticket_id}")
        response_data = "Message was received and ticket created"
        status_code = 200
    else:
        logger.error("Ticket creation failed.")
        response_data = "Ticket creation failed"
        status_code = 500

    logger.info("Preparing response...")
    response_json = json.dumps(received_dict)
    return TextResponse(data=response_data, text=response_json, code=status_code)
