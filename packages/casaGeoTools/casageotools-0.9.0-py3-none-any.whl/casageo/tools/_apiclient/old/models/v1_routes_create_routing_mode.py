from enum import Enum


class V1RoutesCreateRoutingMode(str, Enum):
    FAST = "fast"
    SHORT = "short"

    def __str__(self) -> str:
        return str(self.value)
