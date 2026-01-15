from enum import Enum


class ChargingSetupActionAction(str, Enum):
    CHARGINGSETUP = "chargingSetup"

    def __str__(self) -> str:
        return str(self.value)
