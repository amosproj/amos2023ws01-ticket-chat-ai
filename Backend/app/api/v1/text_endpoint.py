from fastapi import APIRouter, HTTPException
from app.dto.text_input import TextInput
from app.dto.text_response import TextResponse
from app.models.t5.use_trained_t5_model import TrainedT5Model

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
    if not text_input.text:
        raise HTTPException(status_code=400, detail="Text is required")  # Return a 400 Bad Request with an error message

    # run model
    trained_t5_model = TrainedT5Model()
    received_text = trained_t5_model.run_model(text_input.text)

    # Print the received text for debugging or logging purposes
    print(f"Received Text: {received_text}")
    
    # Respond with a simple message and a status code
    response_data = "Message was received"
    status_code = 200  # You can change this as needed

    return TextResponse(data=response_data, text=received_text, code=status_code)
