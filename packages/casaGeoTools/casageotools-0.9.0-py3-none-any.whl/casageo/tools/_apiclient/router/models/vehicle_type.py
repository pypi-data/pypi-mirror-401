from enum import Enum


class VehicleType(str, Enum):
    STRAIGHTTRUCK = "StraightTruck"
    TRACTOR = "Tractor"

    def __str__(self) -> str:
        return str(self.value)
