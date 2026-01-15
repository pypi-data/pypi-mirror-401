from enum import Enum


class TruckTypeWithDefault(str, Enum):
    STRAIGHT = "Straight"
    TRACTOR = "Tractor"

    def __str__(self) -> str:
        return str(self.value)
