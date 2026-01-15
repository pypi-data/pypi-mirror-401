from enum import Enum


class GetGeocodeShowRelatedItem(str, Enum):
    INTERSECTIONS = "intersections"
    MPA = "MPA"
    PARENTPA = "parentPA"

    def __str__(self) -> str:
        return str(self.value)
