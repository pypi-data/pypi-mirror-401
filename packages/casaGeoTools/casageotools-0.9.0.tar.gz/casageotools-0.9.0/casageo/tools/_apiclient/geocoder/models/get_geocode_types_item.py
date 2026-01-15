from enum import Enum


class GetGeocodeTypesItem(str, Enum):
    ADDRESS = "address"
    AREA = "area"
    CITY = "city"
    HOUSENUMBER = "houseNumber"
    PLACE = "place"
    POSTALCODE = "postalCode"
    STREET = "street"

    def __str__(self) -> str:
        return str(self.value)
