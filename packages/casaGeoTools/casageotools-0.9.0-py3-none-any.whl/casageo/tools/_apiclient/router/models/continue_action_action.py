from enum import Enum


class ContinueActionAction(str, Enum):
    CONTINUE = "continue"

    def __str__(self) -> str:
        return str(self.value)
