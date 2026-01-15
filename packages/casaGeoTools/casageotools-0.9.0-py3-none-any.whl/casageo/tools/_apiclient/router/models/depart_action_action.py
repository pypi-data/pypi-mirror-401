from enum import Enum


class DepartActionAction(str, Enum):
    DEPART = "depart"

    def __str__(self) -> str:
        return str(self.value)
