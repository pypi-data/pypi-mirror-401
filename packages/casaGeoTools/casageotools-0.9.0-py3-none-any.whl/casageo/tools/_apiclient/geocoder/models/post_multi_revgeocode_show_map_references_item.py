from enum import Enum


class PostMultiRevgeocodeShowMapReferencesItem(str, Enum):
    ADMINIDS = "adminIds"
    CMVERSION = "cmVersion"
    LINKS = "links"
    MICROPOINTADDRESS = "microPointAddress"
    POINTADDRESS = "pointAddress"
    SEGMENTS = "segments"

    def __str__(self) -> str:
        return str(self.value)
