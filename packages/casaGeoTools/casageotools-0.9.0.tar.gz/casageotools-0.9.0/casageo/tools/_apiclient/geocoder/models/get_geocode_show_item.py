from enum import Enum


class GetGeocodeShowItem(str, Enum):
    ADDRESSUSAGE = "addressUsage"
    COUNTRYINFO = "countryInfo"
    PARSING = "parsing"
    POSTALCODEDETAILS = "postalCodeDetails"
    SECONDARYUNITINFO = "secondaryUnitInfo"
    STREETINFO = "streetInfo"
    TZ = "tz"

    def __str__(self) -> str:
        return str(self.value)
