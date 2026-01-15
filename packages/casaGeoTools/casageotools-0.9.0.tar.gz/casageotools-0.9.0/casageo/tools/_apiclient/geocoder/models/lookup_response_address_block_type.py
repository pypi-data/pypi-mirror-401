from enum import Enum


class LookupResponseAddressBlockType(str, Enum):
    BLOCK = "block"
    SUBBLOCK = "subblock"

    def __str__(self) -> str:
        return str(self.value)
