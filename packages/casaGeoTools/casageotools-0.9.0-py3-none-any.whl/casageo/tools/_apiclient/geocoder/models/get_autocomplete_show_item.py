from enum import Enum


class GetAutocompleteShowItem(str, Enum):
    HASRELATEDMPA = "hasRelatedMPA"
    STREETINFO = "streetInfo"

    def __str__(self) -> str:
        return str(self.value)
