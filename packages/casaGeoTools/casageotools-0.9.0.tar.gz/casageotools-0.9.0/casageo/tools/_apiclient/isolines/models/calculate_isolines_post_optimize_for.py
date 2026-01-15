from enum import Enum


class CalculateIsolinesPostOptimizeFor(str, Enum):
    BALANCED = "balanced"
    PERFORMANCE = "performance"
    QUALITY = "quality"

    def __str__(self) -> str:
        return str(self.value)
