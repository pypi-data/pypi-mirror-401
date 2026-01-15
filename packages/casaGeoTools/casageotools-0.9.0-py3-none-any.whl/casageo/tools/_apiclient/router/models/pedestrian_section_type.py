from enum import Enum


class PedestrianSectionType(str, Enum):
    PEDESTRIAN = "pedestrian"

    def __str__(self) -> str:
        return str(self.value)
