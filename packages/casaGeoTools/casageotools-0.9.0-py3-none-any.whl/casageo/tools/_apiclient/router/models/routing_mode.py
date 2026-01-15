from enum import Enum


class RoutingMode(str, Enum):
    FAST = "fast"
    SHORT = "short"

    def __str__(self) -> str:
        return str(self.value)
