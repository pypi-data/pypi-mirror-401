from enum import Enum


class LookupResponseAdministrativeAreaType(str, Enum):
    COUNTRY = "country"
    COUNTY = "county"
    STATE = "state"

    def __str__(self) -> str:
        return str(self.value)
