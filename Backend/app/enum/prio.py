from enum import Enum


class Prio(str, Enum):
    low = "Niedrig"
    medium = "Mittel"
    high = "Hoch"
    very_high = " Sehr Hoch"
