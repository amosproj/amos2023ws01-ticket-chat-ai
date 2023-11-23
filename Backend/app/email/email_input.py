from pydantic import BaseModel


class EmailInput(BaseModel):
    text: str
