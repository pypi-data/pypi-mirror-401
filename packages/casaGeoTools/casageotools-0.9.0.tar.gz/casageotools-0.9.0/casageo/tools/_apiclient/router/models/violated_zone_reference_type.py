from enum import Enum


class ViolatedZoneReferenceType(str, Enum):
    ZONEREFERENCE = "zoneReference"

    def __str__(self) -> str:
        return str(self.value)
