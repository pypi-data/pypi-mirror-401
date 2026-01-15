from enum import Enum


class VehicleCategory(str, Enum):
    LIGHTTRUCK = "lightTruck"
    UNDEFINED = "undefined"

    def __str__(self) -> str:
        return str(self.value)
