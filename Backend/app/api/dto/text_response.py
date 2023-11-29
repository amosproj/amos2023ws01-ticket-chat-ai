from pydantic import BaseModel


class TextResponse(BaseModel):
    message: str
    data: str
