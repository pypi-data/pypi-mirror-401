from enum import Enum


class GetGeocodePostalCodeMode(str, Enum):
    CITYLOOKUP = "cityLookup"
    DISTRICTLOOKUP = "districtLookup"

    def __str__(self) -> str:
        return str(self.value)
