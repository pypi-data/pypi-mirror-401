from enum import Enum


class GetAutosuggestShowMapReferencesItem(str, Enum):
    ADMINIDS = "adminIds"
    POINTADDRESS = "pointAddress"
    SEGMENTS = "segments"

    def __str__(self) -> str:
        return str(self.value)
