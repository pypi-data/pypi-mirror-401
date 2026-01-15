from enum import Enum


class GetLookupShowItem(str, Enum):
    ADDRESSUSAGE = "addressUsage"
    COUNTRYINFO = "countryInfo"
    EMOBILITYSERVICEPROVIDERS = "eMobilityServiceProviders"
    EV = "ev"
    FUEL = "fuel"
    FUELPRICES = "fuelPrices"
    PHONEMES = "phonemes"
    POSTALCODEDETAILS = "postalCodeDetails"
    STREETINFO = "streetInfo"
    TRIPADVISOR = "tripadvisor"
    TRIPADVISORIMAGEVARIANTS = "tripadvisorImageVariants"
    TRUCK = "truck"
    TZ = "tz"

    def __str__(self) -> str:
        return str(self.value)
