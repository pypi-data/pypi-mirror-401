from enum import Enum


class TimeRestrictedWeekdays(str, Enum):
    FR = "fr"
    MO = "mo"
    SA = "sa"
    SU = "su"
    TH = "th"
    TU = "tu"
    WE = "we"

    def __str__(self) -> str:
        return str(self.value)
