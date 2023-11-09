from enum import Enum


class PrioEnum(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
    very_high = "very high"
