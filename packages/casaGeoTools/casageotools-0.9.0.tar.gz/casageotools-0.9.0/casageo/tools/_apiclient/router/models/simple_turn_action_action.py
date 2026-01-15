from enum import Enum


class SimpleTurnActionAction(str, Enum):
    TURN = "turn"

    def __str__(self) -> str:
        return str(self.value)
