from enum import Enum


class CalculateIsolinesOptimizeFor(str, Enum):
    BALANCED = "balanced"
    PERFORMANCE = "performance"
    QUALITY = "quality"

    def __str__(self) -> str:
        return str(self.value)
