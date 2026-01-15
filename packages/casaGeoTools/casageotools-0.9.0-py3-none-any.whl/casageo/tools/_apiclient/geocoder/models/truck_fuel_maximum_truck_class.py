from enum import Enum


class TruckFuelMaximumTruckClass(str, Enum):
    HEAVY = "heavy"
    MEDIUM = "medium"

    def __str__(self) -> str:
        return str(self.value)
