from enum import Enum


class VehicleRestrictionType(str, Enum):
    RESTRICTION = "restriction"

    def __str__(self) -> str:
        return str(self.value)
