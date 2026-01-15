from enum import Enum


class WaitActionAction(str, Enum):
    WAIT = "wait"

    def __str__(self) -> str:
        return str(self.value)
