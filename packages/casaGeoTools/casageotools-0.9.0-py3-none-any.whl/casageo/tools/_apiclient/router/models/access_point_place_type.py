from enum import Enum


class AccessPointPlaceType(str, Enum):
    ACCESSPOINT = "accessPoint"

    def __str__(self) -> str:
        return str(self.value)
