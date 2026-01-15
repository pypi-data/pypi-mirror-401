from enum import Enum


class TunnelCategory(str, Enum):
    B = "B"
    C = "C"
    D = "D"
    E = "E"

    def __str__(self) -> str:
        return str(self.value)
