from enum import Enum


class RelatedAddressRelationship(str, Enum):
    INTERSECTION = "intersection"
    MPA = "MPA"
    NEARBYADDRESS = "nearbyAddress"
    PARENTPA = "parentPA"

    def __str__(self) -> str:
        return str(self.value)
