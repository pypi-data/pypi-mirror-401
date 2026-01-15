from enum import Enum


class GetGeocodeAddressNamesMode(str, Enum):
    MATCHED = "matched"
    NORMALIZED = "normalized"

    def __str__(self) -> str:
        return str(self.value)
