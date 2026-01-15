from enum import Enum


class PostMultiRevgeocodeWithItem(str, Enum):
    ESTIMATEDAREAFALLBACK = "estimatedAreaFallback"
    MPA = "MPA"
    UNNAMEDSTREETS = "unnamedStreets"

    def __str__(self) -> str:
        return str(self.value)
