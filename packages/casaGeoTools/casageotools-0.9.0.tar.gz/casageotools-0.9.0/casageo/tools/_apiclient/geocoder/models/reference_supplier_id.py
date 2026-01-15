from enum import Enum


class ReferenceSupplierId(str, Enum):
    BOOKING_COM = "booking.com"
    CORE = "core"
    NSR = "nsr"
    PARKOPEDIA = "parkopedia"
    RYD = "ryd"
    TRIPADVISOR = "tripadvisor"
    VENUES = "venues"
    VINFAST = "vinfast"
    YELP = "yelp"

    def __str__(self) -> str:
        return str(self.value)
