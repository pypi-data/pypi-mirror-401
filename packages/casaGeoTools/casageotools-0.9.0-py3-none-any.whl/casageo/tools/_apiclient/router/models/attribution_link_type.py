from enum import Enum


class AttributionLinkType(str, Enum):
    DISCLAIMER = "disclaimer"
    TARIFF = "tariff"

    def __str__(self) -> str:
        return str(self.value)
