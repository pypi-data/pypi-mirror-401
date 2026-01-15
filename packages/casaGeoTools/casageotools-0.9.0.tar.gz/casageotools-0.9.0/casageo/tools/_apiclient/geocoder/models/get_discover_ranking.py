from enum import Enum


class GetDiscoverRanking(str, Enum):
    EXCURSIONDISTANCE = "excursionDistance"

    def __str__(self) -> str:
        return str(self.value)
