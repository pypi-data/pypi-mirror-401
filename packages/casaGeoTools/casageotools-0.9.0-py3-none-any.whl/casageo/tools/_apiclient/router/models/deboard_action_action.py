from enum import Enum


class DeboardActionAction(str, Enum):
    DEBOARD = "deboard"

    def __str__(self) -> str:
        return str(self.value)
