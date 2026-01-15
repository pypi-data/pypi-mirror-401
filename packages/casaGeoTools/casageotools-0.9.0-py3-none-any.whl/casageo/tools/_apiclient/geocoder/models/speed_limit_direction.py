from enum import Enum


class SpeedLimitDirection(str, Enum):
    E = "E"
    N = "N"
    NE = "NE"
    NW = "NW"
    S = "S"
    SE = "SE"
    SW = "SW"
    W = "W"

    def __str__(self) -> str:
        return str(self.value)
