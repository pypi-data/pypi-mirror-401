from enum import Enum


class SpeedLimitSource(str, Enum):
    DERIVED = "derived"
    POSTED = "posted"

    def __str__(self) -> str:
        return str(self.value)
