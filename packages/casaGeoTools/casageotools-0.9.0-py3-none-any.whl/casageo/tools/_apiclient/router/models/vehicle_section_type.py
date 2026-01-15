from enum import Enum


class VehicleSectionType(str, Enum):
    VEHICLE = "vehicle"

    def __str__(self) -> str:
        return str(self.value)
