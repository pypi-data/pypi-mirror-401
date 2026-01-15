from enum import Enum


class PostalCodeDetailsJapanPostPostalEntity(str, Enum):
    JAPAN_POST = "Japan Post"

    def __str__(self) -> str:
        return str(self.value)
