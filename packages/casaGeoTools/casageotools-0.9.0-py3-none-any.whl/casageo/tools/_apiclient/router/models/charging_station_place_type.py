from enum import Enum


class ChargingStationPlaceType(str, Enum):
    CHARGINGSTATION = "chargingStation"

    def __str__(self) -> str:
        return str(self.value)
