from enum import Enum


class CarFuelType(str, Enum):
    BIODIESEL = "biodiesel"
    CNG = "cng"
    DIESEL = "diesel"
    DIESEL_WITH_ADDITIVES = "diesel_with_additives"
    E10 = "e10"
    E20 = "e20"
    E85 = "e85"
    ETHANOL = "ethanol"
    ETHANOL_WITH_ADDITIVES = "ethanol_with_additives"
    GASOLINE = "gasoline"
    HVO = "hvo"
    HYDROGEN = "hydrogen"
    LNG = "lng"
    LPG = "lpg"
    MIDGRADE = "midgrade"
    OCTANE_100 = "octane_100"
    OCTANE_87 = "octane_87"
    OCTANE_89 = "octane_89"
    OCTANE_90 = "octane_90"
    OCTANE_91 = "octane_91"
    OCTANE_92 = "octane_92"
    OCTANE_93 = "octane_93"
    OCTANE_95 = "octane_95"
    OCTANE_98 = "octane_98"
    PREMIUM = "premium"
    REGULAR = "regular"

    def __str__(self) -> str:
        return str(self.value)
