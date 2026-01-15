from enum import Enum


class AutocompleteResultItemResultType(str, Enum):
    ADMINISTRATIVEAREA = "administrativeArea"
    HOUSENUMBER = "houseNumber"
    INTERSECTION = "intersection"
    LOCALITY = "locality"
    POSTALCODEPOINT = "postalCodePoint"
    STREET = "street"

    def __str__(self) -> str:
        return str(self.value)
