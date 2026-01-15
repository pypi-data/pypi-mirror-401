from enum import Enum


class AddressUsageUsageType(str, Enum):
    NONRESIDENTIAL = "nonResidential"
    RESIDENTIAL = "residential"

    def __str__(self) -> str:
        return str(self.value)
