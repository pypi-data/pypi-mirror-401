from enum import Enum


class NoticeSeverity(str, Enum):
    CRITICAL = "critical"
    INFO = "info"

    def __str__(self) -> str:
        return str(self.value)
