from enum import Enum


class TrafficIncidentCriticality(str, Enum):
    CRITICAL = "critical"
    LOW = "low"
    MAJOR = "major"
    MINOR = "minor"

    def __str__(self) -> str:
        return str(self.value)
