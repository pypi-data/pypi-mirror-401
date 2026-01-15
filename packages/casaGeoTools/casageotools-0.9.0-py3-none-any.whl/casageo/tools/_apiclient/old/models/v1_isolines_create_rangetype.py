from enum import Enum


class V1IsolinesCreateRangetype(str, Enum):
    CONSUMPTION = "consumption"
    DISTANCE = "distance"
    TIME = "time"

    def __str__(self) -> str:
        return str(self.value)
