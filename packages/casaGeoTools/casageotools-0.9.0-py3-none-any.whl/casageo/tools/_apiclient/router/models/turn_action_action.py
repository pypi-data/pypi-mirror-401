from enum import Enum


class TurnActionAction(str, Enum):
    CONTINUEHIGHWAY = "continueHighway"
    ENTERHIGHWAY = "enterHighway"
    KEEP = "keep"
    RAMP = "ramp"
    ROUNDABOUTENTER = "roundaboutEnter"
    ROUNDABOUTPASS = "roundaboutPass"
    TURN = "turn"
    UTURN = "uTurn"

    def __str__(self) -> str:
        return str(self.value)
