from enum import Enum


class PostDiscoverShowItem(str, Enum):
    EMOBILITYSERVICEPROVIDERS = "eMobilityServiceProviders"
    EV = "ev"
    FUEL = "fuel"
    FUELPRICES = "fuelPrices"
    PHONEMES = "phonemes"
    STREETINFO = "streetInfo"
    TRIPADVISOR = "tripadvisor"
    TRIPADVISORIMAGEVARIANTS = "tripadvisorImageVariants"
    TRUCK = "truck"
    TZ = "tz"

    def __str__(self) -> str:
        return str(self.value)
