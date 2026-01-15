from enum import Enum


class GetLookupShowNavAttributesItem(str, Enum):
    ACCESS = "access"
    FUNCTIONALCLASS = "functionalClass"
    PHYSICAL = "physical"
    SPEEDLIMITS = "speedLimits"

    def __str__(self) -> str:
        return str(self.value)
