from enum import Enum


class ReroutingMode(str, Enum):
    NONE = "none"
    RETURNTOROUTE = "returnToRoute"

    def __str__(self) -> str:
        return str(self.value)
