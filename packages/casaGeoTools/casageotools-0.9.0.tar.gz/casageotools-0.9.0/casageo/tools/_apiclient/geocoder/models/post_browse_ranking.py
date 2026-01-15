from enum import Enum


class PostBrowseRanking(str, Enum):
    EXCURSIONDISTANCE = "excursionDistance"

    def __str__(self) -> str:
        return str(self.value)
