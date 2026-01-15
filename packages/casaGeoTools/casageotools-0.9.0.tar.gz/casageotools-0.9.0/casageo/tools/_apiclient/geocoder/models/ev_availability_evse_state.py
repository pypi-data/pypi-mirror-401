from enum import Enum


class EvAvailabilityEvseState(str, Enum):
    AVAILABLE = "AVAILABLE"
    OCCUPIED = "OCCUPIED"
    OFFLINE = "OFFLINE"
    OTHER = "OTHER"
    OUT_OF_SERVICE = "OUT_OF_SERVICE"
    RESERVED = "RESERVED"
    UNAVAILABLE = "UNAVAILABLE"

    def __str__(self) -> str:
        return str(self.value)
