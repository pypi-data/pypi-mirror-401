from enum import Enum


class AdminNamesPreference(str, Enum):
    ALTERNATIVE = "alternative"
    PRIMARY = "primary"

    def __str__(self) -> str:
        return str(self.value)
