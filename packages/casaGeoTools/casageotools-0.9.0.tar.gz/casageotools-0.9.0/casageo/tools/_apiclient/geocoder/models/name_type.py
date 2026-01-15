from enum import Enum


class NameType(str, Enum):
    ABBREVIATION = "abbreviation"
    AREACODE = "areaCode"
    BASENAME = "baseName"
    EXONYM = "exonym"
    SHORTENED = "shortened"
    SYNONYM = "synonym"

    def __str__(self) -> str:
        return str(self.value)
