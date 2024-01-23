from pydantic import BaseModel


class Service(BaseModel):
    service_name: str
    safe_keywords: list[str] = []
    hint_keywords: list[str] = []
