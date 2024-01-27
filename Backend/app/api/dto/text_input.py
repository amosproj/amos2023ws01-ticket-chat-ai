from fastapi import UploadFile
from pydantic import BaseModel


class TextInput(BaseModel):
    text: str = ""
