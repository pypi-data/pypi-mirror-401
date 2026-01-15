from enum import Enum


class TransitSectionType(str, Enum):
    TRANSIT = "transit"

    def __str__(self) -> str:
        return str(self.value)
