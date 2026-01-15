from enum import Enum


class ViolatedTransportModeType(str, Enum):
    VIOLATEDTRANSPORTMODE = "violatedTransportMode"

    def __str__(self) -> str:
        return str(self.value)
