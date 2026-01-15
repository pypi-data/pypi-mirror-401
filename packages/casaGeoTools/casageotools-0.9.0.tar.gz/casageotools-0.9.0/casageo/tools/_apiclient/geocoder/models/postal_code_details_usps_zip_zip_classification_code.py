from enum import Enum


class PostalCodeDetailsUspsZipZipClassificationCode(str, Enum):
    M = "M"
    P = "P"
    U = "U"

    def __str__(self) -> str:
        return str(self.value)
