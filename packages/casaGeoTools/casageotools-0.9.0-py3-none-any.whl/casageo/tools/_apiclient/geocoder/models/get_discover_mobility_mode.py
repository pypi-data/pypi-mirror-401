from enum import Enum


class GetDiscoverMobilityMode(str, Enum):
    CAR = "car"
    MOTORBIKE = "motorbike"
    TRUCK = "truck"

    def __str__(self) -> str:
        return str(self.value)
