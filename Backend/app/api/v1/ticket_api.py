from app.api.dto.text_input import TextInput
from app.api.dto.ticket import Ticket
from app.api.dto.wrapped_ticket import WrappedTicket
from app.dependency.ai_service import get_ai_ticket_service
from app.dependency.db_service import get_ticket_db_service, get_user_db_service
from app.dependency.email_service import get_email_service
from app.enum.state import State
from app.model.ai_ticket_service.ai_ticket_service import AITicketService
from app.service.email_service import EmailService
from app.service.ticket_db_service import TicketDBService
from app.service.user_db_service import UserDBService
from app.util.logger import logger
from bson import ObjectId
from fastapi import APIRouter, HTTPException, UploadFile
from fastapi.params import Depends, File, Path, Body
from starlette import status

router = APIRouter()


@router.post("/ticket/text", status_code=status.HTTP_201_CREATED, response_model=Ticket)
async def process_text(
    input: TextInput = Body(default=TextInput()),
    ticket_db_service: TicketDBService = Depends(get_ticket_db_service),
    user_db_service: UserDBService = Depends(get_user_db_service),
    ticket_service: AITicketService = Depends(get_ai_ticket_service),
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
    received_dict = ticket_service.create_ticket(input.text)
    logger.info("Model execution complete. Result: %s", received_dict)

    # Set service based on user's location
    if not received_dict.get("service") or received_dict["service"] == "":
        if input.email:
            user = user_db_service.get_user_by_email(input.email)
            if user and user.location:
                logger.info("Setting ticket's service to user's location...")
                received_dict["service"] = user.location

    received_dict["state"] = State.draft

    # Save the ticket to the database using the TicketDBService
    logger.info("Saving ticket to the database...")
    created_ticket = ticket_db_service.create_ticket(received_dict)
    logger.info(
        f"Ticket created and saved successfully. Ticket ID: {created_ticket.id}"
    )

    return created_ticket


@router.put(
    "/ticket/{ticket_id}/update",
    status_code=status.HTTP_200_OK,
    response_model=Ticket,
)
async def update_ticket_attributes(
    ticket_id: str = Path(default=""),
    wrapped_ticket: WrappedTicket = Body(default=None),
    email_service: EmailService = Depends(get_email_service),
    ticket_db_service: TicketDBService = Depends(get_ticket_db_service),
):
    logger.info("Updating ticket attributes...")

    # Check if the 'ticket_id' field is empty or invalid
    if not ticket_id or not ObjectId.is_valid(ticket_id):
        logger.error("Received empty or invalid ticket id of type ObjectId!")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Received empty or invalid ticket id of type ObjectId!",
        )
    logger.info(f"Received ticket_id: {ticket_id}")

    # Update the ticket attributes in the database using the TicketDBService
    logger.info("Updating ticket attributes in the database...")
    updated_ticket = ticket_db_service.update_ticket_attributes(
        ticket_id, wrapped_ticket.ticket.dict()
    )

    # send email with ticket as content if ticket accepted
    if wrapped_ticket.email and updated_ticket.state == State.accepted:
        email_service.send_email(wrapped_ticket.email, updated_ticket)

    # Prepare response
    logger.info("Preparing response...")
    logger.info(
        f"Ticket attributes updated and saved successfully. Ticket ID: {updated_ticket.id}"
    )

    return updated_ticket


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


@router.delete(
    "/ticket/{ticket_id}/delete",
    status_code=status.HTTP_200_OK,
    response_model=Ticket,
)
async def delete_ticket(
    ticket_id: str = Path(default=""),
    ticket_db_service: TicketDBService = Depends(get_ticket_db_service),
):
    logger.info(f"Deleting ticket with id: {ticket_id}")
    ticket_db_service.delete_ticket(ticket_id)
