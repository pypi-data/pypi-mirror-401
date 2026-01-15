from enum import Enum


class PostMultiRevgeocodeTypesItem(str, Enum):
    ADDRESS = "address"
    AREA = "area"
    CITY = "city"
    STREET = "street"

    def __str__(self) -> str:
        return str(self.value)
