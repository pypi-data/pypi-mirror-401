from enum import Enum


class AccessPointPlaceSideOfStreet(str, Enum):
    LEFT = "left"
    RIGHT = "right"

    def __str__(self) -> str:
        return str(self.value)
