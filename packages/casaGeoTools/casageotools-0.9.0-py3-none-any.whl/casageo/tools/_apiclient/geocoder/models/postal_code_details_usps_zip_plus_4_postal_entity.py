from enum import Enum


class PostalCodeDetailsUspsZipPlus4PostalEntity(str, Enum):
    USPS = "USPS"

    def __str__(self) -> str:
        return str(self.value)
