from enum import Enum


class GetGeocodeShowTranslationsItem(str, Enum):
    CITY = "city"
    COUNTY = "county"
    DISTRICT = "district"
    STATE = "state"

    def __str__(self) -> str:
        return str(self.value)
