from enum import Enum


class GetAutocompleteTypesItem(str, Enum):
    AREA = "area"
    CITY = "city"
    POSTALCODE = "postalCode"

    def __str__(self) -> str:
        return str(self.value)
