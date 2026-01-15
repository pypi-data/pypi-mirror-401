from enum import Enum


class LookupResponseClosedPermanently(str, Enum):
    MAYBE = "maybe"
    YES = "yes"

    def __str__(self) -> str:
        return str(self.value)
