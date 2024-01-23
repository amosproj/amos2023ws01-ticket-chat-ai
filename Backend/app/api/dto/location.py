from pydantic import BaseModel


class Location(BaseModel):
    name: str
