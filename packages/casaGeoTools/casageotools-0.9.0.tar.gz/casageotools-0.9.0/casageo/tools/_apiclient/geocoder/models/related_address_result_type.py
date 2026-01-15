from enum import Enum


class RelatedAddressResultType(str, Enum):
    ADDRESSBLOCK = "addressBlock"
    ADMINISTRATIVEAREA = "administrativeArea"
    HOUSENUMBER = "houseNumber"
    INTERSECTION = "intersection"
    LOCALITY = "locality"
    PLACE = "place"
    POSTALCODEPOINT = "postalCodePoint"
    STREET = "street"

    def __str__(self) -> str:
        return str(self.value)
