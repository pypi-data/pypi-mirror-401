from enum import Enum


class PostMultiRevgeocodeShowRelatedItem(str, Enum):
    INTERSECTIONS = "intersections"
    NEARBYADDRESS = "nearbyAddress"
    PARENTPA = "parentPA"

    def __str__(self) -> str:
        return str(self.value)
