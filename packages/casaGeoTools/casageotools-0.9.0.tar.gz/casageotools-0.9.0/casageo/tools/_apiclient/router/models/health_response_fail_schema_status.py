from enum import Enum


class HealthResponseFailSchemaStatus(str, Enum):
    FAIL = "fail"

    def __str__(self) -> str:
        return str(self.value)
