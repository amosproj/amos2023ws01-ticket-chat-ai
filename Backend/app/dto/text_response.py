from pydantic import BaseModel
from typing import Optional


class TextResponse(BaseModel):
    text: str
    data: str
    code: int
    ticket_id: Optional[str]
