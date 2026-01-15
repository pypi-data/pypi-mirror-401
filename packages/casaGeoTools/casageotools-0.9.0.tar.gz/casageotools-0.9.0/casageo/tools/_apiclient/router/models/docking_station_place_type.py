from enum import Enum


class DockingStationPlaceType(str, Enum):
    DOCKINGSTATION = "dockingStation"

    def __str__(self) -> str:
        return str(self.value)
