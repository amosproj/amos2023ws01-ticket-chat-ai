from enum import Enum


class Prio(str, Enum):
    low = "Low"
    medium = "Medium"
    high = "High"
    very_high = "Very High"
