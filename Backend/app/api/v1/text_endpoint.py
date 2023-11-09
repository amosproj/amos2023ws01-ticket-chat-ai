from fastapi import APIRouter, HTTPException
from app.dto.input_model import TextInput  # Import the TextInput model from the "dto" directory
from app.dto.response_model import TextResponse  # Import the TextResponse model from the "dto" directory

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
    
    # You can perform any processing with the received text here if needed.
    # For example, you could save it to a database or apply some text analysis.
    
    # Print the received text for debugging or logging purposes
    print(f"Received Text: {text_input.text}")
    
    # Respond with a simple message and a status code
    response_data = "Message was received"
    status_code = 200  # You can change this as needed

    return TextResponse(data=response_data, text=text_input.text, code=status_code)
