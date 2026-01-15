from enum import Enum


class FuelStationMinimumTruckClass(str, Enum):
    HEAVY = "heavy"
    MEDIUM = "medium"

    def __str__(self) -> str:
        return str(self.value)
