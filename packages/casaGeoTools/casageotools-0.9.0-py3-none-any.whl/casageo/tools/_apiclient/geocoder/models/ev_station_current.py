from enum import Enum


class EvStationCurrent(str, Enum):
    AC = "AC"
    DC = "DC"

    def __str__(self) -> str:
        return str(self.value)
