from enum import Enum


class FuelAdditiveType(str, Enum):
    AUS32 = "aus32"

    def __str__(self) -> str:
        return str(self.value)
