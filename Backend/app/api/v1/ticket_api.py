from typing import Annotated

from bson import ObjectId
from fastapi import APIRouter, HTTPException, UploadFile
from fastapi.params import Depends, File, Form, Body, Path

from app.dependency.ticket_db_service import get_ticket_db_service
from app.dependency.trained_t5_model import get_trained_t5_model
from app.dto.text_input import TextInput
from app.dto.text_response import TextResponse
from app.model.t5.use_trained_t5_model import TrainedT5Model
from app.persistence.ticket_db_service import TicketDBService
import json
from app.logger import logger

router = APIRouter()


@router.post("/ticket/text")
async def process_text(
    text_input: TextInput,
    trained_t5_model: TrainedT5Model = Depends(get_trained_t5_model),
    ticket_db_service: TicketDBService = Depends(get_ticket_db_service)
):
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
    received_dict = trained_t5_model.run_model(text_input.text)
    logger.info("Model execution complete. Result: %s", received_dict)

    logger.info("Saving ticket to the database...")
    # Save the ticket to the database using the TicketDBService
    created_ticket = ticket_db_service.create_ticket(received_dict)

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


@router.put("/ticket/{ticket_id}/attachments")
async def update_ticket_attachments(
    ticket_id: str = Path(default=""),
    files: list[UploadFile] = File(default=[]),
    ticket_db_service: TicketDBService = Depends(get_ticket_db_service)
):
    """
    Receive Text from the Frontend

    Args:
    - text_input (TextInput): A Pydantic model defining the expected input format containing the 'text' field.

    Returns:
    - TextResponse: A response containing the received text and a status code.

    Raises:
    - HTTPException: If 'text' field is empty, returns a 400 Bad Request with an error message.
    """
    updated_ticket = ticket_db_service.update_ticket_attachments(ticket_id, files)
    return updated_ticket
