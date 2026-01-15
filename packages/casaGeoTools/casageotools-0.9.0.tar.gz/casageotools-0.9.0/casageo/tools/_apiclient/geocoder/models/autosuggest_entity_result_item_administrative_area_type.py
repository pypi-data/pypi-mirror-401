from enum import Enum


class AutosuggestEntityResultItemAdministrativeAreaType(str, Enum):
    COUNTRY = "country"
    COUNTY = "county"
    STATE = "state"

    def __str__(self) -> str:
        return str(self.value)
