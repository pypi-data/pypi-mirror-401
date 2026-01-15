from enum import Enum


class GetGeocodeWithItem(str, Enum):
    MPA = "MPA"

    def __str__(self) -> str:
        return str(self.value)
