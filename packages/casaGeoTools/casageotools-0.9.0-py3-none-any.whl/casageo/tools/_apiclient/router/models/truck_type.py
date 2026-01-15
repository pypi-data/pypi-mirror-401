from enum import Enum


class TruckType(str, Enum):
    STRAIGHT = "Straight"
    TRACTOR = "Tractor"

    def __str__(self) -> str:
        return str(self.value)
