from enum import Enum


class ParkingLotPlaceType(str, Enum):
    PARKINGLOT = "parkingLot"

    def __str__(self) -> str:
        return str(self.value)
