from enum import Enum


class TruckFuelType(str, Enum):
    TRUCK_CNG = "truck_cng"
    TRUCK_DIESEL = "truck_diesel"
    TRUCK_HYDROGEN = "truck_hydrogen"
    TRUCK_LNG = "truck_lng"

    def __str__(self) -> str:
        return str(self.value)
