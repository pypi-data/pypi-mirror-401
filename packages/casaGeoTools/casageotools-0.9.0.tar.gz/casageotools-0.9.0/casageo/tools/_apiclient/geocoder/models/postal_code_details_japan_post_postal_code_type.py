from enum import Enum


class PostalCodeDetailsJapanPostPostalCodeType(str, Enum):
    ZIP = "ZIP"

    def __str__(self) -> str:
        return str(self.value)
