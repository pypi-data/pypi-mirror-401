from enum import Enum


class ViaNoticeDetailType(str, Enum):
    VIA = "via"

    def __str__(self) -> str:
        return str(self.value)
