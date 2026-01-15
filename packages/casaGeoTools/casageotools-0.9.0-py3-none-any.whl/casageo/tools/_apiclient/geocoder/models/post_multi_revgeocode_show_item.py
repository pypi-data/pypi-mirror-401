from enum import Enum


class PostMultiRevgeocodeShowItem(str, Enum):
    ADDRESSUSAGE = "addressUsage"
    COUNTRYINFO = "countryInfo"
    POSTALCODEDETAILS = "postalCodeDetails"
    STREETINFO = "streetInfo"
    TZ = "tz"

    def __str__(self) -> str:
        return str(self.value)
