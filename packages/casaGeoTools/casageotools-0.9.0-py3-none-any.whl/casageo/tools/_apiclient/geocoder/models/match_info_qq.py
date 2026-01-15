from enum import Enum


class MatchInfoQq(str, Enum):
    CITY = "city"
    COUNTRY = "country"
    COUNTY = "county"
    DISTRICT = "district"
    HOUSENUMBER = "houseNumber"
    POSTALCODE = "postalCode"
    STATE = "state"
    STREET = "street"

    def __str__(self) -> str:
        return str(self.value)
