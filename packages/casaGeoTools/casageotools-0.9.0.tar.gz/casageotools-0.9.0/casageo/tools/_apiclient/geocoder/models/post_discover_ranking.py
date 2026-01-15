from enum import Enum


class PostDiscoverRanking(str, Enum):
    EXCURSIONDISTANCE = "excursionDistance"

    def __str__(self) -> str:
        return str(self.value)
