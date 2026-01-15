from enum import Enum


class TruckCategory(str, Enum):
    LIGHTTRUCK = "lightTruck"
    UNDEFINED = "undefined"

    def __str__(self) -> str:
        return str(self.value)
