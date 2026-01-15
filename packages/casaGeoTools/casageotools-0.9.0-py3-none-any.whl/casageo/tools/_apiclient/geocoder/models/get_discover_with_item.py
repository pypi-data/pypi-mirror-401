from enum import Enum


class GetDiscoverWithItem(str, Enum):
    RECOMMENDPLACES = "recommendPlaces"

    def __str__(self) -> str:
        return str(self.value)
