from enum import Enum


class LookupResponseLocalityType(str, Enum):
    CITY = "city"
    DISTRICT = "district"
    POSTALCODE = "postalCode"
    SUBDISTRICT = "subdistrict"

    def __str__(self) -> str:
        return str(self.value)
