
from pydantic import BaseModel
from app.enum.service import ServiceEnum


class Service(BaseModel):
    service_name: ServiceEnum
    safe_keywords: list[str] = []
    hint_keywords: list[str] = []
