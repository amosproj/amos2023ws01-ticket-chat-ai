from bson import ObjectId
from fastapi import APIRouter, HTTPException, UploadFile
from fastapi.params import Depends, File, Path, Body
from starlette import status

from app.api.dto.text_input import TextInput
from app.api.dto.ticket import Ticket
from app.dependency.ticket_db_service import get_ticket_db_service
from app.dependency.trained_t5_model import get_trained_t5_model
from app.model.t5.use_trained_t5_model import TrainedT5Model
from app.service.ticket_db_service import TicketDBService
from app.util.logger import logger

router = APIRouter()


@router.post("/ticket/text", status_code=status.HTTP_201_CREATED, response_model=Ticket)
async def process_text(
    input: TextInput = Body(default=TextInput()),
    trained_t5_model: TrainedT5Model = Depends(get_trained_t5_model),
    ticket_db_service: TicketDBService = Depends(get_ticket_db_service),
):
    """
    Receive Text from the Frontend

    Args:
    - text_input (TextInput): A Pydantic model defining the expected input format containing the 'text' field.

    Returns:
    - Ticket: A response containing the created ticket information.

    Raises:
    - HTTPException: If 'text' field is empty, returns a 400 Bad Request with an error message.
    """
    logger.info("Processing text...")

    # Check if the 'text' field is empty
    if not input.text:
        logger.error("Received empty text!")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Text is required"
        )
    logger.info(f"Received text: {input.text}")

    # Run the model to process the input text
    logger.info("Running the model...")
    received_dict = trained_t5_model.run_model(input.text)
    logger.info("Model execution complete. Result: %s", received_dict)

    # Save the ticket to the database using the TicketDBService
    logger.info("Saving ticket to the database...")
    created_ticket = ticket_db_service.create_ticket(received_dict)
    logger.info(
        f"Ticket created and saved successfully. Ticket ID: {created_ticket.id}"
    )

    print(input.email)

    return created_ticket


@router.put(
    "/ticket/{ticket_id}/attachments",
    status_code=status.HTTP_200_OK,
    response_model=Ticket,
)
async def update_ticket_attachments(
    ticket_id: str = Path(default=""),
    files: list[UploadFile] = File(default=[]),
    ticket_db_service: TicketDBService = Depends(get_ticket_db_service),
):
    """
    Receive Attachments from the Frontend

    Args:
    - ticket_id (str): A id of the ticket which attachments should be updated.
    - files (UploadFile): A list of attachments that should be added to the ticket.

    Returns:
    - Ticket: A response containing the updated ticket and attachments information.

    Raises:
    - HTTPException: If 'ticket_id' field is empty or invalid, returns a 400 Bad Request with an error message.
    """
    logger.info("Updating ticket attachments...")

    # Check if the 'ticket_id' field is empty or invalid
    if not ticket_id or not ObjectId.is_valid(ticket_id):
        logger.error("Received empty or invalid ticket id of type ObjectId!")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Received empty or invalid ticket id of type ObjectId!",
        )
    logger.info(f"Received ticket_id: {ticket_id}")

    # Update the ticket attachments in the database using the TicketDBService
    logger.info("Updating ticket attachments in the database...")
    updated_ticket = ticket_db_service.update_ticket_attachments(ticket_id, files)

    # Prepare response
    logger.info("Preparing response...")
    if updated_ticket:
        logger.info(
            f"Ticket attachments updated and saved successfully. Ticket ID: {updated_ticket.id}"
        )
    else:
        logger.error("Ticket attachments update failed.")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ticket attachments update failed.",
        )

    return updated_ticket
