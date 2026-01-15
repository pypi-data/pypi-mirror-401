from enum import Enum


class ViolatedChargingStationOpeningHoursType(str, Enum):
    VIOLATEDOPENINGHOURS = "violatedOpeningHours"

    def __str__(self) -> str:
        return str(self.value)
