from enum import Enum


class HazardousGoodsRestrictionAny(str, Enum):
    ANY = "any"

    def __str__(self) -> str:
        return str(self.value)
