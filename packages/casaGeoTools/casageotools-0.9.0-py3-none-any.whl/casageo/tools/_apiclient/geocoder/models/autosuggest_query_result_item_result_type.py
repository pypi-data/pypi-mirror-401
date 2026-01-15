from enum import Enum


class AutosuggestQueryResultItemResultType(str, Enum):
    CATEGORYQUERY = "categoryQuery"
    CHAINQUERY = "chainQuery"

    def __str__(self) -> str:
        return str(self.value)
