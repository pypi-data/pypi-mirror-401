from enum import Enum


class BrowseResultItemResultType(str, Enum):
    ADDRESSBLOCK = "addressBlock"
    ADMINISTRATIVEAREA = "administrativeArea"
    LOCALITY = "locality"
    PLACE = "place"
    STREET = "street"

    def __str__(self) -> str:
        return str(self.value)
