from enum import Enum


class TruckAmenityShowersType(str, Enum):
    SHOWERS = "showers"

    def __str__(self) -> str:
        return str(self.value)
