from enum import Enum


class ExtendedAccessPointType(str, Enum):
    DELIVERY = "delivery"
    EMERGENCY = "emergency"
    ENTRANCE = "entrance"
    LOADING = "loading"
    OTHER = "other"
    PARKING = "parking"
    TAXI = "taxi"

    def __str__(self) -> str:
        return str(self.value)
