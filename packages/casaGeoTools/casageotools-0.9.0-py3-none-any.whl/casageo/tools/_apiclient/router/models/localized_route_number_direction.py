from enum import Enum


class LocalizedRouteNumberDirection(str, Enum):
    EAST = "east"
    NORTH = "north"
    SOUTH = "south"
    WEST = "west"

    def __str__(self) -> str:
        return str(self.value)
