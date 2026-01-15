from enum import Enum


class BoardActionAction(str, Enum):
    BOARD = "board"

    def __str__(self) -> str:
        return str(self.value)
