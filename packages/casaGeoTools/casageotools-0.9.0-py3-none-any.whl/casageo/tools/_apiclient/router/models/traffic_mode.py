from enum import Enum


class TrafficMode(str, Enum):
    DEFAULT = "default"
    DISABLED = "disabled"

    def __str__(self) -> str:
        return str(self.value)
