from enum import Enum


class PostAutosuggestWithItem(str, Enum):
    RECOMMENDPLACES = "recommendPlaces"

    def __str__(self) -> str:
        return str(self.value)
