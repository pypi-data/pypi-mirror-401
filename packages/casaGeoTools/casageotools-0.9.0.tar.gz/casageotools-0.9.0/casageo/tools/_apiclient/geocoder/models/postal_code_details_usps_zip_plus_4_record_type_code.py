from enum import Enum


class PostalCodeDetailsUspsZipPlus4RecordTypeCode(str, Enum):
    F = "F"
    G = "G"
    H = "H"
    P = "P"
    R = "R"
    S = "S"

    def __str__(self) -> str:
        return str(self.value)
