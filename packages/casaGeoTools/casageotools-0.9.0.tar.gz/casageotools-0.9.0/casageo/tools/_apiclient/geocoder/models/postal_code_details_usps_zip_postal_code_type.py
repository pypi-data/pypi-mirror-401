from enum import Enum


class PostalCodeDetailsUspsZipPostalCodeType(str, Enum):
    ZIP = "ZIP"

    def __str__(self) -> str:
        return str(self.value)
