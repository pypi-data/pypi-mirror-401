from enum import Enum


class GetBrowseRanking(str, Enum):
    EXCURSIONDISTANCE = "excursionDistance"

    def __str__(self) -> str:
        return str(self.value)
