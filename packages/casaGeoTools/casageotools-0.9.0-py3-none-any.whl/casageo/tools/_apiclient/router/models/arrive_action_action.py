from enum import Enum


class ArriveActionAction(str, Enum):
    ARRIVE = "arrive"

    def __str__(self) -> str:
        return str(self.value)
