from enum import Enum


class MaxSpeedType1(str, Enum):
    UNLIMITED = "unlimited"

    def __str__(self) -> str:
        return str(self.value)
