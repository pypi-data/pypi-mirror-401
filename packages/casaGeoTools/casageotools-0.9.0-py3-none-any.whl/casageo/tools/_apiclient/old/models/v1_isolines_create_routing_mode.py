from enum import Enum


class V1IsolinesCreateRoutingMode(str, Enum):
    FAST = "fast"
    SHORT = "short"

    def __str__(self) -> str:
        return str(self.value)
