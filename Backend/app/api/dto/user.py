from pydantic import BaseModel


class User(BaseModel):
    id: str = ""
    first_name: str
    family_name: str
    email_address: str
    location: str
    password: str
    ticket_ids: list
