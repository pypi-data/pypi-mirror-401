from enum import Enum


class GetRevgeocodeTypesItem(str, Enum):
    ADDRESS = "address"
    AREA = "area"
    CITY = "city"
    STREET = "street"

    def __str__(self) -> str:
        return str(self.value)
