from enum import Enum


class SpeedLimitSpeedUnit(str, Enum):
    KPH = "kph"
    MPH = "mph"

    def __str__(self) -> str:
        return str(self.value)
