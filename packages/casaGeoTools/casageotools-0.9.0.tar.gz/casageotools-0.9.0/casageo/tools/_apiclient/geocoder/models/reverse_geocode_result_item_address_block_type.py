from enum import Enum


class ReverseGeocodeResultItemAddressBlockType(str, Enum):
    BLOCK = "block"
    SUBBLOCK = "subblock"

    def __str__(self) -> str:
        return str(self.value)
