from enum import Enum


class TurnActionDirection(str, Enum):
    LEFT = "left"
    MIDDLE = "middle"
    RIGHT = "right"

    def __str__(self) -> str:
        return str(self.value)
