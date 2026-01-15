from enum import Enum


class PostAutosuggestRanking(str, Enum):
    EXCURSIONDISTANCE = "excursionDistance"

    def __str__(self) -> str:
        return str(self.value)
