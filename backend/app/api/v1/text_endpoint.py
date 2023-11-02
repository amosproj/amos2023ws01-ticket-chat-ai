from fastapi import APIRouter, HTTPException, Body

router = APIRouter()

@router.post("/text/")
async def receive_text(text: str = Body(...)):
    """
    Receive Text from the Frontend

    Args:
    - text (str): The text to be received from the frontend.

    Returns:
    - dict: A response containing the received text.
    """
    # This will just print the text to the console for now
    print(text)
    
    return {"received_text": text}
