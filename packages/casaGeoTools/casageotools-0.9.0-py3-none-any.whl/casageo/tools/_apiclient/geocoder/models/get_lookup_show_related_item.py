from enum import Enum


class GetLookupShowRelatedItem(str, Enum):
    MPA = "MPA"
    PARENTPA = "parentPA"

    def __str__(self) -> str:
        return str(self.value)
