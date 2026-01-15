from enum import Enum


class ChargingActionAction(str, Enum):
    CHARGING = "charging"

    def __str__(self) -> str:
        return str(self.value)
