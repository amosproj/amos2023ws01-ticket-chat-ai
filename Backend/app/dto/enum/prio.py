from enum import Enum


class Prio(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
    very_high = "very high"
