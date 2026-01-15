from enum import Enum


class AutosuggestEntityResultItemAddressBlockType(str, Enum):
    BLOCK = "block"
    SUBBLOCK = "subblock"

    def __str__(self) -> str:
        return str(self.value)
