from pydantic import BaseModel

class TextResponse(BaseModel):
    text: str
    data: str
    code: int
