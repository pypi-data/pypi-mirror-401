from enum import Enum


class WheelchairAccessibility(str, Enum):
    LIMITED = "limited"
    NO = "no"
    UNKNOWN = "unknown"
    YES = "yes"

    def __str__(self) -> str:
        return str(self.value)
