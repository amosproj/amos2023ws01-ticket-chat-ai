from enum import Enum


class State(str, Enum):
    draft = ("draft",)
    accepted = "accepted"
