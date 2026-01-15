from enum import Enum


class ExitActionAction(str, Enum):
    EXIT = "exit"
    ROUNDABOUTEXIT = "roundaboutExit"

    def __str__(self) -> str:
        return str(self.value)
