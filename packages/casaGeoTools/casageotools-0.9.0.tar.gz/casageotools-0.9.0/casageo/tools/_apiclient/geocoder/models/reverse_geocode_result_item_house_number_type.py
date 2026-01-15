from enum import Enum


class ReverseGeocodeResultItemHouseNumberType(str, Enum):
    INTERPOLATED = "interpolated"
    MPA = "MPA"
    PA = "PA"

    def __str__(self) -> str:
        return str(self.value)
