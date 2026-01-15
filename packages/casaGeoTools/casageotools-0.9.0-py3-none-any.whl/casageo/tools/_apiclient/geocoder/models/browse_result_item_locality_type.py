from enum import Enum


class BrowseResultItemLocalityType(str, Enum):
    CITY = "city"
    DISTRICT = "district"
    POSTALCODE = "postalCode"
    SUBDISTRICT = "subdistrict"

    def __str__(self) -> str:
        return str(self.value)
