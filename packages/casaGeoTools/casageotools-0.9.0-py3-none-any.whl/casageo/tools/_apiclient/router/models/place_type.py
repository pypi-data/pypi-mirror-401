from enum import Enum


class PlaceType(str, Enum):
    PLACE = "place"

    def __str__(self) -> str:
        return str(self.value)
