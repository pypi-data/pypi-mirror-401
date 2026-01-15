from enum import Enum


class RoadInfoType(str, Enum):
    HIGHWAY = "highway"
    RURAL = "rural"
    URBAN = "urban"

    def __str__(self) -> str:
        return str(self.value)
