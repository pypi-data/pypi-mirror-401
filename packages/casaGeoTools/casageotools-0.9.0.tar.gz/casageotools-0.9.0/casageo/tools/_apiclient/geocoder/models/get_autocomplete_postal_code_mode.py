from enum import Enum


class GetAutocompletePostalCodeMode(str, Enum):
    CITYLOOKUP = "cityLookup"
    DISTRICTLOOKUP = "districtLookup"

    def __str__(self) -> str:
        return str(self.value)
