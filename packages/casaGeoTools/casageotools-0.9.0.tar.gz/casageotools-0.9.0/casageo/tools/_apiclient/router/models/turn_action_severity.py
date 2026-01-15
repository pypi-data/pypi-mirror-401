from enum import Enum


class TurnActionSeverity(str, Enum):
    HEAVY = "heavy"
    LIGHT = "light"
    QUITE = "quite"

    def __str__(self) -> str:
        return str(self.value)
