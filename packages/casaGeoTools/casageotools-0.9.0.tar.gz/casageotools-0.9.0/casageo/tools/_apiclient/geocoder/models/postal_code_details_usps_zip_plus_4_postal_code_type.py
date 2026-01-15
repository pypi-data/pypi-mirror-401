from enum import Enum


class PostalCodeDetailsUspsZipPlus4PostalCodeType(str, Enum):
    ZIP4 = "ZIP+4"

    def __str__(self) -> str:
        return str(self.value)
