from enum import Enum


class OneboxSearchResultItemAdministrativeAreaType(str, Enum):
    COUNTRY = "country"
    COUNTY = "county"
    STATE = "state"

    def __str__(self) -> str:
        return str(self.value)
