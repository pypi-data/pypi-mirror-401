from enum import Enum


class GetAutosuggestShowItem(str, Enum):
    DETAILS = "details"
    FUEL = "fuel"
    PHONEMES = "phonemes"
    STREETINFO = "streetInfo"
    TRUCK = "truck"
    TZ = "tz"

    def __str__(self) -> str:
        return str(self.value)
