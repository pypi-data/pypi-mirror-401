from enum import Enum


class TruckEngineType(str, Enum):
    ELECTRIC = "electric"
    INTERNALCOMBUSTION = "internalCombustion"
    PLUGINHYBRID = "pluginHybrid"

    def __str__(self) -> str:
        return str(self.value)
