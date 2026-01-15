from enum import Enum


class ReverseGeocodeResultItemResultType(str, Enum):
    ADDRESSBLOCK = "addressBlock"
    ADMINISTRATIVEAREA = "administrativeArea"
    HOUSENUMBER = "houseNumber"
    LOCALITY = "locality"
    PLACE = "place"
    POSTALCODEPOINT = "postalCodePoint"
    STREET = "street"

    def __str__(self) -> str:
        return str(self.value)
