from enum import Enum


class ViolatedTruckRoadTypeType(str, Enum):
    TRUCKROADTYPE = "truckRoadType"

    def __str__(self) -> str:
        return str(self.value)
