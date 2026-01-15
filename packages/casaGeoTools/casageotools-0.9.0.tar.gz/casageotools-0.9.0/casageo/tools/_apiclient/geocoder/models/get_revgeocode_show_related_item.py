from enum import Enum


class GetRevgeocodeShowRelatedItem(str, Enum):
    INTERSECTIONS = "intersections"
    NEARBYADDRESS = "nearbyAddress"
    PARENTPA = "parentPA"

    def __str__(self) -> str:
        return str(self.value)
