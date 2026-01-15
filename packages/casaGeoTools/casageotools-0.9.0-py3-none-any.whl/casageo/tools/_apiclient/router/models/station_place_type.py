from enum import Enum


class StationPlaceType(str, Enum):
    STATION = "station"

    def __str__(self) -> str:
        return str(self.value)
