from enum import Enum


class PostDiscoverMobilityMode(str, Enum):
    CAR = "car"
    MOTORBIKE = "motorbike"
    TRUCK = "truck"

    def __str__(self) -> str:
        return str(self.value)
