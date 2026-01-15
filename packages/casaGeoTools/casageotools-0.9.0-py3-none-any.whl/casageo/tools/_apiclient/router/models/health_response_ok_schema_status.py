from enum import Enum


class HealthResponseOKSchemaStatus(str, Enum):
    OK = "ok"

    def __str__(self) -> str:
        return str(self.value)
