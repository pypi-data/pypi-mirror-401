from enum import Enum


class PostalCodeDetailsUspsZipPostalEntity(str, Enum):
    USPS = "USPS"

    def __str__(self) -> str:
        return str(self.value)
