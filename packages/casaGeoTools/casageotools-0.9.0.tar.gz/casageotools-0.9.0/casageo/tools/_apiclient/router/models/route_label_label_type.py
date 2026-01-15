from enum import Enum


class RouteLabelLabelType(str, Enum):
    NAME = "Name"
    ROUTENUMBER = "RouteNumber"

    def __str__(self) -> str:
        return str(self.value)
